#!/usr/bin/env python
# coding: utf-8


import pandas as pd

# get_ipython().system('uv add tqdm')
# get_ipython().system('uv add sqlalchemy')
# get_ipython().system('uv add psycopg')

from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# df = pd.read_csv(
#     url,
#     dtype=dtype,
#     parse_dates=parse_dates
# )

# df.head()

def run():
    pg_user = 'root'
    pg_password = 'root'
    pg_host = 'localhost'
    pg_database = 'ny_taxi'
    pg_port = 5432

    year = 2021
    month = 1
    
    target_table = 'yellow_taxi_data'
    
    # We cannot take the entire hefty df and insert it into our database. We can read it chunk by chunk.
    
    chunksize=100000
    
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    
    df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=chunksize,
    )
    
    first = True
    
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            # print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
            first = False
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')



if __name__ == '__main__':
    run()