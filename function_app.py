import json
import os
import azure.functions as func
import logging

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = func.FunctionApp()

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]

@app.function_name(name="InteractionsHandler")
@app.route(route="interactions", auth_level=func.AuthLevel.ANONYMOUS)
def handle_request(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Received Interaction from Discord")
        
    try:
        verify_request(req)
        
        body = req.get_json()
                
        if body["type"] == 1:
            logging.info("Got ping request")
            return json_response({"type": 1})

        elif body["type"] == 2:
            logging.info("Incoming Application Command")
            return command_handler(body)
        
        #Unhandled message type
        logging.error("Unhandled message type")
        return json_response({"type": 1})

        
    except BadSignatureError:
        logging.error("Failed to verify signature")

        return json_response({
                "Error": "Could not verify interaction signature"
            }, status_code=401
        )
    except Exception as ex:
        logging.error(ex)

        return json_response({
            "Unkown Error": ex
            }, status_code=500
        )

def command_handler(body) -> func.HttpResponse:
    return json_response({
            "type": 4,
            "data": {
                "content": "Hello, world!"
            }
        }
    )

def json_response(json, status_code = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(json),
        status_code=status_code,
        mimetype="application/json"
    )

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