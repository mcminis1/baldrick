class VALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query, llm_query_plan, data):
        self.activities = activities
        self.llm_query = llm_query
        self.llm_query_plan = llm_query_plan
        self.data = data

    def __str__(self):
        return {
					"blocks": [
						{
							"type": "image",
							"image_url": "https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_880,h_495/v1428917360/gvejybjvt3xw3h1sdmiw.png",
							"alt_text": "Baldrick"
						},
						{
							"type": "header",
							"text": {
								"type": "plain_text",
								"text": "Your Query, My Lord",
								"emoji": true
							}
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*Query:*"
								},
								{
									"type": "mrkdwn",
									"text": f"{self.llm_query}"
								}
							]
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*My Cunning Plan:*"
								},
								{
									"type": "mrkdwn",
									"text": f"{self.llm_query_plan}"
								}
							]
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*Results:*"
								},
								{
									"type": "mrkdwn",
									"text": "None"
								}
							]
						}
					]
				}




    def __repr__(self):
        return str(self)

    def to_str(self) -> str:
        return str(self)


class INVALID_QUERY_RESPONSE:
    def __init__(self, activities, llm_query):
        self.activities = activities
        self.llm_query = llm_query

    def __str__(self):
                return {
					"blocks": [
						{
							"type": "image",
							"image_url": "https://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_880,h_495/v1428917360/gvejybjvt3xw3h1sdmiw.png",
							"alt_text": "Baldrick"
						},
						{
							"type": "header",
							"text": {
								"type": "plain_text",
								"text": "Your Query, My Lord",
								"emoji": true
							}
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*Query:*"
								},
								{
									"type": "mrkdwn",
									"text": f"{self.llm_query}"
								}
							]
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*My Cunning Plan:*"
								},
								{
									"type": "mrkdwn",
									"text": f"{self.llm_query_plan}"
								}
							]
						},
						{
							"type": "section",
							"fields": [
								{
									"type": "mrkdwn",
									"text": "*Results:*"
								},
								{
									"type": "mrkdwn",
									"text": "None"
								}
							]
						}
					]
				}

    def __repr__(self):
        return str(self)

    def to_str(self) -> str:
        return str(self)
