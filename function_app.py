import json
import os
import azure.functions as func
import logging

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

public_key = os.environ["DISCORD_PUBLIC_KEY"]

@app.function_name(name="HttpTrigger1")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    
    try:
        verify_req(req)
        
        return func.HttpResponse(
            json.dumps({
                "type": "1"
                }),
            status_code = 200
        )
    except BadSignatureError:
        return func.HttpResponse(
            "Bad signature",
            status_code = 401
        )
    
def verify_req(req: func.HttpRequest):
    signature = req.headers['x-signature-ed25519']
    timestamp = req.headers['x-signature-timestamp']
    
    verify_key = VerifyKey(bytes.fromhex(public_key))
    
    message = timestamp + json.dump(req.get_body(), separators=(',', ':'))
    
    verify_key.verify(message.encode(), signature=bytes.fromhex(signature))