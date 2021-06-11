import torch
import numpy as np 
import sys, os
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

sys.path.append("../../")
from scripts.utils.linear_transformations import * 

class Scores: 
    def __init__(self, 
                 scores,
                 zspacing, 
                 lower_bound=0, 
                 upper_bound=100, 
                 smoothing_sigma=10,
                 transform_min=np.nan, 
                 transform_max=np.nan): 

        scores = np.array(scores).astype(float)

        self.length = len(scores)
        self.zspacing = zspacing
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound 
        self.smoothing_sigma = smoothing_sigma
        self.transform_min = transform_min
        self.transform_max = transform_max
        self.scale=100
        self.original_values = scores
        self.original_transformed_values = linear_transform(scores, 
                                                            scale=self.scale, 
                                                            min_value=self.transform_min, 
                                                            max_value=self.transform_max)
        self.smoothed_values = self.smooth_and_transform_scores(scores)
        self.smoothed_values = self.remove_extrem_slopes(self.smoothed_values)
        self.valid_region = self.identify_valid_range()
        self.values = self.set_invalid_region_to_nan(self.smoothed_values, self.valid_region)
        self.z = np.arange(len(scores))*zspacing

        self.valid_values = self.values[~np.isnan(self.values)]
        self.valid_z = self.z[~np.isnan(self.values)]


        self.a, self.b = self.fit_linear_line()

    def __len__(self): 
        return len(self.original_values)

    def smooth_and_transform_scores(self, scores): 
        # smooth scores
        smoothed_values = gaussian_filter(scores, 
                                          sigma=self.smoothing_sigma/self.zspacing)

        # transform scores 
        if (not np.isnan(self.transform_min)) & (not np.isnan(self.transform_max)): 
            smoothed_values = linear_transform(smoothed_values, 
                                               scale=self.scale, 
                                               min_value=self.transform_min, 
                                               max_value=self.transform_max)
        return np.array(smoothed_values)

    def remove_extrem_slopes(self, x, diff_cut=0.5): 
        diffs = np.abs(np.array( list(np.diff(x)) + [0]))/self.zspacing
        clean_x = x.copy()
        clean_x[diffs > diff_cut] = np.nan

        # fill values at the top or at the bottom with nans 
        indices = np.where(np.isnan(clean_x))[0]
        if len(indices) == 0: return clean_x
        if (np.max(indices) != len(x)) and (np.max(indices) > len(x)//2): 
            clean_x[np.max(indices):] = np.nan 

        if (np.min(indices) != 0) and np.min(indices) < len(x)//2: 
            clean_x[:np.min(indices)] = np.nan 

        return clean_x

    def set_invalid_region_to_nan(self, scores, valid_indices): 
        if len(valid_indices) == 0: 
            return np.full(scores.shape, np.nan)

        min_valid_index = np.min(valid_indices)
        max_valid_index = np.max(valid_indices)

        scores[0:min_valid_index] = np.nan
        scores[max_valid_index+1:] = np.nan
        return scores 

    def identify_valid_range(self): 
        diff = self.smoothed_values[1:] - self.smoothed_values[:-1]
        negative_slope_indices = np.where(diff < 0)[0]


        # get max valid lower boundary and min valid upper boundary index 
        lower_bound_index = calculate_boundary_index(self.smoothed_values, self.lower_bound, kind="lower")
        upper_bound_index = calculate_boundary_index(self.smoothed_values, self.upper_bound, kind="upper")
        
        # correct lower boundary, if it is not smaller than the upper boundary 
        if not (lower_bound_index < upper_bound_index): 
            lower_bound_index = calculate_boundary_index(self.smoothed_values, self.lower_bound, kind="lower", max_boundary=upper_bound_index)
            upper_bound_index = calculate_boundary_index(self.smoothed_values, self.upper_bound, kind="upper", min_boundary=lower_bound_index)

        # return empty array if still upper_bound < lower_bound
        if not (lower_bound_index < upper_bound_index): return np.array([])

        # get min and max valid boundary, depending on the slope
        critical_lower_indices = negative_slope_indices[negative_slope_indices < lower_bound_index]
        critical_upper_indices = negative_slope_indices[negative_slope_indices >= upper_bound_index]

        if len(critical_lower_indices) == 0: 
            min_valid_index = 0
        else: 
            min_valid_index = np.max(critical_lower_indices)+1

        if len(critical_upper_indices) == 0: 
            max_valid_index = self.length - 1
        else: 
            max_valid_index = np.min(critical_upper_indices)

        return np.arange(min_valid_index, max_valid_index+1)

    def fit_linear_line(self): 
        if len(self.valid_z) == 0: return np.nan, np.nan
        X = np.full((len(self.valid_z), 2), 1.0, dtype=float)
        X[:, 1] = self.valid_z
        b, a = np.linalg.inv(X.T @ X) @ X.T @ self.valid_values

        return a, b

    def transform_scores(self): 
        pass 


def calculate_boundary_index(scores, bound, kind, max_boundary=np.nan, min_boundary=np.nan): 
    if kind == "lower": 
        lower_indices = np.where(scores < bound)[0]

        if len(lower_indices) == 0: 
            return 0 

        # korrekt max boundary to low
        if max_boundary < np.min(lower_indices): 
            max_boundary = len(scores) - 1

        if (~np.isnan(max_boundary)): 
            lower_indices = lower_indices[lower_indices < max_boundary]

        return np.max(lower_indices) # + 1

    if kind == "upper": 
        upper_indices = np.where(scores > bound)[0]
        upper_indices = upper_indices[upper_indices > 0]
        
        # if no upper values exist --> last index is max valid index
        if len(upper_indices) == 0: 
            return len(scores) - 1

        # korrekt min boundary if to high 
        if min_boundary > np.max(upper_indices): 
            min_boundary = 0
        
        # only use indices bigger than min boundary
        if (~np.isnan(min_boundary)):
            upper_indices = upper_indices[upper_indices > min_boundary]

        return np.min(upper_indices)  # - 1



















########## TODO #######################################
class SliceScoreProcessing: 
    def __init__(self, base_dir, gpu=1): 
        self.base_dir = base_dir

    def cut_window(self, y: np.array, min_value: int, max_value: int):
        smaller_min_cut = np.where(y < min_value)[0]
        greater_max_cut = np.where(y > max_value)[0]

        if len(smaller_min_cut) == 0: min_cut = 0
        else: min_cut = smaller_min_cut[-1] + 1

        if len(greater_max_cut) == 0: max_cut = len(y)
        else: max_cut = greater_max_cut[0]
        return np.arange(min_cut, max_cut)
    
    def cut_mask(self, filepath_source, filepath_mask, min_cut, max_cut): 
        # load mask
        mask, _ = self.load_nii(filepath_mask, swapaxes=1)

        # load scores 
        scores, x = self.predict_nii(filepath_source)

        # get cut-indices
        indices_valid = self.cut_window(scores, min_cut, max_cut)

        return indices_valid, scores, mask, x

    def check_false_positives(self, segmentation, indices_valid, filename="", printMe=False): 
        segmentation_zindices = np.where(segmentation>0)[0]
        if len(indices_valid) == 0: 
            if len(segmentation_zindices) > 0: return 1
            return 0 
        if (min(segmentation_zindices) < min(indices_valid)) or (max(segmentation_zindices) > max(indices_valid)): 
            if printMe: 
                print(f"False Positive {filename}")
                print(f"Valid range for indices: {min(indices_valid)} - {max(indices_valid)}")
                print(f"Indices of segmentation: {np.unique(segmentation_zindices)}\n")
            return 1
        return 0
    
    def get_bound_lists(self, data_path): 
        upper_bound_list = []
        lower_bound_list = []

        for file in tqdm(os.listdir(data_source_path)): 
            try: scores, _ = bpr.predict_nii(data_source_path + file)
            except: print(file); continue;
            if len(scores) == 0: continue
                
            # Take 2% percentile as minimum - for more robustness to outliers
            minimum = np.percentile(scores, 2)
            # Take 98% as maximum - for more robustness to outliers
            maximum = np.percentile(scores, 98)
            
            minimum = np.min(scores) # TODO ! 
            maximum = np.max(scores)

            lower_bound_list.append(minimum)
            upper_bound_list.append(maximum)     
        return lower_bound_list, upper_bound_list

    def find_min_max_cut(self, data_path): 
        lower_bound_list, upper_bound_list = self.get_bound_lists(data_path)

        # use 25% and 75% percentile for cuts
        max_cut = np.percentile(upper_bound_list, 75)
        min_cut = np.percentile(lower_bound_list, 25)

        return min_cut, max_cut


    def slice_score_postprocessing(self, filepaths_mask, filepaths_source, min_cut, max_cut, func = lambda x: np.where(x > 0, 1, 0)): 
        myDict = {}
        for filepath_source, filepath_mask in tqdm(zip(filepaths_source, filepaths_mask)): 
            filename_mask = filepath_mask.split("/")[-1]
            indices_valid, scores, x_mask, x = self.cut_mask(filepath_source, filepath_mask, min_cut, max_cut)
            segmentation =  func(x_mask) #np.where(x_mask > 0 , 1, 0)
            if np.sum(segmentation) == 0: continue
            fp = self.check_false_positives(segmentation, indices_valid, filename=filepath_mask, printMe=False)
            myDict[filename_mask] = {}
            myDict[filename_mask]["valid-indices"] = indices_valid
            myDict[filename_mask]["segmentation-indices"] = np.unique(np.where(segmentation>0)[0])
            myDict[filename_mask]["filepath"] = filepath_mask
            myDict[filename_mask]["false positive"] = fp 


        return myDict 

    def print_dict(self, myDict, subset=[]):
        if len(subset) == 0: subset = myDict.keys()

        for key, myDict in myDict.items(): 
            if not key in subset: continue
            if len(myDict['valid-indices']) == 0: myDict['valid-indices'] = [-1]
            print(key)
            print(f"valid region:\t\t{min(myDict['valid-indices'])} - {max(myDict['valid-indices'])}")
            print(f"Segmentation range:\t{min(myDict['segmentation-indices'])} - {max(myDict['segmentation-indices'])}\n")

    def summary_fp(self, myDict, fp_groundtruth_filenames): 
        catched_false_positives = [key for key in myDict.keys() if myDict[key]["false positive"] == 1]
        uncatched_fps = list(set(fp_groundtruth_filenames) - set(catched_false_positives))
        incorrect_fps = list(set(catched_false_positives) - set(fp_groundtruth_filenames))

        print(f"Ground truth false positives: {len(fp_groundtruth_filenames)}")
        print(f"Catched false positives: {len(catched_false_positives) }\n")
        if len(uncatched_fps) > 0: 
            print("Uncatched false positives: ")
            self.print_dict(myDict, subset=np.sort(uncatched_fps))

        else: 
            print("All false positives has been catched")

        if len(incorrect_fps) > 0: 
            print("Wrong catched files: ")
            self.print_dict(myDict, subset=np.sort(incorrect_fps))
        else: 
            print("All catched files are correct. ")

        print(f"Accuracy: {((len(catched_false_positives) - len(incorrect_fps))*100/len(fp_groundtruth_filenames)):1.0f}%")

    def fp_analysis(self, filepaths_mask, filepaths_source, fp_groundtruth_filenames): 
        fp_dict = self.slice_score_postprocessing(filepaths_mask, filepaths_source)
        self.summary_fp(fp_dict, fp_groundtruth_filenames)

        return fp_dict 

    
