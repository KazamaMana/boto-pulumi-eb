from eb_role import createRole
from rds_bd import DataBaseBuilder

from eb import ElasticBeanstalkBuilder
from eb_env_settings import EbEnvSetting
import pulumi_aws as aws

import json

with open("salts.json","r") as f:
    salts_dict = json.load(f)

eb_name = "wp-eb-rob"
vpc_id = "vpc-00fcd97ae96cce58c"
sg_id = "sg-07716f1761a895b86"
createRole("wp-eb-rob")
class_db = DataBaseBuilder("wpeb", "db.t3.micro", "wordpress", "wordpress")
class_list_settings = EbEnvSetting(vpc_id, class_db.eb_db, salts_dict, sg_id, eb_name)
eb = ElasticBeanstalkBuilder(eb_name, class_list_settings.list_settings)
