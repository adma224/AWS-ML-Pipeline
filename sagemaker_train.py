import boto3
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
import random
import json
from io import StringIO
import data_utils
from data_utils import load_config, save_config, fetch_random_users

def create_s3_bucket(config):
    s3 = boto3.client('s3', region_name=config["REGION"])
    bucket_name = f"{config['PROJECT_NAME']}-{random.randint(1000, 9999)}"
    try:
        if config["REGION"] == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': config["REGION"]})
        print(f"Bucket {bucket_name} created successfully.")
        return bucket_name
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return None

def upload_dataframe_to_s3(df, bucket_name, object_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, object_name).put(Body=csv_buffer.getvalue())
    print(f"{object_name} uploaded to S3 bucket {bucket_name}.")

def split_and_upload_data(df, bucket_name):
    train_data, test_data = train_test_split(df, test_size=0.2)
    upload_dataframe_to_s3(train_data, bucket_name, 'train/train_data.csv')
    upload_dataframe_to_s3(test_data, bucket_name, 'test/test_data.csv')

def main():
    config = load_config()
    bucket_name = create_s3_bucket(config)
    
    if bucket_name:
        config["RESOURCES"]["s3_bucket_name"] = bucket_name
        save_config(config)
        
        sample_size = config["SAMPLE_SIZE"]
        users_data = fetch_random_users(sample_size)
        users_df = pd.json_normalize(users_data)
        
        # Simplify DataFrame to include necessary columns for training
        # This step depends on your model's needs
        users_df = users_df[['gender', 'dob.age']]
        
        # Split and upload data to S3
        split_and_upload_data(users_df, bucket_name)
        
        # Update config.json with S3 data paths
        config["RESOURCES"]["s3_train_data"] = f"s3://{bucket_name}/train/train_data.csv"
        config["RESOURCES"]["s3_test_data"] = f"s3://{bucket_name}/test/test_data.csv"
        save_config(config)
        
        # Additional SageMaker training logic goes here
        # Remember to update config.json with model artifact URLs after training

if __name__ == '__main__':
    main()
