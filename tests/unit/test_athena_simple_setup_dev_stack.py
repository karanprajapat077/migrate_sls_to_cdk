import aws_cdk as core
import aws_cdk.assertions as assertions

from athena_simple_setup_dev.athena_simple_setup_dev_stack import AthenaSimpleSetupDevStack

# example tests. To run these tests, uncomment this file along with the example
# resource in athena_simple_setup_dev/athena_simple_setup_dev_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AthenaSimpleSetupDevStack(app, "athena-simple-setup-dev")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
