


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
uvicorn src.app:api --reload --port 3000 --log-level debug
```

## Deploy to Google Cloud Run

1. [install gcloud](https://cloud.google.com/sdk/docs/install)
2. [quickstart for Python](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)

To deploy from source
```python
gcloud run deploy baldrick --source .
```

Using the Google UI to set up secrets was easiest for us.

Configure secret access:
```bash
gcloud run services update baldrick --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest,SLACK_SIGNING_SECRET=SLACK_SIGNING_SECRET:latest,SLACK_BOT_TOKEN=SLACK_BOT_TOKEN:latest"
```

If you're going to set up CICD with github actions, note that the permissions you actually need differ from the [instructions](https://github.com/google-github-actions/deploy-cloudrun)

You'll need these roles:
- Artifact Registry Administrator
- Cloud Build Editor
- Cloud Run Admin
- Service Account Token Creator
- Service Account User
- Service Usage Consumer
- Storage Admin
- Storage Object Admin
- Workload Identity User 

The easiest way to add them is using the CLI:
- role: roles/artifactregistry.admin
- role: roles/cloudbuild.builds.editor
- role: roles/iam.serviceAccountTokenCreator
- role: roles/iam.serviceAccountUser
- role: roles/iam.workloadIdentityUser
- role: roles/run.admin
- role: roles/serviceusage.serviceUsageConsumer
- role: roles/storage.admin
- role: roles/storage.objectAdmin

```bash
gcloud projects add-iam-policy-binding project_id --member="serviceAccount:account_name@project_id.iam.gserviceaccount.com" --role="roles/this-role"
```
And you'll need to add the service account email to the bucket where the build happens.
