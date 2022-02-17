
from constructs import Construct
from aws_cdk import (
    Duration,
    RemovalPolicy,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_p,
    aws_codebuild as cb,
    aws_ssm as ssm,
    aws_ec2 as ec2,
)

class FrontendResources(Construct):
  def __init__(self, scope: Construct) -> None:
    super().__init__(scope, 'Frontend')

    self.ecr_repo = ecr.Repository(self, "Image",
      image_scan_on_push=True,
      # removal_policy=RemovalPolicy.DESTROY,
    )

    # keep track of which docker image tag is used by ECS.
    # This will let us skip pushing a new tag if nothing has changed,
    # thereby preventing ECS from doing a pointless deployment of a "new" image.
    # NOTE: I don't like it this way, find something better. Can we just read
    # the container tag from the current ECS task?
    self.image_tag = ssm.StringParameter(self, "LatestImageTag",
      string_value="None", description="The Docker image tag being used by ECS.",
      tier=ssm.ParameterTier.STANDARD)


class FrontendBuild(Construct):
  def __init__(self, scope: Construct, id: str) -> None:
    super().__init__(scope, id)


class FrontendServices(Construct):
  def __init__(self, scope: Construct, resources: FrontendResources, frontend_image: str) -> None:
    super().__init__(scope, 'Frontend')

    vpc = ec2.Vpc(self, "Vpc",
      nat_gateways=0, max_azs=1,
      cidr='10.0.0.0/16',
      subnet_configuration=[
        ec2.SubnetConfiguration(
          name='PublicSubnet',cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC)
        ])

    cluster = ecs.Cluster(self, "Cluster",
      vpc=vpc,
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
    lbfs.target_group.configure_health_check(healthy_threshold_count=2)
