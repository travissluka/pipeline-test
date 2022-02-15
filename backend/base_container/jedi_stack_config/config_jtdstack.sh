#!/bin/bash
# (C) Copyright 2021-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# The modules needed for building the IODA python bindings, as required by the
# JCSDA Joint Testbed Diagnostics (JTD) backend.
#-------------------------------------------------------------------------------

# Compiler/MPI combination
export JEDI_COMPILER="gnu/9.3.0"
export JEDI_MPI="openmpi/4.1.0"

# This tells jedi-stack how you want to build the compiler and mpi modules
# valid options include:
# native-module: load a pre-existing module (common for HPC systems)
# native-pkg: use pre-installed executables located in /usr/bin or /usr/local/bin,
#             as installed by package managers like apt-get or hombrewo.
#             This is a common option for, e.g., gcc/g++/gfortrant
# from-source: This is to build from source
export COMPILER_BUILD="native-pkg"
export MPI_BUILD="native-pkg"

# Build options
export PREFIX=/opt/modules
export USE_SUDO=N
export PKGDIR=pkg
export LOGDIR=buildscripts/log
export OVERWRITE=N
export NTHREADS=4
export   MAKE_CHECK=N
export MAKE_VERBOSE=N
export   MAKE_CLEAN=N
export DOWNLOAD_ONLY=F
export STACK_EXIT_ON_FAIL=T
export WGET="wget -nv"
#Global compiler flags
export FFLAGS=""
export CFLAGS=""
export CXXFLAGS=""
export LDFLAGS=""