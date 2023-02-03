import json
import os
import azure.functions as func
import logging
import requests

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]

@app.function_name(name="InteractionsHandler")
@app.route(route="interactions")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning("Received Interaction from Discord")
        
    try:
        verify_request(req)
        
        body = req.get_json()
        
        logging.warning(body)
        
        if body["type"] == 1:
            logging.warning("Got ping request")
            return func.HttpResponse(
                json.dumps({
                    "type": 1
                    })
            )
        elif body["type"] == 2:
            logging.warning("Incoming Application Command")
            return command_handler(body)
        
        #Unhandled message type
        logging.error("Unhandled message type")
        return func.HttpResponse(
                json.dumps({
                    "type": 1 
                    }),
            )
        
    except BadSignatureError:
        logging.error("Failed to verify signature")
        return func.HttpResponse(
            json.dumps({
                "Error": "Could not verify interaction signature"
                }),
            status_code = 401
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            json.dumps({
                "Unkown Error": ex 
                }),
            status_code = 500
        )

def command_handler(body) -> func.HttpResponse:
    return func.HttpResponse(json.dumps({"type":4}))
        #json.dumps({
        #    "type": 2,
        #    "data": {
        #        "content": "Hello, world!"
        #    }
        #    })
    #)

def verify_request(req: func.HttpRequest):
    try:
        signature = req.headers["x-signature-ed25519"]
        timestamp = req.headers["x-signature-timestamp"]
        body = req.get_json()
        
        message = timestamp + json.dumps(body, separators=(",", ":"))
        
        vk = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        vk.verify(message.encode(), bytes.fromhex(signature))

    except Exception as ex:
        raise BadSignatureError(ex)