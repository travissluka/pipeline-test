#!/usr/bin/env python3

import aws_cdk as cdk

from pipeline_test.pipeline_test_stack import PipelineStack


app = cdk.App()
PipelineStack(app, "pipeline-test")

app.synth()
