import boto3
import json
import os


class S3Service:
    def __init__(self):
        self.client = boto3.client("s3")
        self.bucket_name = os.environ.get("KNOWLEDGE_BUCKET", "alfred-knowledge-bucket")

    def fetch_knowledge(self, file_key="knowledge_base.json"):
        response = self.client.get_object(Bucket=self.bucket_name, Key=file_key)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
