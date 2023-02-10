from datetime import timedelta, date
import json

from faker import Faker
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
        activity STRING,
        feature_json JSON,
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

num_customers = 200
num_products = 30
max_interactions = 100
min_interactions = 5
non_conversion_ids = int(num_customers + 0.33)

# list of products with price
products = {
    fake.color_name()
    + np.random.choice([" Doodad", " Widget", " Thing-a-ma-bob"]): round(
        np.random.uniform(low=10, high=30), 2
    )
    for _ in range(num_products)
}


# list of customers with personal info
customers = {
    fake.email(domain=fake.domain_name()): (
        fake.name(),
        fake.address(),
        date.isoformat(fake.date_of_birth(minimum_age=18, maximum_age=88)),
    )
    for _ in range(num_customers)
}

# list of fictitious webpages
pages = ["/contact", "/home", "/about", "/products"]

# activity stream of customer interactions
cust_acts = list()


def ACTIVITY_HANDLER(activity, cust, ts):

    if activity == "Visited Page":
        feats = json.dumps({"URL": np.random.choice(pages)})
        out = {"activity_id": fake.uuid4(),"ts": ts, "customer": cust, "activity": activity, 'feature_json': feats}
  
    elif activity == "Placed Order":
        prod = np.random.choice(list(products.keys()))
        feats = json.dumps({"product": prod, "price": products[prod]})
        out = {"activity_id": fake.uuid4(), "ts": ts, "customer": cust, "activity": activity, 'feature_json': feats}

        if np.random.choice([True, False], p=[1 / 10, 9 / 10]):
            ret_ts = ts + timedelta(days=np.random.randint(1, 8))

            if ret_ts.date() <= date.today():
                activity = "Returned Item"
                feats = json.dumps({"product": prod, "price": products[prod]})
                out = {"activity_id": fake.uuid4(), "ts": ret_ts, "customer": cust, "activity": activity, 'feature_json': feats}

    else:
        feats = json.dumps({"representative": fake.name(), "notes": fake.paragraph()})
        out = {"activity_id": fake.uuid4(), "ts": ts, "customer": cust, "activity": activity, 'feature_json': feats}

    out['ts'] = date.isoformat(out['ts'])

    return out

activities = ["Visited Page", "Placed Order", "Contacted Support"]

for _ in range(non_conversion_ids):

    anon_id = fake.uuid4()
    
    ts = fake.date_time_this_decade()
    activity = np.random.choice(activities[:2])
    cust_acts.append(ACTIVITY_HANDLER(activity, anon_id, ts))


# Generate DF of randomly generated customer interactions
for cust, info in customers.items():
    anon_id = fake.uuid4()

    ts = fake.date_time_this_decade()
    for _ in range(np.random.randint(low=1, high=5)):
        
        activity = np.random.choice(activities[:2])
        cust_acts.append(ACTIVITY_HANDLER(activity, anon_id, ts))

    init_activity = "Created Account"
    init_features = {"name": info[0], "address": info[1], "birthdate": info[2], 'anon_id': anon_id}

    cust_acts.append(ACTIVITY_HANDLER(init_activity, cust, ts))

    for _ in range(np.random.randint(min_interactions, max_interactions)):
        ts = ts + timedelta(days=np.random.randint(1, 11))
        if ts.date() <= date.today():
            activity = np.random.choice(activities, p=[1 / 2, 1 / 4, 1 / 4])
              
            cust_acts.append(ACTIVITY_HANDLER(activity, cust, ts))



job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    # source_format="NEWLINE_DELIMITED_JSON",
    # schema=[
    #     # Specify the type of columns whose type cannot be auto-detected. For
    #     # example the "title" column uses pandas dtype "object", so its
    #     # data type is ambiguous.
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
