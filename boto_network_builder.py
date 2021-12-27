import boto3

ec2 = boto3.client('ec2')
rds = boto3.client('rds')

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

    return igw['InternetGateway']['InternetGatewayId']

# 2 privados mas
# subnet group solo con un 1 privado

def createSubnets(_vpc_id):
    public_subnet = ec2.create_subnet(        
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Type',
                    'Value': 'Public'
                }
            ]
        },
    ],
        CidrBlock="10.0.0.0/17",
        VpcId=_vpc_id,
        AvailabilityZone="us-east-1a"
    )

    ec2.modify_subnet_attribute(
        MapPublicIpOnLaunch={'Value': True},
        SubnetId=public_subnet['Subnet']['SubnetId'])

    public_subnet_two = ec2.create_subnet(
                TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Type',
                    'Value': 'Public'
                }
            ]
        },
    ],
        CidrBlock="10.0.128.0/17",
        VpcId=_vpc_id,
        AvailabilityZone="us-east-1b"
    )

    ec2.modify_subnet_attribute(
        MapPublicIpOnLaunch={'Value': True},
        SubnetId=public_subnet_two['Subnet']['SubnetId'])

    subnet_group = rds.create_db_subnet_group(
        DBSubnetGroupDescription='eb-wp-rds-subnet-group',
        DBSubnetGroupName='eb-wp-rds',
        SubnetIds=[
            public_subnet['Subnet']['SubnetId'],
            public_subnet_two['Subnet']['SubnetId'],
        ],
    )
    print("subnets created!")
    print("subnet group created!")
    print("")

def createPrivateSubnets(_vpc_id):
    private_subnet_one = ec2.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Type',
                    'Value': 'Private'
                }
            ]
        },
    ],
        CidrBlock="10.0.0.0/20",
        VpcId=_vpc_id,
        AvailabilityZone="us-east-1a"
    )
    private_subnet_two = ec2.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Type',
                    'Value': 'Private'
                }
            ]
        },
    ],
        CidrBlock="10.0.128.0/20",
        VpcId=_vpc_id,
        AvailabilityZone="us-east-1b"
    )
    print("private subnet created")


def configRouteTable(_vpc_id, _igw_id):

    route_table = ec2.describe_route_tables(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    _vpc_id,
                ]
            }
        ]
    )
    ec2.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=_igw_id,
        RouteTableId=route_table['RouteTables'][0]['Associations'][0]['RouteTableId'],
    )
    print("route table has been config")
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
igw_id = createInternetGateway(vpc_id)
createSubnets(vpc_id)
createPrivateSubnets(vpc_id)
configRouteTable(vpc_id, igw_id)
configSG(vpc_id)
