import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_projects.portfolio_cdk_app_stack import PortfolioCdkAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in portfolio_cdk_app/portfolio_cdk_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PortfolioCdkAppStack(app, "portfolio-cdk-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
