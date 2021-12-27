from eb_role import createRole
from rds_bd import DataBaseBuilder
import collections
from eb import ElasticBeanstalkBuilder
from eb_env_settings import EbEnvSetting
import pulumi_aws as aws

import json
import os

with open("salts.json","r") as f:
    salts_dict = json.load(f)

eb_name = "wp-eb-rob"
vpc_id = "vpc-0a740f406904bcc81"
sg_id = "sg-07716f1761a895b86"


private_subnet = []
public_subnet = []

def public_subnet_retrieve(_vpc_ids: str) -> public_subnet:
    _public_subnet_ids = aws.ec2.get_subnet_ids(vpc_id=_vpc_ids,
                                                tags={"Type": "Public"}).ids

def private_subnet_retrieve(_vpc_ids: str) -> public_subnet:
        _private_subnet_ids = aws.ec2.get_subnet_ids(vpc_id=_vpc_ids,
                                                tags={"Type": "Private"}).ids

private_subnet = private_subnet_retrieve(vpc_id)
public_subnet = public_subnet_retrieve(vpc_id)

print(public_subnet)

createRole("wp-eb-rob")
class_db = DataBaseBuilder("wpeb", "db.t3.micro", "wordpress", "wordpress")
class_list_settings = EbEnvSetting(vpc_id, class_db.eb_db, salts_dict, sg_id, eb_name,
    env_subnets, lb_subnets)
eb = ElasticBeanstalkBuilder(eb_name, class_list_settings.list_settings)
