import json
from datetime import datetime
from services.chatbot_service import ChatbotService
from utils.constants import ALLOWED_ORIGINS
from utils.errors import CORSOriginError, InvalidQuestionError


class AskController:
    def __init__(self, chatbot_service: ChatbotService = None):
        self.chatbot_service = chatbot_service or ChatbotService()

    def handle_event(self, event) -> str:
        headers = event.get("headers", {})
        origin = headers.get("origin", "")
        if origin not in ALLOWED_ORIGINS:
            raise CORSOriginError(origin=origin)

        user_id = headers.get("x-forwarded-for", "anonymous")
        time_epoch = (
            event.get("requestContext").get("timeEpoch") / 1000
        )  # Convert ms to s
        current_date = datetime.fromtimestamp(time_epoch).strftime("%Y-%m-%d")

        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        question: str = body.get("question", "")
        if not question:
            raise InvalidQuestionError(question=question)

        return self.chatbot_service.ask(user_id, question, current_date)
