import boto3
import json
from logger import info


class BedrockClient:
    def __init__(self, configs):
        if configs.get('key') and configs.get('secret'):
            access_key = configs.get('key')
            secret_access_key = configs.get('secret')

            self.client = boto3.client(
                "bedrock-runtime",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_access_key,
                region_name="sa-east-1"
            )
        else:
            self.client = boto3.client(
                "bedrock-runtime",
                region_name="sa-east-1"
            )

    def generate_embedding(self, data):
        payload = {
            'inputText': str(data)
        }
        request = json.dumps(payload)
        response = self.client.invoke_model(
            modelId='amazon.titan-embed-text-v2:0',
            body=request
        )
        model_response = json.loads(response["body"].read())
        info(f"[TOKENS]: {model_response['inputTextTokenCount']}")
        return model_response["embedding"]
