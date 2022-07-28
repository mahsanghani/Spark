import boto3
from sagemaker import get_execution_role

sm_client = boto3.client(service_name='sagemaker')
runtime_sm_client = boto3.client(service_name='sagemaker-runtime')
account_id = boto3.client('sts').get_caller_identity()['Account']
region = boto3.Session().region_name
role = get_execution_role()

container1 = {'Image':spacy_mce_container,'ContainerHostname': 'spacyContainer'}
container2 = {'Image':textblob_mce_container,'ContainerHostname': 'textblobContainer'}
inferenceExecutionConfig = {'Mode': 'Direct'}