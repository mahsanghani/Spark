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

import boto3
from time import gmtime, strftime
sm_client = boto3.Session().client('sagemaker')

#define our MCE in the containers param
model_name = "multi-container-ep-custom" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
response = sm_client.create_model(
              ModelName = model_name,
              InferenceExecutionConfig = inferenceExecutionConfig,
              ExecutionRoleArn = role,
              Containers = [container1, container2])

epc_config_name = "multi-container-epc" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
endpoint_config = sm_client.create_endpoint_config(
    EndpointConfigName=epc_config_name,
    ProductionVariants=[
        {
            "VariantName": "prod",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.r5.24xlarge",
        },
    ],
)

endpoint_name = "mce-custom" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
endpoint = sm_client.create_endpoint(
    EndpointName=endpoint_name, EndpointConfigName=epc_config_name
)

import time
describe_endpoint = sm_client.describe_endpoint(EndpointName=endpoint_name)
endpoint_status = describe_endpoint["EndpointStatus"]

while endpoint_status != "InService":
    print("Current endpoint status is: {}, Trying again...".format(endpoint_status))
    time.sleep(60)
    resp = sm_client.describe_endpoint(EndpointName=endpoint_name)
    endpoint_status = resp["EndpointStatus"]

print("Endpoint status changed to 'InService'")

import json
content_type = "application/json"
request_body = {"input": "This is a test with NER in America with Amazon and Microsoft in Seattle, writing random stuff."}

#Serialize data for endpoint
data = json.loads(json.dumps(request_body))
payload = json.dumps(data)

#Endpoint invocation
response = runtime_sm_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=payload,
    TargetContainerHostname="spacyContainer")

#Parse results
result = json.loads(response['Body'].read().decode())
result

import json
content_type = "application/json"
request_body = {"input": "This is a test with NER in America with Amazon and Microsoft in Seattle, writing random stuff."}

#Serialize data for endpoint
data = json.loads(json.dumps(request_body))
payload = json.dumps(data)

#Endpoint invocation
response = runtime_sm_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=payload,
    TargetContainerHostname="textblobContainer")

#Parse results
result = json.loads(response['Body'].read().decode())
result