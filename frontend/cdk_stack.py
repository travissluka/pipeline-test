
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_p,
    aws_codebuild as cb,
)

class FrontendResources(Construct):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, 'Frontend')

        self.ecr_repo = ecr.Repository(self, "Image",
            image_scan_on_push=True,
            # removal_policy=RemovalPolicy.DESTROY,
        )


class FrontendBuild(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)


class FrontendService(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        cluster = ecs.Cluster(self, "Cluster",
            enable_fargate_capacity_providers=True)