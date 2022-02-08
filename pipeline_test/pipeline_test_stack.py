from constructs import Construct
from aws_cdk import (
    pipelines,
    Duration,
    Stack,
    Stage,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)

class Stack1(Stack):
    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope, **kwargs)


class Stage1(Stage):
    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope, **kwargs)

        stack = Stack1(self, id="empty-stack1")


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # self updating deployment pipeline
        pipeline = pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.git_hub("travissluka/pipeline-test","main"),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth"]
            )
        )

        pipeline.add_stage(Stage1(self, id="empty-stage"))



        # queue = sqs.Queue(
        #     self, "PipelineTestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "PipelineTestTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
