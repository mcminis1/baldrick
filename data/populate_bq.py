from datetime import timedelta, date, datetime
import json

from faker import Faker

import faker_commerce
import numpy as np

from google.cloud import bigquery

client = bigquery.Client()

dataset_id = "baldrick.doodad_inc"
table_id = dataset_id + ".customer_stream_new"

query = f"""
    CREATE TABLE IF NOT EXISTS {table_id}
    (
        activity_id STRING NOT NULL,
        ts TIMESTAMP NOT NULL,
        customer STRING,
        anon_id STRING,
        activity STRING,
        feature_json STRING,
    )
    PARTITION BY TIMESTAMP_TRUNC(ts, MONTH)
    CLUSTER BY customer
    OPTIONS (
        description="an activity stream of customer interaction"
    );
"""
job = client.query(query)
job.result()

Faker.seed(1334)
fake = Faker()
fake.add_provider(faker_commerce.Provider)

num_customers = 400
num_products = 30
max_interactions = 400
min_interactions = 5

# list of products with price
products = {fake.ecommerce_name(): fake.ecommerce_price() for _ in range(num_products)}


# list of customers with personal info
customers = [
    {"name": fake.email(domain=fake.domain_name()), "anon_id": fake.uuid4()}
    for _ in range(num_customers)
]

# activity stream of customer interactions
cust_acts = list()


def ACTIVITY_HANDLER(activity, name, anon_id, ts):
    if activity == "Visited Page":
        feats = json.dumps({"URL": fake.uri_path()})
        out = {
            "activity_id": fake.uuid4(),
            "ts": ts,
            "anon_id": anon_id,
            "customer": name,
            "activity": activity,
            "feature_json": feats,
        }

    elif activity == "Placed Order":
        prod = np.random.choice(list(products.keys()))
        feats = json.dumps({"product": prod, "price": products[prod]})
        out = {
            "activity_id": fake.uuid4(),
            "ts": ts,
            "anon_id": anon_id,
            "customer": name,
            "activity": activity,
            "feature_json": feats,
        }

        if np.random.choice([True, False], p=[1 / 10, 9 / 10]):
            ret_ts = ts + timedelta(days=np.random.randint(1, 8))

            if ret_ts.date() <= date.today():
                activity = "Returned Item"
                feats = json.dumps({"product": prod, "price": products[prod]})
                out = {
                    "activity_id": fake.uuid4(),
                    "ts": ret_ts,
                    "anon_id": anon_id,
                    "customer": name,
                    "activity": activity,
                    "feature_json": feats,
                }

    elif activity == "Contected Support":
        feats = json.dumps({"representative": fake.name_nonbinary(), "notes": fake.paragraph()})
        out = {
            "activity_id": fake.uuid4(),
            "ts": ts,
            "anon_id": anon_id,
            "customer": name,
            "activity": activity,
            "feature_json": feats,
        }

    else:
        reasons = [None, 
                    'Unsatisfied with product', 
                    'Unsatisfied with support',
                    'Will nnot order again',
                    'Do not want an account']

        feats = json.dumps({"reason": np.random.choice(reasons)})
        out = {
            "activity_id": fake.uuid4(),
            "ts": ts,
            "anon_id": anon_id,
            "customer": name,
            "activity": activity,
            "feature_json": feats,
        }

    out["ts"] = datetime.isoformat(out["ts"])

    return out


activities = ["Visited Page", "Placed Order", "Contacted Support", 'Deleted Account']

# Generate DF of randomly generated customer interactions
for cust in customers:
    ts = fake.date_time_this_year()
    for _ in range(np.random.randint(low=1, high=5)):
        activity = np.random.choice(activities[:2])
        cust_acts.append(ACTIVITY_HANDLER(activity, cust['anon_id'], None, ts))

    init_activity = "Created Account"
    init_features = {
        "name": fake.name(),
        "address": fake.address(),
        "birthdate": date.isoformat(fake.date_of_birth(minimum_age=18, maximum_age=88)),
    }

    cust_acts.append(ACTIVITY_HANDLER(init_activity, cust['name'], cust['anon_id'], ts))

    for _ in range(np.random.randint(min_interactions, max_interactions)):
        ts = ts + timedelta(days=np.random.randint(1, 11))
        if ts.date() <= date.today():
            activity = np.random.choice(activities, p=[1 / 2, 1 / 5, 1 / 5, 1 / 10])

            if activity == activities[-1]:
                cust_acts.append(ACTIVITY_HANDLER(activity, cust['name'], cust['anon_id'], ts))
                break
            else:
                cust_acts.append(ACTIVITY_HANDLER(activity, cust['name'], cust['anon_id'], ts))

non_conversion_ids = np.random.randint(low=num_customers, high=10 * num_customers)
for _ in range(non_conversion_ids):
    anon_id = fake.uuid4()
    ts = fake.date_time_this_year()
    for _ in range(np.random.randint(min_interactions, max_interactions)):
        ts = ts + timedelta(days=np.random.randint(1, 11))
        if ts.date() <= date.today():
            activity = np.random.choice(activities[:2])
            cust_acts.append(
                ACTIVITY_HANDLER(activity, None, cust['anon_id'], ts)
            )



job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    # source_format="NEWLINE_DELIMITED_JSON",
    # schema=[
    #     # Specify the type of columns whose type cannot be auto-detected. For
    #     # example the "title" column uses pandas dtype "object", so its
    #     # data type is ambiguous.
    #     bigquery.SchemaField("activity_id", bigquery.enums.SqlTypeNames.STRING),
    #     bigquery.SchemaField("ts", bigquery.enums.SqlTypeNames.TIMESTAMP),
    #     bigquery.SchemaField("customer", bigquery.enums.SqlTypeNames.STRING),
    #     bigquery.SchemaField("anon_id", bigquery.enums.SqlTypeNames.STRING),
    #     bigquery.SchemaField("activity", bigquery.enums.SqlTypeNames.STRING),
    #     bigquery.SchemaField("feature_json", bigquery.enums.SqlTypeNames.STRING)
    # ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
)

# Populate table from pandas DF
job = client.load_table_from_json(cust_acts, table_id, job_config=job_config)
job.result()

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
