# (C) Copyright 2022-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# JCSDA JTD main website frontend
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Base Image: latest ubuntu LTS
#-------------------------------------------------------------------------------
#FROM ubuntu:20.04 as linux-base
FROM public.ecr.aws/lts/ubuntu:20.04_stable as linux-base


#-------------------------------------------------------------------------------
# Build Stage
#-------------------------------------------------------------------------------
FROM linux-base as jtd-frontend

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        nginx \
        python3 \
        python3-pip \
        python3-ipykernel \
        jupyter \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /jtd
COPY app.ipynb .

RUN python3 -m ipykernel install --user
RUN jupyter trust app.ipynb

CMD voila --no-browser --Voila.ip=0.0.0.0 --port=80 \
  --MappingKernelManager.cull_interval=30 \
  --MappingKernelManager.cull_idle_timeout=30 \
  --preheat_kernel=True \
  --pool_size=5 \
  app.ipynb
EXPOSE 80
