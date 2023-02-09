import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

top_k = 100

# this should query the schema to get the columns
table_info = """
Table EVENT_SCHEMA {
    activity_id primary key,
    ts TIMESTAMP NOT NULL,
    customer STRING,
    activity STRING,
    feature_json JSON
}
"""
# this should query the table to get the names
event_names = []
# this should query each event and get the schema available to them
activity_schema = {}


class QUERY_PROMPT:
    def __init__(self, top_k, table_info, activities, activity_schema, user_question):
        self.top_k = top_k
        self.table_info = table_info
        self.activities = activities
        self.activity_schema = activity_schema
        self.user_question = user_question

    def __str__(self) -> str:
        return """Given an input question, first create a syntactically correct BigQuery query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {self.top_k} results using the LIMIT clause. You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Use the following format:
Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"
Only use the following table:
{self.table_info}
where the activity is one of {self.activities}
and the activity schemas are:
{self.activity_schema}
Question: {self.user_question.strip(' \n')}"""

    def __repr__(self) -> str:
        return str(self)

    def to_str(self) -> str:
        return str(self)


class EVENT_CHOOSER_PROMPT:
    def __init__(self, user_question, event_names):
        self.user_question = user_question
        self.event_names = event_names

    def __str__(self) -> str:
        return """Given the below input question and list of potential events, output a comma separated list of the event names that may be necessary to answer this question.
Question: {self.user_question}
Event Names: {', '.join(self.event_names)}
Relevant Event Names:"""

    def __repr__(self) -> str:
        return str(self)
    
    def to_str(self) -> str:
        return str(self)


async def get_relevant_activities(user_question) -> str:
    completion = await openai.Completion.create(
        engine="text-davinci-003",
        prompt=EVENT_CHOOSER_PROMPT(user_question, event_names).to_str(),
    )
    return completion


async def get_sql_query(user_question, activities) -> str:
    completion = await openai.Completion.create(
        engine="text-davinci-003",
        prompt=QUERY_PROMPT(
            top_k, table_info, activities, activity_schema, user_question
        ).to_str(),
    )
    # need to parse the output according to the prompt and return multiple parts
    # e.g. (SQLQuery, SQLResult, Answer) from the QUERY_PROMPT
    return completion
