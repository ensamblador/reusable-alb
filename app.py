#!/usr/bin/env python3
import os
import boto3
import aws_cdk as cdk

from load_balancer.load_balancer_stack import LoadBalancerStack
TAGS = {"app": "generative ai business apps", "customer": "load-balancer-stack"}


region = os.environ.get("AWS_DEFAULT_REGION")
if not region: region = "us-east-1"

caller = boto3.client('sts').get_caller_identity()
account_id = caller.get("Account")

app = cdk.App()
stk = LoadBalancerStack(app, "load-balancer-stack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account=account_id, region=region),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

if TAGS.keys():
    for k in TAGS.keys():
        cdk.Tags.of(stk).add(k, TAGS[k])
app.synth()

