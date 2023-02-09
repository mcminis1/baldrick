import logging
import sys
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from .openai import get_llm_query
from .bigquery import run_query, get_query_plan

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
app_handler = AsyncSlackRequestHandler(app)

@app.command("/baldrick")
async def handle_some_command(ack, command, respond):
    # Acknowledge command request
    await ack()
    await respond(f"{command['text']}")

@app.event("message")
async def handle_message_events(body, logger):
    logger.debug(body)
    pass


class VALID_QUERY_RESPONSE:
    def __init__(self, llm_query, llm_query_plan, data):
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.data = data
    def __str__(self):
        return f" query:\n {self.llm_query}\n\n query plan:\n {self.llm_query_plan}\n\n results: {self.data}"
    def __repr__(self):
        return str(self)


class INVALID_QUERY_RESPONSE:
    def __init__(self, llm_query):
        self.llm_query = llm_query
    def __str__(self):
        return f" query:\n {self.llm_query}\n\n query plan is invalid"
    def __repr__(self):
        return str(self)


@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logging.debug(f"/handle_app_mentions")
    logger.debug(body)
    llm_query = get_llm_query(body["event"]["text"])
    llm_query_plan = get_query_plan(llm_query)
    if llm_query_plan:
        data = run_query(llm_query)
        await say(VALID_QUERY_RESPONSE(llm_query, llm_query_plan, data))
    else:
        await say(INVALID_QUERY_RESPONSE(llm_query))


api = FastAPI()

@api.post("/slack/events")
async def endpoint(req: Request):
    logging.debug("endpoint")
    return await app_handler.handle(req)
