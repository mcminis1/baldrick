import logging
import os
from typing import Optional, Tuple, List
from google.cloud import bigquery

client = bigquery.Client()
project_id = os.environ.get("PROJECT_ID")
dataset = os.environ.get("DATASET")
table = os.environ.get("TABLE")


def get_query_plan(query: str) -> Tuple[Optional[str], Optional[str]]:
    f_query = query.replace("EVENT_SCHEMA", f"`{project_id}.{dataset}.{table}`")
    config = bigquery.QueryJobConfig(
        dry_run=True, priority=bigquery.QueryPriority.BATCH
    )
    try:
        query_job = client.query(f_query, config)
        while query_job.state != "DONE":
            query_job = client.get_job(query_job.job_id, location=query_job.location)
        if query_job.errors is None:
            return "\n".join(query_job.query_plan), None
        else:
            logging.warning(query_job.errors)
            logging.warning(query_job.query_plan)
    except Exception as e:
        logging.error(e)
    return None, query_job.errors


def run_query(query: str) -> Optional[List[str]]:
    f_query = query.replace("EVENT_SCHEMA", f"`{project_id}.{dataset}.{table}`")
    config = bigquery.QueryJobConfig(
        dry_run=False, priority=bigquery.QueryPriority.BATCH
    )
    logging.debug(f_query)
    try:
        query_job = client.query(f_query, config)
        while query_job.state != "DONE":
            query_job = client.get_job(query_job.job_id, location=query_job.location)
        df = query_job.to_dataframe()
        results = []
        for _, row in df.iterrows():
            results.append(row)
        return results
    except Exception as e:
        logging.error(e)
    return None
