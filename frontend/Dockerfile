# (C) Copyright 2022-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# JCSDA JTD main website frontend
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Base Image
#-------------------------------------------------------------------------------
FROM public.ecr.aws/amazonlinux/amazonlinux:2 as linux-base
#FROM public.ecr.aws/lts/ubuntu:20.04_stable as linux-base


#-------------------------------------------------------------------------------
# Build Stage
#-------------------------------------------------------------------------------
FROM linux-base as jtd-frontend

RUN yum update -y \
  && yum install -y \
    python3 \
    python3-pip \
  && yum clean all \
  && rm -rf /var/cache/yum

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /jtd
COPY app.ipynb .

RUN python3 -m ipykernel install --user
RUN jupyter trust app.ipynb

CMD voila --no-browser --Voila.ip=0.0.0.0 --port=80 \
  --MappingKernelManager.cull_interval=60 \
  --MappingKernelManager.cull_idle_timeout=60 \
  --preheat_kernel=True \
  --pool_size=5 \
  app.ipynb
EXPOSE 80
