import json
import os
import azure.functions as func
import logging

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]

@app.function_name(name="InteractionsHandler")
@app.route(route="interactions")
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
    except:
        return func.HttpResponse(
            "Bad signature",
            status_code = 401
        )
    
def verify_req(req: func.HttpRequest):
    signature = req.headers['x-signature-ed25519']
    timestamp = req.headers['x-signature-timestamp']
    body = req.get_body().decode("utf-8")
    
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    
    verify_key.verify(f"{timestamp}{body}".encode(), signature=bytes.fromhex(signature))