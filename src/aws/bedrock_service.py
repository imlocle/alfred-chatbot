import boto3
import json
import os
from botocore.config import Config


class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-west-1",
            config=Config(
                connect_timeout=3600, read_timeout=3600, retries={"max_attempts": 3}
            ),
        )
        self.model_id = os.environ.get("MODEL_ID")

    def ask_alfred(self, question: str, knowledge: str) -> str:
        system_blocks = [
            {
                "text": "You are Alfred, a helpful AI butler who knows everything about Loc Le."
            },
            {"text": f"Knowledge Base:\n{knowledge}"},
        ]
        messages = [{"role": "user", "content": [{"text": question}]}]
        payload = {
            "system": system_blocks,
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": 200,
                "temperature": 0.2,
                "topP": 0.9,
                "topK": 1,
                "stopSequences": [],
            },
        }

        try:
            print(f"question: {question}")
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload),
            )
            result = json.loads(response["body"].read())
            print(result)
            resp_messages = result.get("output", {}).get("message", {})
            if resp_messages:
                content = resp_messages.get("content", [])
                for block in content:
                    if "text" in block:
                        return block["text"]
            return "I'm sorry, I don't have an answer."
        except Exception as e:
            print(f"[BedrockService] Error: {e}")
            return "Sorry, Alfred is unavailable right now."
