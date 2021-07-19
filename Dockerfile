# Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0
   
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.8-slim-buster
FROM nvcr.io/nvidia/pytorch:20.09-py3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy files 
WORKDIR /app
COPY requirements.txt .
COPY starter_test.py .
COPY starter.py .
COPY setup.py . 
COPY README.md .

COPY bpreg bpreg/
COPY scripts scripts/

COPY src/models/private_bpr_model/config.json src/models/private_bpr_model/config.json
COPY src/models/private_bpr_model/lookuptable.json src/models/private_bpr_model/lookuptable.json
COPY src/models/private_bpr_model/model.pt src/models/private_bpr_model/model.pt
COPY src/models/private_bpr_model/settings.json src/models/private_bpr_model/settings.json


# Install pip requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -e .
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# add root as user
USER root

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "-u", "starter.py"]

