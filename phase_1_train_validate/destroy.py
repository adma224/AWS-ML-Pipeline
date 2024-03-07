import boto3
import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

def delete_s3_bucket_contents(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    print(f"Deleted all contents from bucket {bucket_name}.")

def delete_s3_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Deleted bucket: {bucket_name}")
    except Exception as e:
        print(f"Error deleting S3 bucket {bucket_name}: {e}")

def delete_ecr_repository(repo_name):
    ecr = boto3.client('ecr')
    try:
        ecr.delete_repository(repositoryName=repo_name, force=True)
        print(f"Deleted ECR repository: {repo_name}")
    except Exception as e:
        print(f"Error deleting ECR repository {repo_name}: {e}")

def delete_sagemaker_endpoint(endpoint_name):
    sagemaker = boto3.client('sagemaker')
    try:
        sagemaker.delete_endpoint(EndpointName=endpoint_name)
        print(f"Deleted SageMaker endpoint: {endpoint_name}")
    except Exception as e:
        print(f"Error deleting SageMaker endpoint {endpoint_name}: {e}")

def delete_sagemaker_endpoint_config(endpoint_config_name):
    sagemaker = boto3.client('sagemaker')
    try:
        sagemaker.delete_endpoint_config(EndpointConfigName=endpoint_config_name)
        print(f"Deleted SageMaker endpoint config: {endpoint_config_name}")
    except Exception as e:
        print(f"Error deleting SageMaker endpoint config {endpoint_config_name}: {e}")

def main():
    config = load_config()

    # Delete S3 bucket and contents
    if 's3_bucket_name' in config['RESOURCES']:
        delete_s3_bucket_contents(config['RESOURCES']['s3_bucket_name'])
        delete_s3_bucket(config['RESOURCES']['s3_bucket_name'])

    # Delete ECR repository
    if 'ecr_repository_name' in config['RESOURCES']:
        delete_ecr_repository(config['RESOURCES']['ecr_repository_name'])

    # Delete SageMaker endpoint and config
    if 'sagemaker_endpoint_name' in config['RESOURCES']:
        delete_sagemaker_endpoint(config['RESOURCES']['sagemaker_endpoint_name'])
    if 'sagemaker_endpoint_config_name' in config['RESOURCES']:
        delete_sagemaker_endpoint_config(config['RESOURCES']['sagemaker_endpoint_config_name'])

if __name__ == "__main__":
    main()
