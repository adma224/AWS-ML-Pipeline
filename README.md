# AWS Real-Time Data Processing and Analytics Platform
This repository contains a collection of Boto3 scripts for deploying a serverless AWS architecture designed to ingest, process, analyze, and visualize data in real-time. The platform leverages AWS services such as Amazon Kinesis for data streaming, AWS Lambda for event-driven data processing, Amazon S3 for data storage, and Amazon QuickSight for data visualization. Additionally, it integrates Amazon SageMaker for implementing and deploying machine learning models like KMeans and Random Cut Forest (RCF) for data enrichment and anomaly detection.

### Features
- **Data Ingestion:** Scripts to set up and configure Amazon Kinesis Data Streams for real-time data ingestion.
- **Data Processing:** Lambda functions automated to process streams and perform real-time analytics, orchestrated by Boto3.
- **Data Storage:** S3 bucket configuration for storing processed data.
- **Machine Learning:** Integration of SageMaker models for advanced data analytics.
- **Visualization:** Set up of Athena for querying processed data and QuickSight dashboards for visual insights.
- **Notifications:** Amazon SNS setup for alerting based on specific data patterns or anomalies.

### Architecture Overview
The platform is designed with security and efficiency in mind, utilizing a mix of public and private subnets within an Amazon VPC, AWS PrivateLink for secure AWS service connectivity, and IAM roles for fine-grained access control.

This project is ideal for demonstrating a serverless approach to real-time data processing and analytics on AWS, showcasing technical expertise in cloud architecture, automation with Boto3, and machine learning model deployment.
