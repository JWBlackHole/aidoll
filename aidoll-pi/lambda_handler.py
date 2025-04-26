import json
from src.chatbot_inference import ChatbotInference

def lambda_handler(event, context):
    """
    Lambda handler function that processes incoming requests
    """
    chatbot = ChatbotInference()
    
    try:
        # Handle API Gateway request
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event  # For direct Lambda invocation
            
        user_input = body['input']
        
        # Generate response
        response = chatbot.generate_response(user_input)
        
        return {
            'statusCode': response.get('statusCode', 200),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # For CORS support
            },
            'body': json.dumps(response.get('body', {}))
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Error processing request: {str(e)}'
            })
        }
