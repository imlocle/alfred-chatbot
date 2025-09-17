import boto3
import json
import os

# Cache S3 Client
_s3_client = None


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION"))
    return _s3_client


class S3Service:
    def __init__(self):
        self.client = get_s3_client()
        self.bucket_name = os.environ.get("KNOWLEDGE_BUCKET")

    def fetch_knowledge(self, file_key="knowledge_base.json"):
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=file_key)
            content = response["Body"].read().decode("utf-8")
            return json.loads(content)
        except Exception as e:
            raise e
