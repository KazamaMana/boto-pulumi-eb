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

def set_ingress_rule(rds_sg, _eb_sg_id):

    print("RDS SG: " + rds_sg)
    print("EB SG: "+ _eb_sg_id)
    
    response = ec2.authorize_security_group_ingress(
        GroupId=rds_sg,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 3306,
                'ToPort': 3306,
                'UserIdGroupPairs': [
                    {
                        'GroupId': _eb_sg_id,
                    },
                ]
            }
        ]
    )
    if str(response['Return']) == "True":
        print("Ingress rule created!")
    else:
        print("Ingress rule not created...")
        print(response)

eb_sg_id = look_for_eb_sg_id("vpc-03b57ac56786942ce", "wp-eb-rob-env")
set_ingress_rule("sg-0e1c039bab019e6eb", eb_sg_id)