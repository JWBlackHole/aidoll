# src/chatbot_inference.py
import boto3
import os
import json
class ChatbotInference:
    def __init__(self):
        # Initialize AWS credentials as before
        print("AWS_ACCESS_KEY_ID:", os.environ.get('AWS_ACCESS_KEY_ID'))
        print("AWS_SECRET_ACCESS_KEY:", os.environ.get('AWS_SECRET_ACCESS_KEY'))
        print("BEDROCK_KNOWLEDGE_BASE_ID:", os.environ.get('BEDROCK_KNOWLEDGE_BASE_ID'))
        print("BEDROCK_MODEL_ID:", os.environ.get('BEDROCK_MODEL_ID'))
        
        # Initialize both clients
        self.bedrock_agent_client = boto3.client(
            service_name='bedrock-agent-runtime',
            region_name='us-west-2',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
        )
        
        self.bedrock_runtime_client = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-west-2',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
        )
        
        self.knowledge_base_id = os.environ.get('BEDROCK_KNOWLEDGE_BASE_ID')
        self.model_id = os.environ.get('BEDROCK_MODEL_ID')
        self.max_tokens = 500

    def ask(self, input_text, use_knowledge_base=False, system_prompt=None):
        try:
            if use_knowledge_base:
                response = self._generate_with_knowledge_base(input_text, system_prompt)
            else:
                response = self._generate_direct(input_text, system_prompt)

            print(response)
            if response['statusCode'] == 200:
                    return response['body']['response']
            else:
                return "Generation Failed"
        except Exception as e:
            print(f"Error in generate_response: {str(e)}")
            return {
                'statusCode': 500,
                'body': {
                    'error': str(e)
                }
            }

    def _generate_with_knowledge_base(self, input_text, system_prompt):
        """Generate response using Knowledge Base"""
        try:

            body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            # "system": system_prompt,        # not tested
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": input_text}]}
            ]
            })

            print("Knowledge Base prompt:", body)

            response = self.bedrock_agent_client.retrieve_and_generate(
                input=body,
                contentType="application/json",
                accept="application/json",
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.knowledge_base_id,
                        'modelArn': f'arn:aws:bedrock:{self.bedrock_agent_client.meta.region_name}::foundation-model/{self.model_id}'
                    }
                }
            )
            
            return {
                'statusCode': 200,
                'body': {
                    'response': response['output']['text'],
                    'mode': 'knowledge_base'
                }
            }
        except Exception as e:
            print(f"Error in Knowledge Base generation: {str(e)}")
            raise

    def _generate_direct(self, input_text, system_prompt=None):
        """Generate response directly from the model"""
        try:


            
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "system": "你是一個20歲男生性格活潑,喜歡與朋友開玩笑,調侃朋友",        # not tested
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": input_text}]}
                ]
            })

            
            response = self.bedrock_runtime_client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            reply_text = response_body['content'][0]['text']
            
            return {
                'statusCode': 200,
                'body': {
                    'response': reply_text,
                    'mode': 'direct'
                }
            }
        except Exception as e:
            print(f"Error in direct model generation: {str(e)}")
            raise
    def get_response_text(self, input_text, use_knowledge_base=False, system_prompt=None):
        """Get only the response text from the model."""
        try:
            response = self.ask(input_text, use_knowledge_base, system_prompt)
            if response['statusCode'] == 200:
                return response['body']['response']
            else:
                print(f"Error in response: {response['body'].get('error', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Error in get_response_text: {str(e)}")
            return None