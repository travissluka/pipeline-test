#!/usr/bin/env python3
#
# (C) Copyright 2022-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# Main AWS CDK entry point. Responsible for deploying the pipeline stack.
#-------------------------------------------------------------------------------
from constructs import Construct
from aws_cdk import (
  App,
  Environment,
  Stack,
  )

from pipeline.pipeline import PipelineStack
from frontend.cdk_stack import (
  FrontendResources
)

git_repo="travissluka/pipeline-test"
git_branch="feature/testing"
env_name = 'Dev'
jtd_name = f'Jtd{env_name}'


class ResourceStack(Stack):
  def __init__(self, scope: Construct, jtd_name: str, **kwargs) -> None:
    super().__init__(scope, f'{jtd_name}/Resources',
      description="Joint Testbed Diagnostics (JTD) base resources storage.",
      **kwargs)
    #backend_resources = BackendResources(self)
    self.frontend_resources = FrontendResources(self)


app = App()
env = env=Environment(region="us-east-2")

resources = ResourceStack(app, jtd_name, env=env)
pipeline = PipelineStack(app,
  jtd_name=jtd_name, git_repo=git_repo, git_branch=git_branch,
  frontend_resources=resources.frontend_resources, env=env)
pipeline.add_dependency(resources)

app.synth()
