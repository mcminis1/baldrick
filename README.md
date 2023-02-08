


## Setup

Following the [bolt_python quickstart](https://slack.dev/bolt-python/tutorial/getting-started), you'll need to create an app, get your credentials, and set up permissions.

## Local Dev

```bash
pip install -r requirements.txt
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***
uvicorn src:app --reload --port 3000 --log-level debug
```

## Deploy to Google Cloud Run


1. [install gcloud](https://cloud.google.com/sdk/docs/install)
2. [quickstart for Python](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)

To deploy from source
```python
gcloud run deploy baldrick --source .
```
If you have to update the secret/env params
```python
gcloud run services update baldrick --update-secrets=KEY1=VALUE1,KEY2=VALUE2
```

allow access to secrets:
```bash
gcloud run services update baldrick --set-secrets="SLACK_SIGNING_SECRET=SLACK_SIGNING_SECRET:latest,SLACK_BOT_TOKEN=SLACK_BOT_TOKEN:latest"
gcloud run services update baldrick --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest"
```
