#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'


# In[3]:


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

df = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[4]:


df.head()


# In[8]:


get_ipython().system('uv add sqlalchemy')


# In[1]:


get_ipython().system('uv add psycopg')


# In[5]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[6]:


df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[7]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[8]:


len(df)


# In[9]:


## We cannot take the entire hefty df and insert it into our database. We can read it chunk by chunk.


# In[10]:


df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)


# In[11]:


get_ipython().system('uv add tqdm')


# In[12]:


from tqdm.auto import tqdm


# In[15]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




