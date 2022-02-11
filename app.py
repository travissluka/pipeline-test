#!/usr/bin/env python3
#
# (C) Copyright 2022-2022 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# Main AWS CDK entry point. Responsible for deploying the pipeline stack.
#-------------------------------------------------------------------------------
import os

from constructs import Construct
from aws_cdk import (
  App,
  Environment,
  Stack,
  )

from pipeline.pipeline import PipelineStack
from frontend.cdk_stack import (
  FrontendResources,
  FrontendServices
)

git_repo="travissluka/pipeline-test"
git_branch="feature/testing"
env_name = 'Dev'
jtd_name = f'Jtd{env_name}'
frontend_image_tag = os.getenv('FRONTEND_IMAGE_TAG') or 'latest'

app = App()
env = env=Environment(region="us-east-2")

# frontend/backend Resource stack (s3 buckets, ecr repos, etc...)
class ResourceStack(Stack):
  def __init__(self, scope: Construct, jtd_name: str, **kwargs) -> None:
    super().__init__(scope, f'{jtd_name}/Resources',
      description="Joint Testbed Diagnostics (JTD) base resources storage.",
      **kwargs)
    #backend_resources = BackendResources(self)
    self.frontend = FrontendResources(self)
resources = ResourceStack(app, jtd_name, env=env)

# CI/CD pipeline stack
pipeline = PipelineStack(app,
  jtd_name=jtd_name, git_repo=git_repo, git_branch=git_branch,
  frontend_resources=resources.frontend,
  env=env)
pipeline.add_dependency(resources)

# Service deployment stack (ECS, ...)
class ServiceStack(Stack):
  def __init__(self, scope: Construct, jtd_name: str, resources: FrontendResources,
      frontend_image: str, **kwargs) -> None:
    super().__init__(scope, f'{jtd_name}/Services',
      description="Joint Testbed Diagnostics (JTD) frontend/backend services.",
      **kwargs)
    self.frontend = FrontendServices(self, resources=resources, frontend_image=frontend_image)
services = ServiceStack(app, jtd_name,
  resources=resources.frontend, frontend_image=frontend_image_tag,
  env=env)

app.synth()
