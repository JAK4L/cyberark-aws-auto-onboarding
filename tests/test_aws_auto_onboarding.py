import pytest
import boto3



class TestAwsAutoOnboardingTemplate():
  cf_client = boto3.client('cloudformation', region_name='eu-west-2')
  templatename = 'aws_auto_onboarding_0.1.1'

  @pytest.fixture
  def load_template_resources(self, branch, commitid, templateurl):
      template_params = [
                {'ParameterKey': 'LambdasBucket','ParameterValue': templateurl,'UsePreviousValue': False},
                {'ParameterKey': 'PvwaIP', 'ParameterValue': '127.0.0.1', 'UsePreviousValue': False},
                {'ParameterKey': 'UnixSafeName', 'ParameterValue': 'TestUnixSafeName', 'UsePreviousValue': False},
                {'ParameterKey': 'WindowsSafeName', 'ParameterValue': 'TestWindowsSafeName', 'UsePreviousValue': False},
                {'ParameterKey': 'VaultUser', 'ParameterValue': 'TestVaultUser', 'UsePreviousValue': False},
                {'ParameterKey': 'VaultPassword', 'ParameterValue': 'TestVaultPassword', 'UsePreviousValue': False},
                {'ParameterKey': 'CPMNameUnixSafe', 'ParameterValue': 'TestCPMNameUnixSafe', 'UsePreviousValue': False},
                {'ParameterKey': 'CPMNameWindowsSafe', 'ParameterValue': 'TestCPMNameWindowsSafe', 'UsePreviousValue': False},
                {'ParameterKey': 'ComponentsSubnet', 'ParameterValue': 'test-subnet', 'UsePreviousValue': False},
                {'ParameterKey': 'ComponentsVPC', 'ParameterValue': 'test-vpc', 'UsePreviousValue': False},
                {'ParameterKey': 'PVWASG', 'ParameterValue': 'test-pvwasg', 'UsePreviousValue': False},
                {'ParameterKey': 'KeyPairsSafe', 'ParameterValue': 'TestKeyPairsSafe', 'UsePreviousValue': False},
                {'ParameterKey': 'KeyPairName', 'ParameterValue': 'TestKeyPairName', 'UsePreviousValue': False}
      ]
      response = self.cf_client.create_change_set(
        StackName = 'test-{}-{}-{}'.format(self.templatename,branch,commitid),
        TemplateURL = '{}/{}.json'.format(templateurl, self.templatename),
        UsePreviousTemplate = False,
        Parameters = template_params,
        Capabilities = [ 'CAPABILITY_IAM' ],
        ChangeSetName = 'test-{}-{}-{}'.format(self.templatename,branch,commitid),
        Description = 'test-{}-{}-{}'.format(self.templatename,branch,commitid),
        ChangeSetType = 'CREATE'
      )

      res = self.cf_client.describe_change_set(
            StackName='test-{}-{}-{}'.format(self.templatename,branch,commitid),
            ChangeSetName='test-{}-{}-{}'.format(self.templatename,branch,commitid)
      )

      resources = {}
      for resource in res['Changes']:
        if resource['ResourceChange']['Action'] == "Add":
          if resource['ResourceChange']['ResourceType'] not in resources:
              resources[resource['ResourceChange']['ResourceType']] = []
          resources[resource['ResourceChange']['ResourceType']].append(resource['ResourceChange']['LogicalResourceId'])
      return resources


  def test_AwsAutoOnboardingDeployment(self, load_template_resources):

      print(load_template_resources)

