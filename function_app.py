import logging
import azure.functions as func
from functions import message_sender
from functions import interactions_handler
from nacl.exceptions import BadSignatureError
from helper.functions import verify_request
from helper.functions import json_response

app = func.FunctionApp()

# This function is the primary handler for all Interactions from Discord
@app.function_name(name="InteractionsHandler")
@app.route(route="interactions", auth_level=func.AuthLevel.ANONYMOUS)
def http_handler(req: func.HttpRequest) -> func.HttpResponse:
    
    if not __debug__:
        try:
            verify_request(req)
        except BadSignatureError:
            logging.error("Failed to verify signature")
            return json_response({
                "Error": "Could not verify interaction signature"
                }, status_code=401
            )
    
    return interactions_handler.handler(req)

# This is the function the primary handler defers to when sending a message
@app.function_name(name="RespondToMessage")
@app.route(route="sendmessage", auth_level=func.AuthLevel.ANONYMOUS)
def http_handler1(req: func.HttpRequest) -> func.HttpResponse:
    return message_sender.handler(req)
