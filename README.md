# Elastic Beanstalk deploy script
This is a python script to deploy an elastic beanstallk resource with an external RDS instance.
This script uses pulumi for RDS and the EB instance while networking elements are handled mostly with the boto3 module.

### Requirements
* [Pulumi](https://www.pulumi.com/docs/get-started/aws/)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
* [EB client](https://github.com/aws/aws-elastic-beanstalk-cli-setup)

For all required modules you will need to set your [AWS credentials](https://www.pulumi.com/docs/get-started/aws/begin/) 

## How to use this script 

1.- Deploy the `boto_network_builder.py` script, this script will return a printed stringd with the ID of the VPC and Security Group, **save them for future reference**

2.- Modify the `__main__.py` file and replace the `sg_id` & `vpc_id` variables with the ID's you got from the output of the first script.

3.- `Pulumi up` for deploying the Elastic Beanstalk resource and the MYSQL Database (this comes with a salts.json included and added to the variables of the DB, please replace them as soon you finish your setup for security reasons!)


3.- Modify `boto_configs_gs.py` file on the `eb_sg_id = look_for_eb_sg_id("REPLACE VPC ID HERE","wp-eb-env")` and `set_ingress_rule("REPLACE SG-ID HERE", eb_sg_id)`

4.- Check the structure of your files and modify the code of it according to the instructions set in the **"Configure and deploy your application"** paragraph of the following AWS article:

[Deploying a high-availability WordPress website with an external Amazon RDS database to Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/php-hawordpress-tutorial.html#php-wordpress-tutorial-deploy)

5.- Upload your files through the EBCLI, to do so you need run `git init` on your wordpress root folder and from there run `eb init`, select zone and the option `[Create a new repository]`

 6.- `eb deploy wp-eb-env` and select the newly created application.


## Troubleshooting/Destroying resources

(wip)