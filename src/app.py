import logging
import sys
import os
import json
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
from .database import session_maker
from .models import UserQuestions
from sqlalchemy import select
from .responses import VALID_QUERY_RESPONSE, INVALID_QUERY_RESPONSE, RETURN_BQ_STATEMENT

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# this makes it easier to curl the route and test functionality locally
local_deployment = os.environ.get("DB_HOST") == "localhost"
verify_requests = True
if local_deployment:
    verify_requests = False

app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    request_verification_enabled=verify_requests,
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
async def handle_slash_baldrick(ack, command, respond, context):
    user_question = str(command["text"])
    new_user_question = UserQuestions(question=user_question, user=command["user_name"])
    ack_this = await ack(
        f"For your question: {user_question}\n I have a cunning plan...",
        response_type="in_channel",
    )
    logging.debug(context)
    async with session_maker() as session:
        session.add(new_user_question)
        # We commit it first to get the created_on right. If anything dies, we'll have a record of what started it.
        await session.commit()
        await session.refresh(new_user_question)
        session.add(new_user_question)

        activities = await get_relevant_activities(user_question)
        query = await get_sql_query_with_examples(user_question, activities)
        query_plan, query_errors = get_query_plan(query)
        if query_errors is not None:
            query = await correct_sql_query(
                user_question, activities, query_plan, query_errors
            )
            query_plan, query_errors = get_query_plan(query)
        new_user_question.query = query
        new_user_question.query_plan = query_plan
        new_user_question.query_errors = query_errors

        if query_errors is None:
            data = run_query(query)
            query_explanation = await get_query_explanation(user_question, query, data)
            blocks = VALID_QUERY_RESPONSE(
                    user_question, query, query_explanation, data, new_user_question.id
                ).get_json()
            logging.debug(f"blocks: {blocks}")

            q_response = await respond(blocks)
            logging.debug(f"response: {q_response.status_code} - {q_response.body}")

            new_user_question.was_valid = True
            new_user_question.query_explanation = query_explanation
            await session.commit()
        else:
            q_response = await respond(
                INVALID_QUERY_RESPONSE(user_question, query).get_json()
            )
            logging.debug(f"response: {q_response.status_code} - {q_response.body}")

            new_user_question.was_valid = False
            await session.commit()


@app.action("results_approved")
async def results_approved(ack, body, respond):
    await ack()
    logging.debug(body)

    user_id = body["user"]["id"]
    value_json = json.loads(body["actions"][0]["value"])
    session_id = value_json["session_id"]
    async with session_maker() as session:
        user_question = await session.execute(
            select(UserQuestions).where(UserQuestions.id == session_id)
        ).first()
        user_question.marked_bad = True
        session.add(user_question)
        # We commit it first to get the created_on right. If anything dies, we'll have a record of what started it.
        await session.commit()
    # in_channel / dict
    await respond(
        {
            "response_type": "in_channel",
            "replace_original": False,
            "text": f"<@{user_id}> clicked results_approved! (in_channel)",
        }
    )
    # ephemeral / kwargs
    await respond(
        replace_original=False,
        text=":white_check_mark: Done!",
    )


@app.action("results_rejected")
async def results_rejected(ack, body, respond):
    await ack()
    logging.debug(body)

    user_id = body["user"]["id"]
    value_json = json.loads(body["actions"][0]["value"])
    session_id = value_json["session_id"]
    async with session_maker() as session:
        user_question = await session.execute(
            select(UserQuestions).where(UserQuestions.id == session_id)
        ).first()
        user_question.marked_bad = True
        session.add(user_question)
        # We commit it first to get the created_on right. If anything dies, we'll have a record of what started it.
        await session.commit()

    # in_channel / dict
    await respond(
        {
            "response_type": "in_channel",
            "replace_original": False,
            "text": f"<@{user_id}> clicked results_rejected! (in_channel)",
        }
    )
    # ephemeral / kwargs
    await respond(
        replace_original=False,
        text=":white_check_mark: Done!",
    )


@app.action("view_bigqeury")
async def view_bigqeury(ack, body, respond):
    await ack()
    logging.debug(body)

    value_json = json.loads(body["actions"][0]["value"])
    session_id = value_json["session_id"]
    async with session_maker() as session:
        user_question = await session.execute(
            select(UserQuestions).where(UserQuestions.id == session_id)
        ).first()
        user_question.viewed_query = True
        session.add(user_question)
        # We commit it first to get the created_on right. If anything dies, we'll have a record of what started it.
        await session.commit()

    # in_channel / dict
    await respond(RETURN_BQ_STATEMENT(value_json["query"]).get_json())

    # ephemeral / kwargs
    await respond(
        replace_original=False,
        text=":white_check_mark: Done!",
    )


api = FastAPI()


@api.post("/slack/events")
async def events_endpoint(req: Request):
    return await app_handler.handle(req)


@api.post("/slack/interactions")
async def interactions_endpoint(req: Request):
    return await app_handler.handle(req)
