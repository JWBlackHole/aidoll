import boto3
import json

class BedrockClient:
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=500):
        # model_id: Replaceable model version
        # max_tokens: Replaceable maximum number of tokens

        self.bedrock = boto3.client("bedrock-runtime")
        self.model_id = model_id
        self.max_tokens = max_tokens

    def ask(self, transcribed_text: str) -> str:
        prompt = f"Please answer the question in detail: {transcribed_text}"

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "system": "你是一個20歲男生性格活潑,喜歡與朋友開玩笑,調侃朋友",        # not tested
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        })

        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )

        response_body = json.loads(response.get('body').read())
        reply_text = response_body['content'][0]['text']

        return reply_text


if __name__ == "__main__":
    transcribed_text = "How's the weather today?"
    client = BedrockClient()
    response = client.ask(transcribed_text)
    print("AI response:", response)