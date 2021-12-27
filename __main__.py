from eb_role import createRole
from rds_bd import DataBaseBuilder
import collections
from eb import ElasticBeanstalkBuilder
from eb_env_settings import EbEnvSetting
import pulumi_aws as aws

import json

with open("salts.json","r") as f:
    salts_dict = json.load(f)

eb_name = "wp-eb-rob"
vpc_id = "vpc-00fcd97ae96cce58c"
sg_id = "sg-07716f1761a895b86"


VPCDefinition = collections.namedtuple('VPCDefinition', ['vpc_id', 'public_subnet_ids', 'private_subnet_ids'])

def retrieve_vpc_and_subnets(vpc) -> VPCDefinition:
    _public_subnet_ids = aws.ec2.get_subnet_ids(vpc_id=vpc_id,
                                                tags={"Type": "Public"}).ids
    _private_subnet_ids = aws.ec2.get_subnet_ids(vpc_id=vpc_id,
                                                tags={"Type": "Private"}).ids
    return VPCDefinition(vpc_id=vpc_id, public_subnet_ids=_public_subnet_ids, private_subnet_ids=_private_subnet_ids)


Private_subnet = VPCDefinition['private_subnet_ids']
Public_subnet = VPCDefinition['public_subnet_ids']

createRole("wp-eb-rob")
class_db = DataBaseBuilder("wpeb", "db.t3.micro", "wordpress", "wordpress")
class_list_settings = EbEnvSetting(vpc_id, class_db.eb_db, salts_dict, sg_id, eb_name)
eb = ElasticBeanstalkBuilder(eb_name, class_list_settings.list_settings,private_subnet_ids=Private_subnet,public_subnet_ids=Public_subnet)
