import logging
import requests
from os import environ as env
import azure.functions as func
from helper.functions import json_response

AZURE_URL = env["AZURE_URL_BASE"]

def handler(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Received Interaction from Discord")
    
    body = req.get_json()
            
    if body["type"] == 1:
        logging.info("Got ping request")
        return json_response({"type": 1})

    elif body["type"] == 2:
        logging.info("Incoming Application Command")
        
        if body["data"]["name"] == "support":
            logging.info("Sending an ACK and defering")

            requests.post(f"{AZURE_URL}/sendmessage",
                None, body
            )

            return json_response({"type": 5})

        logging.error("Invalid Application Command")
    
    logging.error("Unhandled message type")
    return json_response({"type": 1})