import boto3

# Create separate clients for different purposes
bedrock = boto3.client('bedrock')  # For listing models and other management operations
bedrock_runtime = boto3.client('bedrock-runtime')  # For model invocation
bedrock_agent = boto3.client('bedrock-agent-runtime')  # For agent/KB operations

# List available foundation models
try:
    response = bedrock.list_foundation_models()
    print("\nAvailable Models:")
    for model in response['modelSummaries']:
        print(f"Model ID: {model['modelId']}")
        print(f"Model Name: {model.get('modelName', 'N/A')}")
        print(f"Provider: {model.get('providerName', 'N/A')}")
        print("---")
except Exception as e:
    print(f"Error listing models: {str(e)}")
