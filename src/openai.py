import os
import openai
import logging
from .prompts import (
    EVENT_CHOOSER_PROMPT,
    QUERY_PLAN_EXPLANATION,
    QUERY_PROMPT,
    CORRECT_QUERY_ERROR,
    QUERY_WITH_EXAMPLES_PROMPT,
)
from .embeddings import get_top_k_matches

openai.api_key = os.environ.get("OPENAI_API_KEY")


async def get_relevant_activities(user_question) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=EVENT_CHOOSER_PROMPT(user_question).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    activities = [x.strip() for x in completion["choices"][0]["text"].split(",")]
    return activities


async def get_query_explanation(user_question, sql_query) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=QUERY_PLAN_EXPLANATION(user_question, sql_query).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    response = completion["choices"][0]["text"]
    return response


async def get_sql_query(user_question, activities) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=QUERY_PROMPT(activities, user_question).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    response = completion["choices"][0]["text"]
    start_query = response.find("BigQuery Statement:") + len("BigQuery Statement:")
    end_query = response.find("BigQuery Result:")
    start_answer = response.find("Answer:") + len("Answer:") + 1

    query = response[start_query:end_query]
    example_answer = response[start_answer:]
    # need to parse the output according to the prompt and return multiple parts
    # e.g. (SQLQuery, SQLResult, Answer) from the QUERY_PROMPT
    return query, example_answer


async def get_sql_query_with_examples(user_question, activities) -> str:
    examples = get_top_k_matches(user_question)
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=QUERY_WITH_EXAMPLES_PROMPT(activities, user_question, examples).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    response = completion["choices"][0]["text"]
    start_query = response.find("BigQuery Statement:") + len("BigQuery Statement:")
    end_query = response.find("BigQuery Result:")
    start_answer = response.find("Answer:") + len("Answer:") + 1

    query = response[start_query:end_query]
    example_answer = response[start_answer:]
    # need to parse the output according to the prompt and return multiple parts
    # e.g. (SQLQuery, SQLResult, Answer) from the QUERY_PROMPT
    return query, example_answer


async def correct_sql_query(user_question, query, error) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=CORRECT_QUERY_ERROR(user_question, query, error).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    return completion["choices"][0]["text"].strip()
