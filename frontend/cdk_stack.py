
from constructs import Construct
from aws_cdk import (
    Duration,
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


class FrontendServices(Construct):
  def __init__(self, scope: Construct, resources: FrontendResources, frontend_image: str) -> None:
    super().__init__(scope, 'Frontend')

    cluster = ecs.Cluster(self, "Cluster",
      enable_fargate_capacity_providers=True)

    voila_task = ecs.FargateTaskDefinition(
      self, 'VoilaTaskDef', cpu=512, memory_limit_mib=2048)
    voila_task.add_container("VoilaContainer",
      image=ecs.ContainerImage.from_ecr_repository(resources.ecr_repo, frontend_image),
      port_mappings=[ecs.PortMapping(container_port=80),]
    )

    lbfs = ecs_p.ApplicationLoadBalancedFargateService(self, 'LoadBalancer',
      cluster=cluster,
      desired_count=1,
      min_healthy_percent=50,
      max_healthy_percent=200,
      task_definition=voila_task,
      public_load_balancer=True,
    )
    lbfs.target_group.set_attribute('deregistration_delay.timeout_seconds', '5')
    # lbfs.target_group.configure_health_check(
    #   healthy_threshold_count=2, interval=Duration.seconds(10))
