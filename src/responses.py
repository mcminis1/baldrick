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
                    "image_url": "https://mcminis1.github.io/img/baldrick/baldrick_grouse_sm.png",
                    "alt_text": "Baldrick",
                },
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Your Query, M'Lord"},
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*You asked me:*"},
                        {"type": "mrkdwn", "text": f"{self.user_question}"},
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
                        {"type": "mrkdwn", "text": "\n".join([x for x in self.data])},
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Are you satisfied M'Lord?*"},
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Verily",
                                "emoji": True,
                            },
                            "style": "primary",
                            "value": "True",
                            "action_id": "results_approved",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Nay",
                                "emoji": True,
                            },
                            "style": "danger",
                            "value": "False",
                            "action_id": "results_rejected",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Care to view the BigQuery statement?*",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Indeed", "emoji": True},
                        "value": f"{self.llm_query}",
                        "action_id": "view_bigqeury",
                    },
                },
            ],
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
                    "image_url": "https://mcminis1.github.io/img/baldrick/baldrick_grouse_sm.png",
                    "alt_text": "Baldrick",
                },
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Your Query, M'Lord"},
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*You asked me:*"},
                        {"type": "mrkdwn", "text": f"{self.user_question}"},
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
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "new_query-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Your question but better...",
                        "emoji": True,
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Submit",
                                "emoji": True,
                            },
                            "style": "primary",
                            "value": "None",
                            "action_id": "Submit_new_query",
                        }
                    ],
                },
            ],
        }

class RETURN_BQ_STATEMENT:
    def __init__(self, llm_query):
        self.llm_query = llm_query

    def get_json(self):
        return {
            "response_type": "in_channel",
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Right, 'ere ya go..."}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text":"*BigQuery Statement*"},
                        {"type": "mrkdwn", "text": f"{self.llm_query}"}
                    ]
                }
            ]
        }
