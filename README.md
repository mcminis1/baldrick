


## Setup

Following the [bolt_python quickstart](https://slack.dev/bolt-python/tutorial/getting-started), you'll need to create an app, get your credentials, and set up permissions.

## App Manifest

```yaml
display_information:
  name: baldrick
  description: Your SQL dogsbody
  background_color: "#474e66"
features:
  bot_user:
    display_name: baldrick
    always_online: true
  slash_commands:
    - command: /baldrick
      url: https://{{ your host }}/slack/events
      description: ask baldrick a question
      usage_hint: ask baldrick to query your data warehouse for an answer
      should_escape: true
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - channels:history
      - chat:write
      - commands
      - mpim:history
settings:
  event_subscriptions:
    request_url: https://{{ your host }}/slack/events
    bot_events:
      - app_mention
      - message.channels
      - message.mpim
  interactivity:
    is_enabled: true
    request_url: https://{{ your host }}/slack/events
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```


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
gcloud run services update baldrick --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest,SLACK_SIGNING_SECRET=SLACK_SIGNING_SECRET:latest,SLACK_BOT_TOKEN=SLACK_BOT_TOKEN:latest"
```
