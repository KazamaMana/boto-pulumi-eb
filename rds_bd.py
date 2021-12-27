import pulumi_aws as aws

class DataBaseBuilder:

    eb_db: aws.rds.Instance

    # activar Multi-AZ
    def __init__(self, db_name: str, instance_size: str, _password: str, user_name) -> None:
        self.eb_db = aws.rds.Instance(db_name,
            allocated_storage=10,
            max_allocated_storage=100,
            apply_immediately=True,
            engine="mysql",
            engine_version="8.0.26",
            instance_class=instance_size,
            name=db_name,
            port=3306,
            parameter_group_name="default.mysql8.0",
            password=_password,
            skip_final_snapshot=True,
            multi_az=True,
            username=user_name,
            db_subnet_group_name="eb-wp-rds")