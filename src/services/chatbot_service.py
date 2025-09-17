from aws.bedrock_service import BedrockService


class ChatbotService:
    def __init__(self, bedrock_service=None):
        self.bedrock_service = bedrock_service or BedrockService()

    def ask_alfred(self, question: str, knowledge: str) -> str:
        print(f"Q: {question}")
        system_blocks = [
            {
                "text": "You are Alfred, a helpful AI butler named after Bruce Wayne's butler Alfred Pennyworth, who knows everything about Loc Le."
            },
            {"text": f"Knowledge Base:\n{knowledge}"},
        ]
        messages = [{"role": "user", "content": [{"text": question}]}]
        return self.bedrock_service.invoke_model(system_blocks, messages)
