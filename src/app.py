import logging
import sys
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from .openai import (
    get_relevant_activities,
    get_sql_query_with_examples,
    get_query_explanation,
    correct_sql_query,
)
from .bigquery import run_query, get_query_plan
from .responses import VALID_QUERY_RESPONSE, INVALID_QUERY_RESPONSE

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
app_handler = AsyncSlackRequestHandler(app)


@app.command("/baldrick")
async def handle_some_command(ack, command, respond):
    # Acknowledge command request
    await ack()
    await respond(f"{command['text']}")


@app.event("message")
async def handle_message_events(ack):
    await ack()
    pass


@app.event("app_mention")
async def handle_app_mentions(ack, body, say):
    ack_this = await ack(f"I have a cunning plan...")
    logging.debug(f"ack response: {ack_this}")
    user_question = str(body["event"]["text"])
    activities = await get_relevant_activities(user_question)
    query = await get_sql_query_with_examples(user_question, activities)
    query_plan, query_errors = get_query_plan(query)
    if query_errors is not None:
        query = await correct_sql_query(user_question, query_plan, query_errors)
        query_plan, query_errors = get_query_plan(query)

    if query_errors is None:
        query_explanation = await get_query_explanation(user_question, query)
        data = run_query(query)
        await say(
            VALID_QUERY_RESPONSE(
                activities, query, query_explanation, data
            ).to_str()
        )
    else:
        await say(INVALID_QUERY_RESPONSE(activities, query).to_str())


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)
