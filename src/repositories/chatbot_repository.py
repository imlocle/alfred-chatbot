import os
from datetime import datetime, timedelta
from aws.bedrock_service import BedrockService
from aws.dynamodb_service import DynamodbService
from mypy_boto3_dynamodb.type_defs import (
    GetItemInputTableGetItemTypeDef,
    UpdateItemInputTableUpdateItemTypeDef,
)

from aws.s3_service import S3Service
from utils.errors import RateLimitError


class ChatbotRepository:
    def __init__(self, bedrock_service=None, dynamodb_service=None, s3_service=None):
        self.table_name = os.getenv("ALFRED_USAGE_TRACKER_TABLE")
        self.bedrock_service = bedrock_service or BedrockService()
        self.dynamodb_service = dynamodb_service or DynamodbService(
            table_name=self.table_name
        )
        self.s3_service = s3_service or S3Service()
        self.knowledge = self.s3_service.fetch_knowledge()

    def ask(self, question: str) -> str:
        system_blocks = [
            {
                "text": (
                    "You are Alfred, a distinguished and articulate AI butler inspired by Alfred Pennyworth, "
                    "Bruce Wayne's loyal and knowledgeable confidant. You serve as Loc Le's personal assistant, "
                    "possessing extensive knowledge about his professional experience, technical skills, personal projects, "
                    "hobbies, achievements, and personal background as provided in the knowledge base below.\n\n"
                    "You must answer **only** questions that are directly related to Loc Le and the knowledge base. "
                    "If a user asks about anything outside this scope (such as programming tutorials, general knowledge, "
                    "current events, or unrelated facts), you must **politely decline** and provide **no additional information**. "
                    "Do not attempt to be helpful beyond declining.\n\n"
                    "Your decline response must strictly follow this format:\n"
                    "“I'm afraid I must respectfully decline, as I can only speak on matters concerning Mr. Loc Le.”\n\n"
                    "Under no circumstances should you:\n"
                    "❌ Provide code snippets, tutorials, examples, or general knowledge unrelated to Loc Le.\n"
                    "❌ Explain topics not found in the knowledge base.\n"
                    "❌ Try to be helpful beyond the polite decline.\n\n"
                    "✅ You may answer questions about Loc's skills, work history, hobbies, opinions, or achievements.\n"
                    "✅ You must maintain a formal, composed, and respectful tone, in the manner of Alfred Pennyworth."
                )
            },
            {"text": f"Knowledge Base:\n{self.knowledge}"},
        ]
        messages = [{"role": "user", "content": [{"text": question}]}]
        return self.bedrock_service.invoke_model(system_blocks, messages)

    def check_usage(self, user_id: str, current_date: str) -> None:
        get_params: GetItemInputTableGetItemTypeDef = {
            "Key": {"pk": user_id, "sk": current_date}
        }
        response = self.dynamodb_service.get(get_params)

        count: int = response.get("count", 0)
        if count >= 50:
            raise RateLimitError()

    def update_usage(self, user_id: str, current_date: str) -> None:
        update_params: UpdateItemInputTableUpdateItemTypeDef = {
            "Key": {"pk": user_id, "sk": current_date},
            "UpdateExpression": "SET #count = if_not_exists(#count, :start) + :inc, #expires_at = :expires_at",
            "ExpressionAttributeNames": {
                "#count": "count",
                "#expires_at": "expires_at",
            },
            "ExpressionAttributeValues": {
                ":start": 0,
                ":inc": 1,
                ":expires_at": int((datetime.now() + timedelta(days=1)).timestamp()),
            },
            "ConditionExpression": "attribute_not_exists(pk) OR attribute_exists(sk)",
        }
        self.dynamodb_service.update(update_params)
