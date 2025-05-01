# Build Real Time Data Pipeline using AWS Kinesis and Snowflake

## Project Description
This project focuses on building a real-time data pipeline to analyze global food market data.Leveraging AWS services such as Kinesis, S3, App Runner, and Lambda, along with Snowflake for data storage and processing, the pipeline enables continuous ingestion, transformation, and analysis of live streaming data. Power BI is used to create dynamic dashboards that visualize key trends and patterns, supporting timely and data-driven decision-making. 

## Data 
The global food market data used in this project consisted of data collected from 36 countries across different market for various food items from year 2007 until 2023. The data includes estimated open, close, high and low prices for each food item, as well as inflation rate and trust score (1-10) which refelects the reliability of inflation calculation for each item. After preprocessing and transforming the raw dataset,the segement of [Data for 2007](Data\2007_s3_snowflake_realtime.csv) shows how cleaned dataset looks before analysis.

## Fetching Data using FastAPI
The streaming data market analysis could oriinate from external APIs such as Apache Kafka, server logs or stand- alone applications. For the demonstration in this project, previously streamed data is been stored in a AWS S3 bucket as pre-existing data. The data, whether in real time or pre-existing in the storage bucket is accessed through FastAPI application, which is a modern web framework for building HTTP-based service APIs. The API was deployed using AWS ApppRunner and the S3 bucket was integrated with the FastAPI service to expose the pre-existing data objects as accessible API endpoints.

##
