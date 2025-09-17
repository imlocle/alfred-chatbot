from controllers.ask_controller import AskController

from utils.errors import InvalidQuestionError, ChatbotProcessingError, CORSOriginError
from utils.response_service import error_response, success_response


class AskHandler:
    def __init__(self):
        self.controller = AskController()

    def handler(self, event, context):
        try:
            result = self.controller.handle_event(event)
            return success_response(body={"reply": result})
        except InvalidQuestionError as e:
            return error_response(
                message=str(e), headers=e.headers, status_code=e.http_status
            )
        except CORSOriginError as e:
            return error_response(
                message=f"{str(e)}: Origin: {e.origin}",
                headers=e.headers,
                status_code=e.http_status,
            )
        except Exception as e:
            error = ChatbotProcessingError(details=str(e))
            return error_response(
                message=str(error), headers=error.headers, status_code=error.http_status
            )


def lambda_handler(event, context):
    return AskHandler().handler(event, context)
