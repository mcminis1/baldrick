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


@app.event("app_mention")
async def handle_app_mention(say):
    # Acknowledge command request
    await say("Yes M'Lord? Perhaps use /baldrick M'Lord?")
    pass


@app.event("message")
async def handle_message_events(ack):
    await ack()
    pass


@app.command("/baldrick")
async def handle_slash_baldrick(ack, command, respond):
    user_question = str(command["text"])
    ack_this = await ack(
        f"For your question: {user_question}\n I have a cunning plan...",
        response_type="in_channel",
    )
    logging.debug(command)
    activities = await get_relevant_activities(user_question)
    query = await get_sql_query_with_examples(user_question, activities)
    query_plan, query_errors = get_query_plan(query)
    if query_errors is not None:
        query = await correct_sql_query(
            user_question, activities, query_plan, query_errors
        )
        query_plan, query_errors = get_query_plan(query)

    if query_errors is None:
        data = run_query(query)
        query_explanation = await get_query_explanation(user_question, query, data)
        await respond(
            VALID_QUERY_RESPONSE(
                user_question, query, query_explanation, data
            ).get_json()
        )
    else:
        await respond(INVALID_QUERY_RESPONSE(user_question, query).get_json())


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.post("/slack/interactions")
async def endpoint(req: Request):
    logging.debug(req)
    return await app_handler.handle(req)
