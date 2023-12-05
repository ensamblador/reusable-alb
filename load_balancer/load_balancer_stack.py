from aws_cdk import (
    aws_ssm as ssm,
    Stack,
    aws_elasticloadbalancingv2 as elbv2,  aws_elasticloadbalancingv2_targets as targets,
    aws_certificatemanager as acm,
    aws_ec2 as ec2,
    aws_route53 as r53,
    aws_route53_targets as r53targets,
)
from constructs import Construct

from aws_cdk.aws_ec2 import SecurityGroup, Port, Peer
from lambdas import Lambdas




class LoadBalancerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc_id = self.get_ssm_parameter("vpc-id")
        vpc = ec2.Vpc.from_lookup(self, "V", vpc_id=vpc_id)

        alb_sg, task_sg = self.create_security_groups(vpc)

        alb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True, security_group=alb_sg)
        self.alb  = alb

        http_listener = alb.add_listener("http_listener", port=80)
        http_listener.add_action(
            "80_to_443_redirect",
            action=elbv2.ListenerAction.redirect(
                port="443", permanent=True, protocol="HTTPS"
            ),
        )

        certificate = self.get_certificate()

        listener = alb.add_listener(
            "https_listener", certificates=[certificate], port=443, open=True
        )

        self.listener = listener

        listener.add_action(
            "/",
            action=elbv2.ListenerAction.fixed_response(
                200,
                content_type="application/json",
                message_body='{"msg":"hello world"}',
            ),
        )

        zone = self.get_hosted_zone()

        r53.ARecord(
            self,
            "demos_base",
            zone=zone,
            target=r53.RecordTarget.from_alias(r53targets.LoadBalancerTarget(alb)),
        )

        self.create_logout_action()

        self.create_ssm_param("task-sg-id", task_sg.security_group_id)
        self.create_ssm_param("alb-sg-id", alb_sg.security_group_id)

        self.create_ssm_param("load-balancer-arn", alb.load_balancer_arn)
        self.create_ssm_param("listener-arn", listener.listener_arn)

    def create_logout_action(self):
        L = Lambdas(self, "L")
        self.alb_logout_lambda = L.alb_logout
        
        target_group = elbv2.ApplicationTargetGroup(
            self,"TG",
            targets=[targets.LambdaTarget(self.alb_logout_lambda)]
        )

        self.listener.add_action(
            "logout-action",
            priority=1,
            action=elbv2.ListenerAction.forward(target_groups=[target_group]),   
            conditions=[elbv2.ListenerCondition.path_patterns(["/logout"])],

        )



    def create_ssm_param(self, name, value):
        ssm.StringParameter(
            self,
            f"ssm-{name}",
            parameter_name=f"/gen-ai-apps/{name}",
            string_value=value,
        )

    def get_certificate(self):
        certificate_arn = self.get_ssm_parameter("certificate-arn")
        certificate = acm.Certificate.from_certificate_arn(
            self, "ACMCert", certificate_arn=certificate_arn
        )
        return certificate

    def get_ssm_parameter(self, parameter_name):
        return ssm.StringParameter.value_from_lookup(
            self, parameter_name=f"/gen-ai-apps/{parameter_name}"
        )

    def get_hosted_zone(self):
        hosted_zone_domain_name = self.get_ssm_parameter("hosted-zone-domain-name")
        hosted_zone = r53.HostedZone.from_lookup(
            self, "hzone", domain_name=hosted_zone_domain_name
        )
        return hosted_zone

    def create_security_groups(self, vpc):
        alb_sg = SecurityGroup(
            self,
            "SG",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="ToALB",
        )
        alb_sg.add_ingress_rule(
            peer=Peer.any_ipv4(), connection=Port.tcp(80), description="Allow HTTP"
        )
        alb_sg.add_ingress_rule(
            peer=Peer.any_ipv4(), connection=Port.tcp(443), description="Allow HTTPS"
        )

        task_sg = SecurityGroup(
            self,
            "SGTask",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="ToStreamlitPrivate",
        )
        task_sg.add_ingress_rule(
            peer=alb_sg, connection=Port.tcp(8501), description="Allow 8501"
        )

        return alb_sg, task_sg
