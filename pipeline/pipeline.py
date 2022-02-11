from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    SecretValue,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
)

from frontend.cdk_stack import (
  FrontendResources,
  FrontendServices
)


CODEBUILD_IMAGE = cb.LinuxBuildImage.STANDARD_5_0

class PipelineStack(Stack):

  def __init__(self, scope: Construct, jtd_name: str, git_repo: str,
                git_branch: str, frontend_resources: FrontendResources,
                **kwargs) -> None:
    super().__init__(scope, f'{jtd_name}/Pipeline',
      description="Joint Testbed Diagnostics (JTD) CI/CD pipeline",
      **kwargs)

    # the pipeline needs an s3 bucket to put things in temporarily
    pipeline_s3 = s3.Bucket(self, 'PipelineArtifacts',
      auto_delete_objects=True,
      removal_policy=RemovalPolicy.DESTROY)

    # needed for CodeBuild to run "cdk deploy"
    deploy_role=iam.PolicyStatement(
      effect=iam.Effect.ALLOW,
      actions=["sts:AssumeRole"],
      resources=["arn:aws:iam::*:role/cdk-*"]
      )

    # CI/CD pipeline
    pipeline = cp.Pipeline(self, "Pipeline",
      artifact_bucket=pipeline_s3,
      restart_execution_on_update=True,
      cross_account_keys=False)

    # pipeline stage: Get source from github
    github_token = SecretValue.secrets_manager("JtdGithubToken")
    source_output = cp.Artifact()
    source_action = cpa.GitHubSourceAction(
      action_name="github_source", output=source_output,
      owner=git_repo.split('/')[0], repo=git_repo.split('/')[1],
      branch=git_branch,
      oauth_token=github_token
    )
    pipeline.add_stage(stage_name="Source", actions=[source_action])

    # pipeline stage: Update this pipeline (self mutating... watch out for zombies)
    update_project = cb.PipelineProject(self, f'{jtd_name}PipelineUpdate',
      build_spec=cb.BuildSpec.from_source_filename("pipeline/buildspec_update.yaml"),
      environment=cb.BuildEnvironment(build_image=CODEBUILD_IMAGE)
      )
    update_project.add_to_role_policy(deploy_role)
    update_action = cpa.CodeBuildAction(
      action_name="CodeBuild", project=update_project, input=source_output)
    pipeline.add_stage(stage_name="UpdatePipeline", actions=[update_action])

    # pipeline stage: Build application containers
    # TODO move this into a separate Stage class?
    frontend_build_output = cp.Artifact('frontend_build')
    frontend_build_project = cb.PipelineProject(self, f'{jtd_name}FrontendBuild',
      build_spec=cb.BuildSpec.from_source_filename("frontend/buildspec.yaml"),
      environment=cb.BuildEnvironment(
        build_image=CODEBUILD_IMAGE,
        privileged=True),
      environment_variables={
        'REPOSITORY_URI': cb.BuildEnvironmentVariable(value=frontend_resources.ecr_repo.repository_uri),}
      )
    frontend_resources.ecr_repo.grant_pull_push(frontend_build_project)
    frontend_build = cpa.CodeBuildAction(
      action_name="FrontendBuild", input=source_output, outputs=[frontend_build_output],
      project=frontend_build_project)
    pipeline.add_stage(stage_name="BuildContainers", actions=[frontend_build,])

    #pipline stage: update services
    services_project = cb.PipelineProject(self, f'{jtd_name}Services',
      build_spec=cb.BuildSpec.from_source_filename("pipeline/buildspec_services.yaml"),
      environment=cb.BuildEnvironment(build_image=CODEBUILD_IMAGE),
    )
    services_project.add_to_role_policy(deploy_role)
    services_action = cpa.CodeBuildAction(
      action_name="Deploy", project=services_project, input=source_output,
      extra_inputs=[frontend_build_output])
    pipeline.add_stage(stage_name='UpdateServices', actions=[services_action])