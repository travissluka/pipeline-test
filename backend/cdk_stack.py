from constructs import Construct
from aws_cdk import (
  aws_ecr as ecr,
)

class BackendResources(Construct):
  def __init__(self, scope: Construct) -> None:
    super().__init__(scope, 'Backend')

    self.base_ecr_repo = ecr.Repository(self, "BaseImage",
      image_scan_on_push=True,
    )

    self.ecr_repo = ecr.Repository(self, "Image",
      image_scan_on_push=True,
    )


