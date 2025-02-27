�}q (X   custom_transformqctorchvision.transforms.transforms
Compose
q)�q}qX
   transformsq]q(cscripts.dataset.custom_transformations
GaussNoise
q)�q}q	(X   std_minq
K X   std_maxqG?�z�G�{X	   min_valueqJ����X	   max_valueqKX   pqG?�      ubcscripts.dataset.custom_transformations
ShiftHU
q)�q}q(X   limitqG?�z�G�{hG?�      hJ����hKubcscripts.dataset.custom_transformations
ScaleHU
q)�q}q(hG?�      X   scale_deltaqG?ə�����hKhJ����ubesbX   custom_transform_paramsq}q(hh	hhhhuX   albumentation_transformqcalbumentations.core.composition
Compose
q)�q}q(hcalbumentations.core.composition
Transforms
q)�q}q(h]q (calbumentations.augmentations.transforms
Flip
q!)�q"}q#(hG?�      X   always_applyq$�X   _additional_targetsq%}q&X   deterministicq'�X   save_keyq(X   replayq)X   paramsq*}q+X   replay_modeq,�X   applied_in_replayq-�ubcalbumentations.augmentations.transforms
Transpose
q.)�q/}q0(hG?�      h$�h%}q1h'�h(h)h*}q2h,�h-�ubcalbumentations.augmentations.transforms
ShiftScaleRotate
q3)�q4}q5(hG?�      h$�h%}q6h'�h(h)h*}q7h,�h-�X   shift_limit_xq8K K �q9X   shift_limit_yq:K K �q;X   scale_limitq<G?陙����G?�333333�q=X   rotate_limitq>J����K
�q?X   interpolationq@KX   border_modeqAKX   valueqBNX
   mask_valueqCNubcalbumentations.augmentations.transforms
GaussianBlur
qD)�qE}qF(hG?�      h$�h%}qGh'�h(h)h*}qHh,�h-�X
   blur_limitqIKK�qJX   sigma_limitqKK G?�      �qLubeX	   start_endqM]qN(K KeubhG?�      h,�h-�X
   processorsqO}qPX   additional_targetsqQ}qRubX   albumentation_transform_paramsqSh X    qTX8   
*******************************************************qUX   df_data_source_pathqVX^   /gpu/data/OE0441/s429r/MetaData/meta-data-public-dataset-npy-arrays-3.5mm-windowing-sigma.xlsxqWX	   data_pathqXX-   /gpu/data/OE0441/s429r/Arrays-3.5mm-sigma-01/qYX   landmark_pathqZX;   /gpu/data/OE0441/s429r/MetaData/landmarks-meta-data-v2.xlsxq[X
   model_nameq\X   data-augmentation-experimentq]X   save_dirq^X9   /gpu/checkpoints/OE0441/s429r/results/bodypartregression/q_X   shuffle_train_dataloaderq`�X   random_seedqaK h'�X
   save_modelqb�X
   base_modelqcX   vggqdX      qehUX
   batch_sizeqfK@X   effective_batch_sizeqgK@X   equidistance_rangeqh]qi(KKdeX
   num_slicesqjKX       qkhUX   alpha_hqlKX   beta_hqmG?�z�G�{X
   loss_orderqnX   hqoX   lambdaqpK X   alphaqqK X   lrqrG?6��C-X   epochsqsM�X        qthUX   descriptionquX    qvX   nameqwX   no-add-frame.pqxX   accumulate_grad_batchesqyKu.