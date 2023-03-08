from os import environ as env
import datetime
import azure.functions as func
import logging
import requests

AZURE_URL = env["AZURE_URL_BASE"]

def handle_request(wakeup: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if wakeup.past_due:
        logging.warn("Waking up to prevent cold start")
        requests.post(f"{AZURE_URL}/interactions",
                None, {
                    "type": 1
                }
            )

    logging.info("Python timer trigger function ran at %s", utc_timestamp)
