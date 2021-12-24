import boto3

ec2 = boto3.client('ec2')

def look_for_eb_sg_id(vpc_id, env_name):

    response = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc_id,
                ]
            },
            {
                'Name': 'tag:Name',
                'Values': [
                    env_name,
                ]
            },
            {
                'Name': 'tag:aws:cloudformation:logical-id',
                'Values': [
                    'AWSEBSecurityGroup',
                ]
            }
        ]
    )
    return response['SecurityGroups'][0]['GroupId']

def remove_ingress_rule(sg_default, _eb_sg_id):
    boto3.resource('ec2').SecurityGroup(sg_default).revoke_ingress(IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 3306,
        'ToPort': 3306,
        'UserIdGroupPairs': [
            {
                'GroupId': _eb_sg_id,
            },
        ]
    }])
    print("ingress rule deleted")
    
eb_sg_id=look_for_eb_sg_id("vpc-03b57ac56786942ce", "wp-eb-rob-env")
remove_ingress_rule("sg-0e1c039bab019e6eb", eb_sg_id)