


## Setup

Create an app in a workspace in your [console](https://api.slack.com/apps).


## Install and run

```bash
pip install -r requirements.txt
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
uvicorn src:app --reload --port 3000 --log-level debug
```
