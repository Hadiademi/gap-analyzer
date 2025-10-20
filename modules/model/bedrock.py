import os
import boto3
import json
from botocore.exceptions import NoCredentialsError,ClientError
from langchain_aws import BedrockEmbeddings

def create_client():
    aws_access_key_id = os.getenv("Access_Key_ID")
    aws_secret_access_key = os.getenv("Secret_Access_Key")
    return boto3.client(service_name='bedrock-runtime', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com') 

def bedrock_embedding():
    boto3_bedrock= create_client()
    bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=boto3_bedrock)   
    return bedrock_embeddings

def ask_claude(question,temperature, model="anthropic.claude-3-sonnet-20240229-v1:0", bedrock=None, max_tokens=4096):
    if not bedrock:
        bedrock = create_client()


    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages":[{"role": "user", "content": question}],
        "max_tokens": max_tokens,
        "temperature": temperature
    })

    kwargs={
        "modelId": model,
        "contentType": "application/json",
        "accept": "application/json",
        "body" : body
    }  

    try:

        response = bedrock.invoke_model(**kwargs)
        response_body = json.loads(response.get('body').read())
        return  response_body["content"][0]['text']
    
    except NoCredentialsError:
        print("We seem to have some issues with the setup!. Contact your admin!" )
        return 'None'   
        
    except bedrock.exceptions.ValidationException as e:
        print("There is some error with the prompt: {}".format(e.response['message']))
        return 'None'    