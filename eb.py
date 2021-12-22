
from pulumi.resource import ResourceOptions
import pulumi_aws as aws

class ElasticBeanstalkBuilder:

    wp_env: aws.elasticbeanstalk.Environment
    wp_app: aws.elasticbeanstalk.Application
    eb_default_security_group: aws.ec2.get_security_group

    def __init__(self, name: str, list_settings) -> None:
        
        self.wp_app = aws.elasticbeanstalk.Application(name + "-app",
            name=name + "-app", 
            description="tf-testwp")

        self.wp_env = aws.elasticbeanstalk.Environment(name + "-env",
            name=name + "-env",
            application=self.wp_app.name,
            solution_stack_name="64bit Amazon Linux 2 v3.3.8 running PHP 8.0",
            settings=list_settings)
