import json
from aws.s3_service import S3Service
from aws.bedrock_service import BedrockService


class AlfredAskHandler:
    def __init__(self):
        self.s3_service = S3Service()
        self.bedrock_service = BedrockService()

    def handler(self, event, context):
        try:
            body = json.loads(event.get("body", "{}"))
            question = body.get("question")
            knowledge = self.s3_service.fetch_knowledge()
            reply = self.bedrock_service.ask_alfred(question, knowledge)
            return {"statusCode": 200, "body": json.dumps({"reply": reply})}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": e})}


def lambda_handler(event, context):
    return AlfredAskHandler().handler(event, context)
