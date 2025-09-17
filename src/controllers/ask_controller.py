import json

from aws.s3_service import S3Service
from services.chatbot_service import ChatbotService
from utils.constants import ALLOWED_ORIGINS
from utils.errors import CORSOriginError, InvalidQuestionError


class AskController:
    def __init__(self, s3_service=None, chatbot_service=None):
        self.s3_service = s3_service or S3Service()
        self.chatbot_service = chatbot_service or ChatbotService()

    def handle_event(self, event) -> str:
        origin = event.get("headers", {}).get("origin", "")
        if origin not in ALLOWED_ORIGINS:
            raise CORSOriginError(origin=origin)
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        question: str = body.get("question", "")
        if not question:
            raise InvalidQuestionError(
                message="Please provide a question about Loc.",
                question=question,
            )
        knowledge = self.s3_service.fetch_knowledge()
        return self.chatbot_service.ask_alfred(question, knowledge)
