import os

top_k = 10

# this should query the schema to get the columns
table_info = """
Table EVENT_SCHEMA {
    activity_id primary key,
    ts TIMESTAMP NOT NULL,
    anon_id STRING,
    customer STRING,
    activity STRING,
    feature_json JSON
}
"""
# this should query the table to get the names
event_names = [
    "Visited Page",
    "Contacted Support",
    "Placed Order",
    "Returned Item",
    "Created Account",
    "Deleted Account",
]

# this should query each event and get the schema available to them
activity_schema = {
    "Visited Page": """Event "Visited Page" {
    URL STRING,
}""",
    "Contacted Support": """Event "Contacted Support" {
    representative STRING,
    notes STRING,
}""",
    "Placed Order": """Event "Placed Order" {
    product STRING,
    price STRING,
}""",
    "Returned Item": """Event "Returned Item" {
    product STRING,
    price STRING,
}""",
    "Created Account": """Event "Created Account" {
    name STRING,
    birthdate TIMESTAMP NOT NULL,
    address STRING,
}""",
    "Deleted Account": """Event "Deleted Account" {
    reason STRING,
}""",
}

project_id = os.environ.get("PROJECT_ID")
dataset = os.environ.get("DATASET")
table = os.environ.get("TABLE")
fully_qualified_table_name = f"`{project_id}.{dataset}.{table}`"


class CORRECT_QUERY_ERROR:
    def __init__(self, activities, user_question, query, error):
        self.activities = activities
        self.user_question = user_question
        self.query = query
        self.error = error
        valid_activity_schema = []
        for key in self.activities:
            if key in activity_schema:
                valid_activity_schema.append(activity_schema.get(key))
        self.valid_activity_schema = "\n".join(valid_activity_schema)

    def __str__(self) -> str:
        return f"""Correct the SQL query below to solve the error.
Only use the following table:
{table_info}
where the activity is one of these strings: {', '.join(self.activities)}
and the JSON schema for each of these activities is:
{self.valid_activity_schema}
        
Double check that your query obeys the following rules.
- You can order the results by a relevant column to return the most interesting examples in the database. 
- Unless the user specifies a specific number of examples, always limit your query to at most {top_k} results using the LIMIT clause.
- When performing aggregations like COUNT, SUM, MAX, MIN, or MEAN rename the column to something descriptive
- Use valid BigQuery syntax
- Use JSON_QUERY(feature_json, '$.json_path') to access fields in the activity JSON.
- Account for possible capitalization in in STRING values by casting them to lower case.
- All queries should be FROM {fully_qualified_table_name}
- If the user wants to limit the time range for the question use CAST(ts as DATE) and CURRENT_DATE() appropriately in the where clause.

Correct the SQL query so that it is syntactically correct SQL for BigQuery, still answers the user question, and eliminates the following error. Provide just the SQL query as your response.
User Question: {self.user_question}
Query: {self.query}
Error: {self.error}
Corrected Query:"""

    def __repr__(self) -> str:
        return str(self)

    def to_str(self) -> str:
        return str(self)


class QUERY_WITH_EXAMPLES_PROMPT:
    def __init__(self, activities, user_question, examples):
        self.activities = activities
        self.user_question = user_question.strip(" \n")
        self.examples = "\n".join(
            "Question: " + p + "\n" + "BigQuery Statement: " + q + "\n"
            for p, q in examples
        )
        valid_activity_schema = []
        for key in self.activities:
            if key in activity_schema:
                valid_activity_schema.append(activity_schema.get(key))
        self.valid_activity_schema = "\n".join(valid_activity_schema)

    def __str__(self) -> str:
        nl = "\n"
        return f"""Given an input question, first create a syntactically correct BigQuery query to run. 
Only use the following table:
{table_info}
where the activity is one of these strings: {', '.join(self.activities)}
and the JSON schema for each of these activities is:
{self.valid_activity_schema}

Double check that your query obeys the following rules.
- You can order the results by a relevant column to return the most interesting examples in the database. 
- Unless the user specifies a specific number of examples, always limit your query to at most {top_k} results using the LIMIT clause.
- When performing aggregations like COUNT, SUM, MAX, MIN, or MEAN rename the column to something descriptive
- Use valid BigQuery syntax
- Use JSON_QUERY(feature_json, '$.json_path') to access fields in the activity JSON.
- Account for possible capitalization in in STRING values by casting them to lower case.
- All queries should be FROM {fully_qualified_table_name}
- If the user wants to limit the time range for the question use CAST(ts as DATE) and CURRENT_DATE() appropriately in the where clause.

Examples:
{ self.examples }

Question: {self.user_question}
BigQuery Statement:"""

    def __repr__(self) -> str:
        return str(self)

    def to_str(self) -> str:
        return str(self)


class EVENT_CHOOSER_PROMPT:
    def __init__(self, user_question):
        self.user_question = user_question

    def __str__(self) -> str:
        return f"""Given the below input question and list of potential events, output a comma separated list of the event names that may be necessary to answer this question.
Question: {self.user_question}
Event Names: {', '.join(event_names)}
Relevant Event Names:"""

    def __repr__(self) -> str:
        return str(self)

    def to_str(self) -> str:
        return str(self)


class QUERY_PLAN_EXPLANATION:
    def __init__(self, user_question, query, answer):
        self.user_question = user_question
        self.query = query
        self.answer = answer

    def __str__(self) -> str:
        return f"""You are a mideval dogsbody tasked with explaining to a modern CEO how the following BigQuery request will answer their business question. If there is a where clause explain it to them in simple terms. Include the answer in your narrative.
BigQuery Statement:
{self.query}
Business Question:
{self.user_question}
Answer:
{self.answer}
Explanation:"""

    def __repr__(self) -> str:
        return str(self)

    def to_str(self) -> str:
        return str(self)
