import data_utils
import random
import json
import boto3
from datetime import datetime
import time

def put_data_into_stream(kinesis_client, stream_name, payload):
    """Put a data record into the Kinesis stream."""

    data = {
        'value': payload,
        'timestamp': str(datetime.utcnow())
    }
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey="partitionKey"
    )
    print(f"Put record to {stream_name}: {response}")

def main():
    config = data_utils.load_config()
    kinesis_client = boto3.client('kinesis')
    print("Press Ctrl+C to interrupt...")
    try:
        while True:
            payload = data_utils.fetch_random_users(random.randint(1, 10))
            put_data_into_stream(kinesis_client, config['KINESIS_STREAM_NAME'], payload)
            time.sleep(random.randint(1, 5))
    except KeyboardInterrupt:
        print("Program interrupted by the user. Cleaning up...")
        # Place any necessary cleanup code here
        # For example, closing files, releasing resources, etc.
    finally:
        print("Goodbye!")

if __name__ == "__main__":
    main()