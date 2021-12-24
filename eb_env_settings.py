import pulumi_aws as aws
from pulumi_aws.ec2.get_subnet_ids import AwaitableGetSubnetIdsResult

class EbEnvSetting:

    list_settings: any
    subnets_ids: AwaitableGetSubnetIdsResult

    def __init__(self, vpc_id: str, eb_db: aws.rds.Instance, salts_dict, sg_id: str, eb_name: str) -> None:

        self.subnets_ids = aws.ec2.get_subnet_ids(vpc_id=vpc_id)

        # 1. filtrar e identificar privados y publicos
        # 2. formatear los subnets ordenador por privados y 
        #   publicos en un string como este "subnet-1-public, subnet-2-public" y guardar en variable

        self.list_settings=[
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="VPCId",
                    value=vpc_id,
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="IamInstanceProfile",
                    value=eb_name + "-ec2-instance-profile"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:autoscaling:launchconfiguration",
                    name="SecurityGroups",
                    value=sg_id
                ),
                # aqui van los privados porque es el eb
                aws.elasticbeanstalk.EnvironmentSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="Subnets",
                    value="subnet-009717451db0ac979, subnet-0d91347c5cae8784e"
                ),
                # aqui van los publicos porque es el lb
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:ec2:vpc",
                    name="ELBSubnets",
                    value="subnet-009717451db0ac979, subnet-0d91347c5cae8784e"
                ),
                aws.elasticbeanstalk.EnvironmentAllSettingArgs(
                    namespace="aws:elasticbeanstalk:environment",
                    name="LoadBalancerType",
                    value="application"
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
        # for subnet in self.subnets_ids.ids:
        #     self.list_settings.append(
        #         aws.elasticbeanstalk.EnvironmentSettingArgs(
        #             namespace="aws:ec2:vpc",
        #             name="Subnets",
        #             value=subnet
        #         )
        #     )
        #     self.list_settings.append(
        #         aws.elasticbeanstalk.EnvironmentAllSettingArgs(
        #             namespace="aws:ec2:vpc",
        #             name="ELBSubnets",
        #             value=subnet
        #         )
        #     )