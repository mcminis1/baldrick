
## Baldrick

Baldrick is your friends BI chatbot! Currently Baldrick is a Proof-of-Concept.

Current tech stack:
1. Communicates with users via slack.
2. Runs queries on BigQuery.
3. Restricted to querying an [activity schema 2.0](https://github.com/ActivitySchema/ActivitySchema/blob/main/2.0.md).
4. Results and logging are fone on Postgres.
5. OpenAI text-davinci-003 is used to generate SQL.
6. The `sentence-transformers` package is used to compute embeddings.

### How it works

Offline
1. A collection of (business question, SQL query) pairs is collected
2. An embedding is computed for the business questions using an embedding model, ["sentence-transformers/all-mpnet-base-v1"](https://huggingface.co/sentence-transformers/all-mpnet-base-v1).
3. The (embedding, business question, SQL query) triplet is stored in a list.

Online
1. Listens in a slack channel for the slash command `/baldrick {user question}`
2. The user question is parsed out of the slash command and, along with all of the different activity types in our activity Schema, we form a prompt that limits the number of activities we should include in the SQL query. Choosing the activity schema limits complexity due to joins, but does not eliminate the complexity of a varying schema (in JSON for the 2nd version of the activity schema) based on the event.
3. The top 5 most similar business questions are retrieved from our corpus. This is done using the dot product similarity with our corpus.
4. A prompt is formed which queries GPT-3 for a new SQL query. It includes these similar business question, SQL query pairs (up to some constraints on prompt length).
5. That SQL query is tested against bigquery to determine if it errors or runs.
6. [Optional] If step 5 errors, a new prompt is formed with some common reasons these queries fail, the business problem, SQL query, and error. That is then sent to GPT-3 for a single retry.
7. The query is run and results are returned.
8. The business problem, query plan, SQL, and data are used in another prompt which is sent to GPT-3 for a "human readable" explanation of how the query was done and what the results are.

### Todo

Some items that could be on the road map depending on interest:
- Auto-infer the schema.
- Generalize to Snowflake and Redshift.
- Add support for Discord.
- Automatically index (business question, SQL queries) as examples when users approve them.
- Load initial examples into postgres instead of loading from csv.
- Schema migration layer for SQL queries.
- Support for Cohere and AI21 LLMs.
- Refine ambiguous queries with dialogue.
- Use postgres vector store for embedding queries + KNN search.

If you are interested in extending the functionality, or want to use it for something, please reach out to the maintainers.

## Setup

There is a fair amount of setup to get this running. You need: a slack app, a google project and bigquery, a postgres db, and an OpenAI API account key.

Following the [bolt_python quickstart](https://slack.dev/bolt-python/tutorial/getting-started), you'll need to create an app, get your credentials, and set up permissions.

You'll need to set up an OpenAI account and generate an API key.

You'll need a postgres db (though it would be easy to generalize to another db). You will also need to edit the alembic.ini file so the username/password/host are all right for your db.

You'll need to use `gcloud` to set up credentials and your project for BigQuery. The initial steps in the following section go over this part.

You should then be able to spin up a local server.
```bash
pip install -r requirements.txt

export SLACK_BOT_TOKEN=
export SLACK_SIGNING_SECRET=
export DB_DATABASE=
export DB_USER=
export DB_HOST=
export DB_PASSWORD=
export OPENAI_API_KEY=
uvicorn --port 8080 --host 0.0.0.0 --reload src.app:api 
```

If you're using localhost to serve a db, then request verification is turned off. You can use the curl_service.sh script to test if things are working end to end. You should see entries made in your database table when things are all set up correctly.

## Deploy to Google Cloud Run

If you choose to use GCP for this here is some getting started help. You can look at the github action to see some of the env params and VM settings we needed to use.

1. [install gcloud](https://cloud.google.com/sdk/docs/install)
2. [quickstart for Python](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)

You'll need to set up networking as well. This [tutorial](https://codelabs.developers.google.com/connecting-to-private-cloudsql-from-cloud-run) has the essentials for connecting cloud run to cloud sql using a private IP address and VPC peering.

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
