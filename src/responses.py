
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
    def to_str(self) -> str:
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
    def to_str(self) -> str:
        return str(self)
