from datetime import timedelta, date
import argparse

from faker import Faker
import numpy as np
import pandas as pd

from google.cloud import bigquery

client = bigquery.Client()

dataset_id = "baldrick.doodad_inc"
table_id = dataset_id + ".customer_stream"

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

# list of products with price
products = {
    fake.color_name()
    + np.random.choice([" Doodad", " Widget", " Thing-a-ma-bob"]): round(
        np.random.uniform(low=10, high=30), 2
    )
    for _ in range(30)
}

# list of customers with personal info
customers = {
    fake.email(): (
        fake.name(),
        fake.address(),
        fake.date_of_birth(minimum_age=18, maximum_age=88),
    )
    for _ in range(200)
}

# list of fictitious webpages
pages = ["/contact", "/home", "/about", "/products"]

# activity stream of customer interactions
cust_act_df = pd.DataFrame(columns=["ts", "customer", "activity", "feature_json"])

# Generate DF of randomly generated customer interactions
for cust, info in customers.items():
    activities = ["Visited Page", "Placed Order", "Contacted Support"]

    ts = fake.date_time_this_decade()
    init_activity = "Created Account"
    init_features = {"name": info[0], "address": info[1], "birthdate": info[2]}

    temp_df = pd.DataFrame(
        {"ts": ts, "customer": cust, "activity": init_activity}, index=pd.RangeIndex(1)
    )
    temp_df["feature_json"] = [init_features]
    cust_act_df = pd.concat([cust_act_df, temp_df], ignore_index=True)

    for _ in range(np.random.randint(5, 100)):
        ts = ts + timedelta(days=np.random.randint(1, 11))
        if ts.date() <= date.today():
            activity = np.random.choice(activities, p=[1 / 2, 1 / 4, 1 / 4])

            if activity == "Visited Page":
                feats = {"URL": np.random.choice(pages)}
                temp_df = pd.DataFrame(
                    {"ts": ts, "customer": cust, "activity": activity},
                    index=pd.RangeIndex(1),
                )
                temp_df["feature_json"] = [feats]
                cust_act_df = pd.concat([cust_act_df, temp_df], ignore_index=True)

            elif activity == "Placed Order":
                prod = np.random.choice(list(products.keys()))
                feats = {"product": prod, "price": products[prod]}
                temp_df = pd.DataFrame(
                    {"ts": ts, "customer": cust, "activity": activity},
                    index=pd.RangeIndex(1),
                )
                temp_df["feature_json"] = [feats]
                cust_act_df = pd.concat([cust_act_df, temp_df], ignore_index=True)

                if np.random.choice([True, False], p=[1 / 10, 9 / 10]):
                    ret_ts = ts + timedelta(days=np.random.randint(1, 8))

                    if ret_ts.date() <= date.today():
                        activity = "Returned Item"
                        feats = {"product": prod, "price": products[prod]}
                        temp_df = pd.DataFrame(
                            {"ts": ts, "customer": cust, "activity": activity},
                            index=pd.RangeIndex(1),
                        )
                        temp_df["feature_json"] = [feats]
                        cust_act_df = pd.concat(
                            [cust_act_df, temp_df], ignore_index=True
                        )
            else:
                feats = {"representative": fake.name(), "notes": fake.paragraph()}
                temp_df = pd.DataFrame(
                    {"ts": ts, "customer": cust, "activity": activity},
                    index=pd.RangeIndex(1),
                )
                temp_df["feature_json"] = [feats]
                cust_act_df = pd.concat([cust_act_df, temp_df], ignore_index=True)

# Sort data by time and reset index to get an ordered activity_id
final_df = (
    cust_act_df.sort_values(by="ts")
    .reset_index(drop=True)
    .reset_index()
    .rename(columns={"index": "activity_id"})
    .astype({"activity_id": str, "feature_json": str})
)


job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    schema=[
        # Specify the type of columns whose type cannot be auto-detected. For
        # example the "title" column uses pandas dtype "object", so its
        # data type is ambiguous.
        bigquery.SchemaField("feature_json", bigquery.enums.SqlTypeNames.STRING)
    ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
)

# Populate table from pandas DF
job = client.load_table_from_dataframe(final_df, table_id, job_config=job_config)
job.result()

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
