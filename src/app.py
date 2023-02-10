import logging
import sys
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from .openai import get_relevant_activities, get_sql_query
from .bigquery import run_query, get_query_plan

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
async def handle_message_events(body, logger):
    logger.debug(body)
    pass


class VALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query, llm_query_plan, example_answer, data):
        self.activities = activities
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.example_answer = example_answer
        self.data = data

    def __str__(self):
        return f" activities:\n {self.activities}\n\n query:\n {self.llm_query}\n\n query plan:\n {self.llm_query_plan}\n\n example answer:\n {self.example_answer}\n\n results: {self.data}"

    def __repr__(self):
        return str(self)


class INVALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query, example_answer):
        self.activities = activities
        self.llm_query = llm_query
        self.example_answer = example_answer

    def __str__(self):
        return f" activities:\n {self.activities}\n\n query:\n {self.llm_query}\n\n query plan is invalid\n\n example answer:\n {self.example_answer}"

    def __repr__(self):
        return str(self)


@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logging.debug(f"/handle_app_mentions")
    logger.debug(body)
    user_question = str(body["event"]["text"])
    activities = await get_relevant_activities(user_question)
    query, example_answer = await get_sql_query(user_question, activities)
    query_plan = get_query_plan(query)
    if query_plan is not None:
        data = run_query(query)
        await say(VALID_QUERY_RESPONSE(activities, query, query_plan, example_answer, data))
    else:
        await say(INVALID_QUERY_RESPONSE(activities, query, example_answer))


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    logging.debug("endpoint")
    return await app_handler.handle(req)
