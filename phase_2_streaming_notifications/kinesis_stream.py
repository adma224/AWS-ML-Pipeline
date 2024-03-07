import boto3
import json
from datetime import datetime
import random

def load_config():
    """Load configuration from config.json."""
    with open('config.json') as f:
        return json.load(f)

def create_kinesis_client(config):
    """Create and return a Kinesis client using credentials from the config."""
    

def create_stream(kinesis_client, stream_name):
    """Create a Kinesis stream if it doesn't already exist."""
    try:
        kinesis_client.create_stream(StreamName=stream_name, ShardCount=1)
        print(f"Stream {stream_name} is being created.")
        kinesis_client.get_waiter('stream_exists').wait(StreamName=stream_name)
        print(f"Stream {stream_name} is now active.")
    except kinesis_client.exceptions.ResourceInUseException:
        print(f"Stream {stream_name} already exists and is active.")

def main():
    config = load_config()
    kinesis_client = boto3.client('kinesis',region_name=config['REGION'],)
    create_stream(kinesis_client, config['KINESIS_STREAM_NAME'])

if __name__ == '__main__':
    main()
