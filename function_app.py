import logging
import azure.functions as func
from os import environ as env
from nacl.exceptions import BadSignatureError
from helper.functions import verify_request
from helper.functions import json_response
from functions import wakeup
from functions import message_sender
from functions import interactions_handler

app = func.FunctionApp()
AZURE_URL = env["AZURE_URL_BASE"]

# This function is the primary handler for all Interactions from Discord
@app.function_name(name="InteractionsHandler")
@app.route(route="interactions", auth_level=func.AuthLevel.ANONYMOUS)
def http_handler(req: func.HttpRequest) -> func.HttpResponse:
    
    if env["DEBUG"] == "1":
        logging.info("In debug mode")
    else:
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

# This runs once every 20 minutes to prevent the bot from Cold Starting
@app.function_name(name="Wakeup")
@app.schedule(schedule="0 */20 * * * *", 
            arg_name="mytimer", 
            run_on_startup=False,
            use_monitor=False)
def handle_request(mytimer: func.TimerRequest) -> None:
    wakeup.handle_request(mytimer)
