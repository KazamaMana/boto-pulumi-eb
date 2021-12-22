import boto3

ec2 = boto3.client('ec2')

def createVpc():
    response = ec2.create_vpc(
        CidrBlock="10.0.0.0/16",
    )
    
    ec2.modify_vpc_attribute(VpcId = response['Vpc']['VpcId'], EnableDnsHostnames = { 'Value': True } )

    print("vpc created!")
    print("vpc_id: " + response['Vpc']['VpcId'])
    print("")
    return response['Vpc']['VpcId']

def createInternetGateway(_vpc_id):
    igw = ec2.create_internet_gateway()
    attach_igw = ec2.attach_internet_gateway(
        InternetGatewayId=igw['InternetGateway']['InternetGatewayId'],
        VpcId=_vpc_id,
    )
    print("internet gateway created!")
    print("")

def createSubnets(_vpc_id):
    public_subnet = ec2.create_subnet(
        CidrBlock="10.0.0.0/17",
        VpcId=_vpc_id
    )

    ec2.modify_subnet_attribute(
        MapPublicIpOnLaunch={'Value': True},
        SubnetId=public_subnet['Subnet']['SubnetId'])

    private_subnet = ec2.create_subnet(
        CidrBlock="10.0.128.0/17",
        VpcId=_vpc_id
    )
    print("subnets created!")
    print("")

def configSG(_vpc_id):

    sg = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    _vpc_id
                ]
            },
            {
                'Name': 'group-name',
                'Values': [
                    'default'
                ]
            }
        ]
    )

    # Clean all the rules
    boto3.resource('ec2').SecurityGroup(sg['SecurityGroups'][0]['GroupId']).revoke_ingress(IpPermissions=sg['SecurityGroups'][0]['IpPermissions'])

    sg_ingress_rule = ec2.authorize_security_group_ingress(
        GroupId=sg['SecurityGroups'][0]['GroupId'],
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0'
                }]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0'
                }]
            }
        ]
    )

    if str(sg_ingress_rule['Return']) == "True":
        print("SG created!")
        print("SG ID: " + sg['SecurityGroups'][0]['GroupId'])
    else:
        print("SG not created...")
        print(sg_ingress_rule)

vpc_id = createVpc()
createInternetGateway(vpc_id)
createSubnets(vpc_id)
configSG(vpc_id)
