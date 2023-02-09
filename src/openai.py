import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")

top_k = 100
table_info = 

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct BigQuery query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results using the LIMIT clause. You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Use the following format:
Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"
Only use the following tables:
{table_info}
Question: {input}"""

EVENT_CHOOSER = """Given the below input question and list of potential events, output a comma separated list of the event names that may be necessary to answer this question.
Question: {query}
Event Names: {table_names}
Relevant Event Names:"""




def get_llm_query(user_question) -> str:
    return "query string"
