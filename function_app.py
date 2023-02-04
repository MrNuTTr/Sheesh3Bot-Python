import azure.functions as func
from functions import message_sender
from functions import interactions_handler

app = func.FunctionApp()

# This function is the primary handler for all incoming Interactions from Discord
@app.function_name(name="InteractionsHandler")
@app.route(route="interactions", auth_level=func.AuthLevel.ANONYMOUS)
def http_handler(req: func.HttpRequest) -> func.HttpResponse:
    return interactions_handler.handler(req)

# This is the function the primary handler defers to when sending a message
@app.function_name(name="RespondToMessage")
@app.route(route="sendmessage", auth_level=func.AuthLevel.FUNCTION)
def http_handler1(req: func.HttpRequest) -> func.HttpResponse:
    return message_sender.handler(req)
