import boto3
import subprocess
import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def create_ecr_repository(repo_name, config):
    ecr = boto3.client('ecr', region_name=config['REGION'])
    try:
        response = ecr.create_repository(repositoryName=repo_name)
        repositoryUri = response['repository']['repositoryUri']
        print(f"Repository {repo_name} created: {repositoryUri}")
        return repositoryUri
    except ecr.exceptions.RepositoryAlreadyExistsException:
        print(f"Repository {repo_name} already exists.")
        response = ecr.describe_repositories(repositoryNames=[repo_name])
        return response['repositories'][0]['repositoryUri']

def build_and_push_docker_image(repo_uri, model_artifact):
    # Example command, adjust as needed
    docker_build_command = f"docker build -t {repo_uri} ."
    docker_push_command = f"docker push {repo_uri}"
    
    try:
        subprocess.run(docker_build_command, check=True, shell=True)
        subprocess.run(docker_push_command, check=True, shell=True)
        print(f"Image {repo_uri} built and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building or pushing Docker image: {e}")

def deploy_sagemaker_endpoint(sagemaker_client, model_name, repo_uri, config):
    # Assume container definition and SageMaker role are set
    container = {'Image': repo_uri}
    execution_role_arn = "YourSageMakerRoleArn"  # Replace with your actual ARN
    
    # Create model in SageMaker
    create_model_response = sagemaker_client.create_model(
        ModelName=model_name,
        PrimaryContainer=container,
        ExecutionRoleArn=execution_role_arn,
    )
    
    # Create endpoint configuration
    endpoint_config_name = f"{model_name}-config"
    sagemaker_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[{
            'VariantName': 'AllTraffic',
            'ModelName': model_name,
            'InitialInstanceCount': 1,
            'InstanceType': 'ml.t2.medium',
            'InitialVariantWeight': 1
        }]
    )
    
    # Create endpoint
    endpoint_name = f"{model_name}-endpoint"
    sagemaker_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )
    print(f"Endpoint {endpoint_name} creation in progress...")

def main():
    config = load_config()
    repo_name = f"{config['PROJECT_NAME']}-repo"
    
    # ECR Repository
    repo_uri = create_ecr_repository(repo_name, config)
    
    # Assuming model artifacts URL is in config (adjust as needed)
    model_artifact_url = config['RESOURCES']['model_artifact_urls']['kmeans']  # Example for KMeans
    
    # Build and Push Docker Image
    build_and_push_docker_image(repo_uri, model_artifact_url)
    
    # Deploy SageMaker Endpoint
    sagemaker_client = boto3.client('sagemaker', region_name=config['REGION'])
    deploy_sagemaker_endpoint(sagemaker_client, repo_name, repo_uri, config)

if __name__ == "__main__":
    main()
