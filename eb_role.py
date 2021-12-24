import pulumi_aws as aws
import json

def createRole(eb_name: str) -> None:
    eb_ec2_role = aws.iam.Role(eb_name + "-ec2-role",
        name=eb_name + "-ec2-role",
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

    aws.iam.InstanceProfile(eb_name + "-ec2-instance-profile", 
        name=eb_name + "-ec2-instance-profile", 
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