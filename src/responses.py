import json


class VALID_QUERY_RESPONSE:
    def __init__(self, user_question, llm_query, llm_query_plan, data, session_id):
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.data = data
        self.user_question = user_question
        self.session_id = session_id

    def _create_result_blocks(self):
        bq_return_value = json.dumps(
            {
                "question": self.user_question,
                "query": self.llm_query,
                "session_id": self.session_id,
            }
        )

        results = [
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
            {"type": "header", "text": {"type": "plain_text", "text": "Results:"}},
            {"type": "divider"},
        ]

        for row in self.data:
            fields = []
            for k, v in row.items():
                k_col = {"type": "mrkdwn", "text": "*" + str(k) + "*"}
                v_col = {"type": "mrkdwn", "text": str(v).strip('"')}
                fields.extend([k_col, v_col])

            results.append({"type": "section", "fields": fields})

        results.extend(
            [
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
                        "value": bq_return_value,
                        "action_id": "view_bigqeury",
                    },
                },
            ]
        )

        return results

    def get_json(self):
        return {"response_type": "in_channel", "blocks": self._create_result_blocks()}


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
                    "text": {"type": "plain_text", "text": "Right, 'ere ya go..."},
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*BigQuery Statement*"},
                        {"type": "mrkdwn", "text": f"{self.llm_query}"},
                    ],
                },
            ],
        }
