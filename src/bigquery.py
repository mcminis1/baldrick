import logging
import os
from google.cloud import bigquery

client = bigquery.Client()
project_id = os.environ.get("PROJECT_ID")
dataset = os.environ.get("DATASET")
table = os.environ.get("TABLE")

def get_query_plan(query:str) -> str:
    f_query = query.replace('EVENT_SCHEMA', f'`{project_id}.{dataset}.{table}`')
    results = client.query("EXPLAIN " + f_query)
    return str(results)

def run_query(query:str) -> dict:
    f_query = query.replace('EVENT_SCHEMA', f'`{project_id}.{dataset}.{table}`')
    logging.debug(f_query)
    results = client.query(f_query).to_dataframe()
    return results.to_json()