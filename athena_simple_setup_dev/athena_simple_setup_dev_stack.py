from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_athena as athena
import aws_cdk.aws_glue as glue
from constructs import Construct

"""
  The AWS CloudFormation template for this Serverless application
"""
class AthenaSimpleSetupDevStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Resources
    athenaWorkGroup = athena.CfnWorkGroup(self, 'AthenaWorkGroup',
          name = 'MyWorkGroup',
          state = 'ENABLED',
          work_group_configuration = {
            'enforceWorkGroupConfiguration': True,
            'publishCloudWatchMetricsEnabled': True,
            'resultConfiguration': {
              'outputLocation': 's3://testing-bucket-athena-tables/',
            },
          },
        )

    athenaDatabase = glue.CfnDatabase(self, 'AthenaDatabase',
          catalog_id = self.account,
          database_input = {
            'name': 'my_database',
            'description': 'My Athena Database',
          },
        )
    athenaDatabase.add_dependency(athenaWorkGroup)

    athenaTable = glue.CfnTable(self, 'AthenaTable',
          database_name = athenaDatabase.ref,
          catalog_id = self.account,
          table_input = {
            'name': 'my_table',
            'tableType': 'EXTERNAL_TABLE',
            'storageDescriptor': {
              'columns': [
                {
                  'name': 'id',
                  'type': 'string',
                },
                {
                  'name': 'name',
                  'type': 'string',
                },
              ],
              'location': 's3://testing-bucket-athena-tables/data/',
              'inputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
              'outputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
              'serdeInfo': {
                'serializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                'parameters': {
                  'field.delim': ',',
                },
              },
            },
          },
        )

    # Outputs
    self.serverless_deployment_bucket_name = 'testing-bucket-athena-tables'
    cdk.CfnOutput(self, 'CfnOutputServerlessDeploymentBucketName', 
      key = 'ServerlessDeploymentBucketName',
      export_name = 'sls-athena-simple-setup-dev-ServerlessDeploymentBucketName',
      value = str(self.serverless_deployment_bucket_name),
    )



