import logging
import openai
from os import environ as env
import azure.functions as func
from nacl.exceptions import BadSignatureError
from helper.functions import verify_request
from helper.functions import json_response

OPENAI_KEY = env["OPENAI_API_KEY"]

def handler(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse()
