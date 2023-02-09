import logging
import sys
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
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

@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logging.debug(f"/handle_app_mentions")
    logger.info(body)
    data = run_query("select count * from EVENT_SCHEMA")
    await say(f"app_mention: {data}")


api = FastAPI()

@api.post("/slack/events")
async def endpoint(req: Request):
    logging.debug("endpoint")
    return await app_handler.handle(req)
