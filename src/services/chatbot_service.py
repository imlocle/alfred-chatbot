from aws.bedrock_service import BedrockService
from repositories.chatbot_repository import ChatbotRepository


class ChatbotService:
    def __init__(
        self,
        bedrock_service: BedrockService = None,
        chatbot_repository: ChatbotRepository = None,
    ):
        self.bedrock_service = bedrock_service or BedrockService()
        self.chatbot_repository = chatbot_repository or ChatbotRepository()

    def ask(self, user_id: str, question: str, current_date: str) -> str:
        print(f"Q: {question}")
        self.chatbot_repository.check_usage(user_id=user_id, current_date=current_date)
        response = self.chatbot_repository.ask(question=question)
        self.chatbot_repository.update_usage(user_id=user_id, current_date=current_date)
        return response
