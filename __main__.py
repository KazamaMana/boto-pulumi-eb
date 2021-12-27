from eb_role import createRole
from rds_bd import DataBaseBuilder

from eb import ElasticBeanstalkBuilder
from eb_env_settings import EbEnvSetting
import pulumi_aws as aws

import json
import os

with open("salts.json","r") as f:
    salts_dict = json.load(f)

eb_name = os.environ.get("EB_NAME")
vpc_id = os.environ.get("EB_VPC_ID")
sg_id = os.environ.get("EB_RDS_SG_ID")
env_subnets = "subnet-02e5d5ec1f202811e, subnet-081e7f228051433b2" #privates
lb_subnets = "subnet-014730c82b5781e84, subnet-0618225b91041e6ee" #publics

createRole(eb_name)
class_db = DataBaseBuilder("wpeb", "db.t3.micro", "wordpress", "wordpress")
class_list_settings = EbEnvSetting(vpc_id, class_db.eb_db, salts_dict, sg_id, eb_name,
    env_subnets, lb_subnets)
eb = ElasticBeanstalkBuilder(eb_name, class_list_settings.list_settings)
