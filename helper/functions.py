import json
import azure.functions as func
from os import environ as env
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

DISCORD_KEY = env["DISCORD_PUBLIC_KEY"]

def json_response(data, status_code = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json"
    )

def verify_request(req: func.HttpRequest):
    try:
        signature = req.headers["x-signature-ed25519"]
        timestamp = req.headers["x-signature-timestamp"]
        body = req.get_json()
        
        message = timestamp + json.dumps(body, separators=(",", ":"))
        
        vk = VerifyKey(bytes.fromhex(DISCORD_KEY))
        vk.verify(message.encode(), bytes.fromhex(signature))

    except Exception as ex:
        raise BadSignatureError(ex)