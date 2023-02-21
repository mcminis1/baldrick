import os
import openai
import logging
from typing import List
from .prompts import (
    EVENT_CHOOSER_PROMPT,
    QUERY_PLAN_EXPLANATION,
    CORRECT_QUERY_ERROR,
    QUERY_WITH_EXAMPLES_PROMPT,
)
from .embeddings import get_top_k_matches

openai.api_key = os.environ.get("OPENAI_API_KEY")


async def get_relevant_activities(user_question) -> List[str]:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=EVENT_CHOOSER_PROMPT(user_question).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    activities = [x.strip() for x in completion["choices"][0]["text"].split(",")]
    return activities


async def get_query_explanation(user_question, sql_query, answer) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=QUERY_PLAN_EXPLANATION(user_question, sql_query, answer).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    response = completion["choices"][0]["text"].strip()
    return response


async def get_sql_query_with_examples(user_question, activities) -> str:
    examples = get_top_k_matches(user_question)
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=QUERY_WITH_EXAMPLES_PROMPT(activities, user_question, examples).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    response = completion["choices"][0]["text"].strip()
    return response


async def correct_sql_query(user_question, activities, query, error) -> str:
    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=CORRECT_QUERY_ERROR(activities, user_question, query, error).to_str(),
        max_tokens=512,
        temperature=0,
    )
    logging.debug(completion)
    return completion["choices"][0]["text"].strip()
