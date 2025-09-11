import json
from aws.s3_service import S3Service
from services.alfred_service import AlfredService


s3_service = S3Service()
alfred_service = AlfredService()


class AlfredAskHandler:
    def __init__(self):
        pass

    def handler(self, event, context):
        try:
            body = json.loads(event.get("body", "{}"))
            question = body.get("question")
            knowledge = s3_service.fetch_knowledge()
            reply = alfred_service.ask(question, knowledge)
            return {"statusCode": 200, "body": json.dumps({"reply": reply})}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": e})}


def lambda_handler(event, context):
    return AlfredAskHandler().handler(event, context)
