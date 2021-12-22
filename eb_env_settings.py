import pulumi_aws as aws
from pulumi_aws.ec2 import vpc
from pulumi_aws.ec2.get_subnet_ids import AwaitableGetSubnetIdsResult
from pulumi_aws.ec2.vpc import Vpc

class EbEnvSetting:

    list_settings: any
    subnets_ids: AwaitableGetSubnetIdsResult

    def __init__(self, vpc_id: str, eb_db: aws.rds.Instance, salts_dict) -> None:

        self.list_settings=[
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="VPCId",
                    value=vpc_id,
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="IamInstanceProfile",
                    value="wordpress-deploy-elasticbeanstalk-ec2-role"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="ELBScheme",
                    value="internet facing"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:autoscaling:asg",
                    name="MinSize",
                    value="1"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:autoscaling:asg",
                    name="MaxSize",
                    value="2"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="RDS_HOSTNAME",
                    value=eb_db.address
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="RDS_PORT",
                    value="3306"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="RDS_DB_NAME",
                    value=eb_db.name
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="RDS_PASSWORD",
                    value=eb_db.password
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="RDS_USERNAME",
                    value=eb_db.username
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="AUTH_KEY",
                    value=salts_dict.get('AUTH_KEY')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="SECURE_AUTH_KEY",
                    value=salts_dict.get('SECURE_AUTH_KEY')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="LOGGED_IN_KEY",
                    value=salts_dict.get('LOGGED_IN_KEY')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="NONCE_KEY",
                    value=salts_dict.get('NONCE_KEY')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="AUTH_SALT",
                    value=salts_dict.get('AUTH_SALT')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="SECURE_AUTH_SALT",
                    value=salts_dict.get('SECURE_AUTH_SALT')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="LOGGED_IN_SALT",
                    value=salts_dict.get('LOGGED_IN_SALT')
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:application:environment",
                    name="NONCE_SALT",
                    value=salts_dict.get('NONCE_SALT')
                )
            ]
        self.subnets_ids = aws.ec2.get_subnet_ids(vpc_id=vpc_id)
        for subnet in self.subnets_ids.ids:
            self.list_settings.append(
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="Subnets",
                    value=subnet
                )
            )
