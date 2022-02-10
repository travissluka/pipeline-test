#!/usr/bin/env python3
#
# (C) Copyright 2022-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# Main AWS CDK entry point. Responsible for deploying the pipeline stack.
#-------------------------------------------------------------------------------
import aws_cdk as cdk

from pipeline.pipeline import JTDPipeline

git_repo="travissluka/pipeline-test"
git_branch="feature/testing"

app = cdk.App()

JTDPipeline(app, git_repo, git_branch, env=cdk.Environment(region="us-east-2"))

app.synth()
