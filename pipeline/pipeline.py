from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    SecretValue,
    Stack,
    RemovalPolicy,
    aws_ecr as ecr,
    aws_s3 as s3,
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
)

# class Assets(Stack):
#   def __init__(self, scope: Construct, construct_id: str, ) -> None:
#     super().__init__(scope, construct_id)
#     frontend_repo = ecr.Repository(self, "TempRepo",
#       removal_policy=RemovalPolicy.DESTROY)

# class Services(Stack):
#   def __init__(self, scope: Construct, construct_id: str, ) -> None:
#     super().__init__(scope, construct_id)


class JTDPipeline(Stack):

  def __init__(self, scope: Construct, git_repo: str,
                git_branch: str, **kwargs) -> None:
    env_name = 'Dev' # TODO:  base this on the git branch
    jtd_name = f"Jtd{env_name}"
    super().__init__(scope, jtd_name,
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
      environment=cb.BuildEnvironment(build_image=cb.LinuxBuildImage.STANDARD_5_0)
      )
    update_project.add_to_role_policy(deploy_role)
    update_action = cpa.CodeBuildAction(
      action_name="CodeBuild", project=update_project, input=source_output)
    pipeline.add_stage(stage_name="UpdatePipeline", actions=[update_action])

    # # Update application stacks
    # app_project = cb.PipelineProject(self, 'app-update',
    #   build_spec=cb.BuildSpec.from_source_filename("pipeline/buildspec_app.yaml"),
    #   environment=cb.BuildEnvironment(build_image=cb.LinuxBuildImage.STANDARD_5_0)
    # )
    # app_project.add_to_role_policy(deploy_role)
    # app_action = cpa.CodeBuildAction(
    #   action_name="CodeBuild", project=app_project, input=source_output)
    # pipeline.add_stage(stage_name="AppDeploy", actions=[app_action])


    # # repositories to hold the assets
    # repo = ecr.Repository(self, "FrontendImage",
    #   removal_policy=RemovalPolicy.DESTROY)

    # # overall build pipeline
    # pipeline = cp.Pipeline(self, "Pipeline", cross_account_keys=False)

    # # Get source from github
    # github_token = SecretValue.secrets_manager("github-token")
    # source_output = cp.Artifact()
    # source_action = cpa.GitHubSourceAction(
    #   action_name="github_source", output=source_output,
    #   owner=git_repo.split('/')[0], repo=git_repo.split('/')[1],
    #   branch=git_branch,
    #   oauth_token=github_token
    # )
    # pipeline.add_stage(stage_name="Source", actions=[source_action])

    # # build containers and put in ECR
    # project = cb.PipelineProject(self, f'{construct_id}-frontendBuild',
    #   build_spec=cb.BuildSpec.from_source_filename("frontend/buildspec.yaml"),
    #   environment=cb.BuildEnvironment(privileged=True),
    #   environment_variables=
    #     {'REPOSITORY_URI': cb.BuildEnvironmentVariable(value=repo.repository_uri),})
    # repo.grant_pull_push(project)
    # build_action = cpa.CodeBuildAction(
    #   action_name="CodeBuild", project=project, input=source_output,
    # )
    # pipeline.add_stage(stage_name="Build", actions=[build_action])