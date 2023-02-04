import logging
import openai
import requests
from os import environ as env
import azure.functions as func

OPENAI_KEY = env["OPENAI_API_KEY"]

def handler(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing a send message request")
    
    body = req.get_json()

    # Get the OpenAI Information and request text
    openai.api_key = OPENAI_KEY
    logging.info(body)
    prompt = body["data"]["options"][0]["value"]

    logging.info("Prompt: " + prompt)

    # This should give varied and pretty random results. n=1 to save time
    ai_request = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.99,
        frequency_penalty=1,
        max_tokens=64,
        n=1
    )
    
    # This gets the actual text, it's kinda weird. Ignore the weirdness
    text = ai_request.choices[0].text.strip()  # type: ignore

    logging.info("Reponse:" + text)

    # Send the message directly to discord, now that it's generated
    # See documentation on follow-up messages
    # https://discord.com/developers/docs/interactions/receiving-and-responding#create-interaction-response
    id = body["id"]
    token = body["token"]
    discord_url = f"https://discord.com/api/{id}/{token}/callback"

    response = requests.post(
        discord_url, None, {
            "type": 4,
            "data": {
                "content": text
            }
        }
    )

    # Check if the response was sent correctly
    if response.status_code != 204:
        logging.error("Failed to send message")
        logging.error(response.content)
        return func.HttpResponse(status_code=response.status_code)

    # We were successful. Send back status code 200.
    logging.info("Message sent")
    return func.HttpResponse()