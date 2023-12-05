import sys

from aws_cdk import (aws_lambda, Duration, aws_iam as iam)

from constructs import Construct


LAMBDA_TIMEOUT= 60

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=128,
    architecture=aws_lambda.Architecture.ARM_64,
    tracing= aws_lambda.Tracing.ACTIVE)

PYTHON_LAMBDA_CONFIG = dict(runtime=aws_lambda.Runtime.PYTHON_3_11, **BASE_LAMBDA_CONFIG)




class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        COMMON_LAMBDA_CONF = dict(**PYTHON_LAMBDA_CONFIG)
        
        self.alb_logout = aws_lambda.Function(
            self, "alb_logout", handler="alb_logout/lambda_function.lambda_handler",
            code = aws_lambda.Code.from_asset("./lambdas/code/"),**COMMON_LAMBDA_CONF)
        
    
    


         