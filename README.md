# Build Real Time Data Pipeline using AWS Kinesis and Snowflake

## Project Description
This project focuses on building a real-time data pipeline to analyze global food market data.Leveraging AWS services such as Kinesis, S3, App Runner, and Lambda, along with Snowflake for data storage and processing, the pipeline enables continuous ingestion, transformation, and analysis of live streaming data. Power BI is used to create dynamic dashboards that visualize key trends and patterns, supporting timely and data-driven decision-making. 

## Business Overview 
The management of global food market system involves several stakeholders such as organizations, vendors, regulatory authorities and retailers.Since the food market data can gain significant value over time due to ivolve of operating system & conditions and frequent fluctuations of economic conditions, the information carrried by this type of data is often time-critical allowing only a limited time window to make preventive and predictive actions and effectively implement them. In contrast, reactive data, typically historical and processsed in batch are more suitable for development in buisness intelligence and stratergies. Having a unified platform to analyze real-time data allow stakeholders to manage inquiries and prioritize the decisions that are made using this time-critical information,regardless of the variability and volume of incoming trend. 

## Data 
The global food market data used in this project consisted of data collected from 36 countries across different market for various food items from year 2007 until 2023. The data includes estimated open, close, high and low prices for each food item, as well as inflation rate and trust score (1-10) which refelects the reliability of inflation calculation for each item. After preprocessing and transforming the raw dataset,the segement of [Data for 2007](Data/2007_s3_snowflake_realtime.csv) shows how cleaned dataset looks before analysis.

## Fetching Data using FastAPI
The streaming data market analysis could oriinate from external APIs such as Apache Kafka, server logs or stand- alone applications. For the demonstration in this project, previously streamed data is been stored in a AWS S3 bucket as pre-existing data. The data, whether in real time or pre-existing in the storage bucket is accessed through FastAPI application, which is a modern web framework for building HTTP-based service APIs. The API was deployed using AWS ApppRunner and the S3 bucket was integrated with the FastAPI service to expose the pre-existing data objects as accessible API endpoints.

## Project Architecture 
![reference diagram](Images/reference_architecture.png)
As shown in the reference architecture:
1. Previously streamed data is stored in AWS s3 storage bucket for the use in building the data pipeline and data stored objects are exposed to API endpoint.
2. The FastAPI code created to build the API application is saved in github repository and deployed in AWS AppRunner as a github action.
3. The datafetched through FastAPI is streamed into AWS Kinesis Data Stream.
4. AWS Kinesis  firehose is use to ingest and load the streaming data into the destination which is seperate S3 storage bucket.
5. AWS lambda is use to create an Lambda function to transforms real-time logs into CSV format before delivering the data to final destination, acting as a junction to streamline live data received from the API.
6. Use a snowpipe to automate the data ingestion to snowflake from external sources,s3 storage bucket where transformed data is stored.
7. Snowpark within snowflake is used for pre-processing and transformation of data.
8. The transformed and cleaned data, along with row count information, is logged and saved as separate tables in Snowflake, executed using SnowSQL scripts.
9. PowerBI uilizes the snowflake database connection to retrieve cleaned and prepared data to create visualizations for insightful analysis and informed decision making.

### 1. Build and Deploy FastAPI Application via AWS AppRunner 
 **I.** When building the FastAPI application and defining the endpoint to fetch data, the URL path used in this project is for s3 storage bucket with pre-existing data as shown below.
```python
app = FastAPI()

def fetch_data(year: int = None, country: str = None, market: str = None):
 
        # Load CSV content into a pandas DataFrame
        df = pd.read_csv("https://real-time-market-data.s3.us-east-1.amazonaws.com/total_data.csv")
 return {"message": "Welcome! Use /fetch_data endpoint with query parameters."}
```
Completed [application code](app.py) and [requirement files](requirements.txt) can be accessed in the root directory of this repository.

 **II.** When streaming real-time data from external API such as apache kafka, the  URL path can be used for Kafka consumer to get connect with kafka as shown below:
```python
from fastapi import FastAPI
from kafka import KafkaConsumer

app = FastAPI()

@app.get("/kafka-data")
def get_kafka_data():
    consumer = KafkaConsumer(
        'your_topic',
        bootstrap_servers='localhost:9092',  
        auto_offset_reset='latest',
        group_id='my-group'
    )
    for message in consumer:
        return {"data": message.value.decode()}
```
  **III.** The port `8080` and host `'0.0.0.0'` are used allowing server to accept requests from any IP adress.
```python
uvicorn.run(app, host='0.0.0.0', port=8080)
```
**IV.** AWS App Runner which is a fully managed service is used to create and deploy a new service by configuring build settings, specifying the port, linking to a GitHub repository, and defining build and start commands to launch the FastAPI application.

### 2. AWS Kinesis Data Stream 

Amazon Kinesis enables seamless collection, processing, and analysis of real-time streaming data to deliver instant insights and support rapid responses to new information.Unlike traditional methods that require complete data collection before processing, Kinesis allows you to analyze and act on data the moment it arrives.Kinesis Data Stream collects and store data streams for analysis. The data fetched through FastAPI is sent to Kinesis Data Stream by creating a kinesis client using the AWS SDK(boto3).
```python

kinesis_client = boto3.client('kinesis', region_name='us-east-1', aws_access_key_id='',
     aws_secret_access_key='')
```
The [completed code for fetching data from API](Installation & Execution codes/Fetch_data_from_API_vidishai.ipynb) demonstrates how data is retrieved by inivoking API  with configured parameters for the year 2007 and then streamed to the Kinesis Data Stream.

### 3. AWS Kinesis Data Firehose 

Amazon Kinesis Data Firehose is a fully managed service that automatically delivers real-time streaming data to destinations like Amazon S3 and Amazon Redshift.













