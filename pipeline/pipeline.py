from constructs import Construct
from aws_cdk import (
    SecretValue,
    Stack,
    RemovalPolicy,
    aws_ecr as ecr,
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
)


class JTDPipeline(Stack):

  def __init__(self, scope: Construct, git_repo: str,
                git_branch: str, **kwargs) -> None:
    env_name = 'dev' # TODO:  base this on the git branch
    construct_id = f"jtd-{env_name}"
    super().__init__(scope, construct_id, **kwargs)

    # repositories to hold the assets
    repo = ecr.Repository(self, "FrontendImage",
      removal_policy=RemovalPolicy.DESTROY)

    # overall build pipeline
    pipeline = cp.Pipeline(self, "Pipeline", cross_account_keys=False)

    # Get source from github
    source_output = cp.Artifact()
    source_action = cpa.GitHubSourceAction(
      action_name="github_source", output=source_output,
      owner=git_repo.split('/')[0], repo=git_repo.split('/')[1],
      branch=git_branch,
      oauth_token=SecretValue.secrets_manager("github-token")
    )
    pipeline.add_stage(stage_name="Source", actions=[source_action])

    # build containers and put in ECR
    project = cb.PipelineProject(self, f'{construct_id}-frontendBuild',
      build_spec=cb.BuildSpec.from_source_filename("frontend/buildspec.yaml"),
      environment=cb.BuildEnvironment(privileged=True),
      environment_variables=
        {'REPOSITORY_URI': cb.BuildEnvironmentVariable(value=repo.repository_uri),})
    repo.grant_pull_push(project)
    build_action = cpa.CodeBuildAction(
      action_name="CodeBuild", project=project, input=source_output,
    )
    pipeline.add_stage(stage_name="Build", actions=[build_action])