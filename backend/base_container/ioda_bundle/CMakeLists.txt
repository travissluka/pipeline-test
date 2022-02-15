# (C) Copyright 2021-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# IODA bundle as required by the JCSDA Joint Testbed Diagnostics (JTD) backend
#
# TODO: use a proper tag of OOPS/IODA once available. (1.2.0 / 2.1.0 did not
# have the latest required chagnes to the python bindings)
# -------------------------------------------------------------------------------

cmake_minimum_required( VERSION 3.12 FATAL_ERROR )
project( ioda-bundle VERSION 1.0.0 LANGUAGES C CXX Fortran )

find_package( ecbuild 3.3.2 REQUIRED)
include( ecbuild_bundle )

ecbuild_bundle_initialize()

ecbuild_bundle( PROJECT jedicmake GIT "https://github.com/JCSDA/jedi-cmake.git" TAG 1.2.0 )
include( jedicmake/cmake/Functions/git_functions.cmake )


ecbuild_bundle( PROJECT oops GIT "https://github.com/JCSDA/oops.git" TAG 281689f)
#1.2.0 )
ecbuild_bundle( PROJECT ioda GIT "https://github.com/JCSDA/ioda.git" TAG abf8626)
#2.1.0)

ecbuild_bundle_finalize()