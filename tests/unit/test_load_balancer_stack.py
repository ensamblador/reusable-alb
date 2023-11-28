import aws_cdk as core
import aws_cdk.assertions as assertions

from load_balancer.load_balancer_stack import LoadBalancerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in load_balancer/load_balancer_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LoadBalancerStack(app, "load-balancer")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
