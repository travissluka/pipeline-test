#!/usr/bin/env python3

import aws_cdk as cdk

from pipeline.pipeline import JTDPipeline

git_repo="travissluka/pipeline-test"
git_branch="feature/testing"

app = cdk.App()
JTDPipeline(app, git_repo, git_branch,
    env=cdk.Environment(region="us-east-1"))

app.synth()
