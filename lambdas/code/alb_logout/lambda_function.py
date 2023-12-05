import os
import json
import os


#https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html
def lambda_handler(event, context):
    logout_cognito_url = os.environ.get("LOGOUT_URL")
    host=event.get("headers").get("host", "google.com")
    params = event.get("queryStringParameters")
    congnito_domain = params["logout_domain"]
    client_id = params["client_id"]

    tg_arn = event.get("requestContext").get("elb").get("targetGroupArn")
    region = tg_arn.split(":elasticloadbalancing:")[1].split(":")[0]

    host = f"https://{congnito_domain}.auth.{region}.amazoncognito.com/logout?client_id={client_id}&logout_uri=https%3A//{host}"
    html = f'<head><meta http-equiv="Refresh" content="0; URL={host}" /></head>'

    #html = "OK
    return build_response(200, html)


def build_response(status_code, json_content):
        return {
        'statusCode': status_code,
        "headers": {
            "Content-Type": "text/html;charset=UTF-8",
            "charset": "UTF-8",
            "Access-Control-Allow-Origin": "*",
            "Set-Cookie":"AWSELBAuthSessionCookie-0=deleted; Max-Age=-1, AWSELBAuthSessionCookie-1=deleted; Max-Age=-1"
            #"cookie": "AWSELBAuthSessionCookie-0=deleted; AWSELBAuthSessionCookie-1=deleted; AWSELBAuthSessionCookie-2=deleted; AWSELBAuthSessionCookie-3=deleted"
        },
        'body': json_content
    }
