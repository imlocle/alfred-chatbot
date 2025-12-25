from controllers.ask_controller import AskController

from utils.errors import (
    InvalidQuestionError,
    ChatbotProcessingError,
    CORSOriginError,
    RateLimitError,
)
from utils.response_service import error_response, success_response


class AskHandler:
    def __init__(self):
        self.controller = AskController()

    def handler(self, event, context):
        try:
            result: str = self.controller.handle_event(event)
            return success_response(body={"reply": result})
        except InvalidQuestionError as e:
            print(f"Error: {str(e)}")
            return error_response(
                message="I am sorry, but that was an invalid question. Please ask another.",
                headers=e.headers,
                status_code=e.http_status,
            )
        except CORSOriginError as e:
            print(f"Error: {str(e)}: Origin: {e.origin}")
            return error_response(
                message="I am sorry, but you are chatting with me from a different place. Please continue this conversation through Loc's website.",
                headers=e.headers,
                status_code=e.http_status,
            )
        except RateLimitError as e:
            print(f"Error: {str(e)}")
            return error_response(
                message="I apologize, but you have reached the limit for today. Please come back tomorrow.",
                headers=e.headers,
                status_code=e.http_status,
            )
        except Exception as e:
            error = ChatbotProcessingError(details=str(e))
            print(f"Error: {str(error)}")
            return error_response(
                message="My apologies, I am currently unavailable. Please come back soon.",
                headers=error.headers,
                status_code=error.http_status,
            )


def lambda_handler(event, context):
    return AskHandler().handler(event, context)
