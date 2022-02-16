#!/bin/bash
# (C) Copyright 2021-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# The modules needed for building the IODA python bindings, as required by the
# JCSDA Joint Testbed Diagnostics (JTD) backend.
#-------------------------------------------------------------------------------

# Minimal JEDI Stack
export      STACK_BUILD_CMAKE=N
export     STACK_BUILD_GITLFS=N
export       STACK_BUILD_SZIP=N
export    STACK_BUILD_UDUNITS=N
export       STACK_BUILD_ZLIB=N
export     STACK_BUILD_LAPACK=N
export STACK_BUILD_BOOST_HDRS=N
export       STACK_BUILD_BUFR=N
export     STACK_BUILD_EIGEN3=N
export       STACK_BUILD_HDF5=N
export    STACK_BUILD_PNETCDF=N
export     STACK_BUILD_NETCDF=N
export      STACK_BUILD_NCCMP=N
export    STACK_BUILD_ECBUILD=Y
export      STACK_BUILD_ECKIT=Y
export      STACK_BUILD_FCKIT=Y
export      STACK_BUILD_ATLAS=Y
export   STACK_BUILD_GSL_LITE=Y
export   STACK_BUILD_PYBIND11=N

# Optional Additions
export           STACK_BUILD_ODC=N
export           STACK_BUILD_PIO=N
export          STACK_BUILD_GPTL=N
export           STACK_BUILD_NCO=N
export        STACK_BUILD_PYJEDI=N
export      STACK_BUILD_NCEPLIBS=N
export          STACK_BUILD_JPEG=N
export           STACK_BUILD_PNG=N
export        STACK_BUILD_JASPER=N
export     STACK_BUILD_ARMADILLO=N
export        STACK_BUILD_XERCES=N
export        STACK_BUILD_TKDIFF=N
export    STACK_BUILD_BOOST_FULL=N
export          STACK_BUILD_ESMF=N
export      STACK_BUILD_BASELIBS=N
export     STACK_BUILD_PDTOOLKIT=N
export          STACK_BUILD_TAU2=N
export          STACK_BUILD_CGAL=N
export          STACK_BUILD_GEOS=N
export        STACK_BUILD_SQLITE=N
export          STACK_BUILD_PROJ=N
export           STACK_BUILD_FMS=N
export          STACK_BUILD_JSON=N
export STACK_BUILD_JSON_SCHEMA_VALIDATOR=N
export        STACK_BUILD_ECFLOW=N