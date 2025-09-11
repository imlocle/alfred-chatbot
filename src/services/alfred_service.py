from aws.bedrock_service import BedrockService


class AlfredService:
    def __init__(self):
        self.bedrock_service = BedrockService()

    def ask(self, question: str, knowledge: str) -> str:
        print(f"Q: {question}")
        system_blocks = [
            {
                "text": "You are Alfred, a helpful AI butler named after Bruce Wayne's butler Alfred Pennyworth, who knows everything about Loc Le."
            },
            {"text": f"Knowledge Base:\n{knowledge}"},
        ]
        messages = [{"role": "user", "content": [{"text": question}]}]
        return self.bedrock_service.invoke_model(system_blocks, messages)
