import logging
import openai
from os import environ as env
import azure.functions as func
from nacl.exceptions import BadSignatureError
from helper.functions import verify_request
from helper.functions import json_response

OPENAI_KEY = env["OPENAI_API_KEY"]

def handler(req: func.HttpRequest) -> func.HttpResponse:
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
    if body["data"]["name"] == "support":
        openai.api_key = OPENAI_KEY
        logging.info(body)
        prompt = body["data"]["options"][0]["value"]

        logging.info("Prompt: " + prompt)

        ai_request = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.99,
            frequency_penalty=1,
            max_tokens=64,
            n=1
        )
        
        response = ai_request.choices[0].text.strip()  # type: ignore

        logging.info("Reponse:" + response)

        return json_response({
            "type": 4,
            "data": {
                "content": response
            }
        })

    return json_response({
        "type":2,
        "data":{
            "content": "Unhandled command."
        },
        "flags": 1 << 6
    })