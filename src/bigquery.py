import logging
from typing import Optional, Tuple, Dict, Any
from google.cloud import bigquery

client = bigquery.Client()


def get_query_plan(query: str) -> Tuple[Optional[str], Optional[Dict]]:
    config = bigquery.QueryJobConfig(dry_run=True)
    try:
        logging.debug(f"bq plan for: {query}")
        query_job = client.query(query, config)
        logging.debug(f"bq plan result: {query_job.query_plan}")
        logging.debug(f"bq errors result: {query_job.errors}")
        if query_job.errors is None:
            return "\n".join(query_job.query_plan), None
        else:
            logging.warning(query_job.errors)
            logging.warning(query_job.query_plan)
            return None, query_job.errors
    except Exception as e:
        logging.error(e)
    return None, {"error": "raised exception"}


def run_query(query: str) -> Optional[Dict[str, Any]]:
    config = bigquery.QueryJobConfig(dry_run=False)
    logging.debug(query)
    try:
        query_job = client.query(query, config)
        logging.debug(f"bq plan result: {query_job.query_plan}")
        logging.debug(f"bq errors result: {query_job.errors}")
        results = query_job.to_dataframe().to_dict(orient="records")
        return results
    except Exception as e:
        logging.error(e)
    return None
