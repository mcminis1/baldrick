class VALID_QUERY_RESPONSE:
    def __init__(self, user_question, llm_query, llm_query_plan, data):
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.data = data
        self.user_question = user_question

    def get_json(self):
        return {
            "response_type": "in_channel",
            "blocks": [
                {
                    "type": "image",
                    "image_url": "https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_880,h_495/v1428917360/gvejybjvt3xw3h1sdmiw.png",
                    "alt_text": "Baldrick",
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Your Query, My Lord",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Your Question:*"},
                        {"type": "mrkdwn", "text": f"{self.user_question}"},
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Query:*"},
                        {"type": "mrkdwn", "text": f"{self.llm_query}"},
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*My Cunning Plan:*"},
                        {"type": "mrkdwn", "text": f"{self.llm_query_plan}"},
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Results:*"},
                        {"type": "mrkdwn", "text": f"{self.data}"},
                    ],
                },
            ]
        }


class INVALID_QUERY_RESPONSE:
    def __init__(self, user_question, llm_query):
        self.llm_query = llm_query
        self.user_question = user_question

    def get_json(self):
        return {
            "response_type": "in_channel",
            "blocks": [
                {
                    "type": "image",
                    "image_url": "https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_880,h_495/v1428917360/gvejybjvt3xw3h1sdmiw.png",
                    "alt_text": "Baldrick",
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Your Query, My Lord",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Your Question:*"},
                        {"type": "mrkdwn", "text": f"{self.user_question}"},
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Query:*"},
                        {"type": "mrkdwn", "text": f"{self.llm_query}"},
                    ],
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*My Cunning Plan:*"},
                        {
                            "type": "mrkdwn",
                            "text": "Is a turnip! Can you ask me a different way?",
                        },
                    ],
                },
            ]
        }
