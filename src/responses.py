class VALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query, llm_query_plan, data):
        self.activities = activities
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.data = data

    def __str__(self):
        return f" activities:\n {self.activities}\n\n query:\n {self.llm_query}\n\n query plan:\n {self.llm_query_plan}\n\n results: {self.data}"

    def __repr__(self):
        return str(self)

    def to_str(self) -> str:
        return str(self)


class INVALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query):
        self.activities = activities
        self.llm_query = llm_query

    def __str__(self):
        return f" activities:\n {self.activities}\n\n query:\n {self.llm_query}\n\n query plan is invalid\n"

    def __repr__(self):
        return str(self)

    def to_str(self) -> str:
        return str(self)
