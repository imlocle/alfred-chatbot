from repositories.chatbot_repository import ChatbotRepository


class ChatbotService:
    def __init__(
        self,
        chatbot_repository: ChatbotRepository = None,
    ):
        self.chatbot_repository = chatbot_repository or ChatbotRepository()

    def ask(self, user_id: str, question: str, current_date: str) -> str:
        self.chatbot_repository.check_usage(user_id=user_id, current_date=current_date)
        response = self.chatbot_repository.ask(question=question)
        self.chatbot_repository.update_usage(user_id=user_id, current_date=current_date)
        return response
