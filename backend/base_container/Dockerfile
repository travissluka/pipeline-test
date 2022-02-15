#-------------------------------------------------------------------------------
# (C) Copyright 2021-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# JCSDA JTD base image for the backend.
#
# The resulting docker image contains all of the required dependencies for
# BESPIN and PADME to be run under AWS Lambda (as well as codebuild testing
# of individual BESPIN/PADME repos).
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Build Stage
#
# A minimal jedi stack is built in order to build the IODA python library. Also,
# several required dependencies are built (e.g. PROJ which is needed by cartopy,
# which is needed by PADME).
#-------------------------------------------------------------------------------
FROM public.ecr.aws/lts/ubuntu:20.04_stable as jtd-backend-base-build

WORKDIR /var/jtd_build

# system dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        g++ \
        gcc \
        gfortran \
        git \
        libblas-dev \
        libboost-all-dev \
        libeigen3-dev \
        libgeos-dev \
        liblapack-dev \
        libnetcdf-dev \
        libnetcdff-dev \
        libopenmpi-dev \
        libsqlite3-dev \
        libtiff-dev \
        lmod \
        make \
        pybind11-dev \
        python3 \
        python3-dev \
        python3-pip \
        sqlite3 \
        wget \
        \
    && rm -rf /var/lib/apt/lists/*

# setup an install directory
ARG JTD_RUNTIME=/var/jtd_runtime
ENV CPPFLAGS=-I${JTD_RUNTIME}/include \
    LD_LIBRARY_PATH=${JTD_RUNTIME}/lib:${LD_LIBRARY_PATH} \
    LDFLAGS=-L${JTD_RUNTIME}/lib \
    PATH=${JTD_RUNTIME}/bin:${PATH}

# build PROJ dependency for python-cartopy
# (ubuntu 20.04 doesn't have a new enough version in apt)
ARG PROJ_VERSION=8.2.0
RUN wget https://github.com/OSGeo/PROJ/releases/download/${PROJ_VERSION}/proj-${PROJ_VERSION}.tar.gz\
    && tar -xaf proj-${PROJ_VERSION}.tar.gz
RUN mkdir proj_build \
    && cd proj_build \
    && cmake ../proj-${PROJ_VERSION} -DCMAKE_INSTALL_PREFIX=${JTD_RUNTIME} \
    && make -j 4 \
    && make install

# build part of jedi-stack (ecbuild, eckit, fckit, atlas, gsl_lite)
# The bare minimum that we need for compiling the ioda python bindings
ARG JEDI_STACK_BRANCH=1.1.0
RUN git clone --branch ${JEDI_STACK_BRANCH} \
    https://git@github.com/jcsda/jedi-stack
COPY jedi_stack_config jedi-stack/buildscripts/config
ENV JEDI_OPT=/opt/modules
RUN . /etc/profile.d/lmod.sh \
    && jedi-stack/buildscripts/setup_modules.sh jtdstack \
    && module use ${JEDI_OPT}/modulefiles/core \
    && jedi-stack/buildscripts/build_stack.sh jtdstack

# build ioda
COPY ioda_bundle ioda_bundle/
RUN mkdir ioda_build\
    && cd ioda_build\
    && . /etc/profile.d/lmod.sh\
    && module use ${JEDI_OPT}/modulefiles/core\
    && module load ecbuild jedi-gnu jedi-openmpi eckit fckit atlas gsl_lite\
    && ecbuild ../ioda_bundle -DBUILD_PYTHON_BINDINGS=ON \
    && cd ioda/src/engines/ioda\
    && make -j 4

# copy jedi libs to a staging directory
# TODO: do a make install in the above step instead??
RUN . /etc/profile.d/lmod.sh \
    && mkdir -p ${JTD_RUNTIME}/lib/python3.8/site-packages \
    && module use ${JEDI_OPT}/modulefiles/core\
    && module load ecbuild jedi-gnu jedi-openmpi eckit fckit atlas gsl_lite \
    && mv $ECKIT_PATH/lib/*.so* ${JTD_RUNTIME}/lib \
    && mv $FCKIT_PATH/lib/*.so* ${JTD_RUNTIME}/lib \
    && mv $ATLAS_PATH/lib/*.so* ${JTD_RUNTIME}/lib \
    && mv ioda_build/lib/*.so*  ${JTD_RUNTIME}/lib \
    && mv ioda_build/lib/python3.8/pyioda/* ${JTD_RUNTIME}/lib/python3.8/site-packages/

# setup rest of python environment
COPY requirements.txt .
RUN pip3 install --no-cache-dir --prefix ${JTD_RUNTIME} -r requirements.txt


#-------------------------------------------------------------------------------
# Runtime Stage
#
# pull only what we need from the build stage
#-------------------------------------------------------------------------------
FROM public.ecr.aws/lts/ubuntu:20.04_stable as jtd-backend-base

ENV JTD_ROOT=/var/jtd
WORKDIR ${JTD_ROOT}

# copy runtime from build stage
COPY --from=jtd-backend-base-build /var/jtd_runtime .

# system dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        libcurl3-gnutls\
        libgeos-c1v5 \
        libgomp1\
        liblapack3\
        libnetcdff7\
        libopenmpi3\
        libtiff5 \
        python3 \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=${JTD_ROOT}/bin:${PATH} \
    LD_LIBRARY_PATH=${JTD_ROOT}/lib:${LD_LIBRARY_PATH} \
    PYTHONPATH=${JTD_ROOT}/lib/python3.8/site-packages:${PYTHONPATH}


#-------------------------------------------------------------------------------
# TODO add a testing stage?
#-------------------------------------------------------------------------------