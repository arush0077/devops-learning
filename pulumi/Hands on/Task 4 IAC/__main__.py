import pulumi
config = pulumi.Config()
region = config.require('aws_region')
secret_key = config.require_secret('secret_key')

pulumi.export('region', region)
pulumi.export('secret_key', secret_key)
