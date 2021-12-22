import pulumi_aws as aws
import json

def createRole() -> None:
    eb_ec2_role = aws.iam.Role("wordpress-deploy-elasticbeanstalk-ec2-role",
        name="wordpress-deploy-elasticbeanstalk-ec2-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "",
                "Principal": {
                    "Service": "ec2.amazonaws.com",
                },
            }],
        }))

    aws.iam.InstanceProfile("wp-deploy-eb-ec2-role", 
        name="wordpress-deploy-elasticbeanstalk-ec2-role", 
        role=eb_ec2_role.name)

    aws.iam.PolicyAttachment("WebTier",
        roles=[eb_ec2_role.name],
        policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier")

    aws.iam.PolicyAttachment("EBWorker",
        roles=[eb_ec2_role.name],
        policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWorkerTier")

    aws.iam.PolicyAttachment("MCDocker",
        roles=[eb_ec2_role.name],
        policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkMulticontainerDocker")