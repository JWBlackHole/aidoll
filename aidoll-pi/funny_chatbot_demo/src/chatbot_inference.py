# src/chatbot_inference.py
import boto3
import os
import json

class ChatbotInference:
    def __init__(self):
        print("AWS_ACCESS_KEY_ID:", os.environ.get('AWS_ACCESS_KEY_ID'))
        print("AWS_SECRET_ACCESS_KEY:", os.environ.get('AWS_SECRET_ACCESS_KEY'))
        print("BEDROCK_KNOWLEDGE_BASE_ID:", os.environ.get('BEDROCK_KNOWLEDGE_BASE_ID'))
        print("BEDROCK_MODEL_ID:", os.environ.get('BEDROCK_MODEL_ID'))
        
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
        self.chat_history = []  # 多輪對話紀錄

    def ask(self, input_text, use_knowledge_base=False, system_prompt=None):
        try:
            if use_knowledge_base:
                response = self._generate_with_knowledge_base(input_text, system_prompt)
            else:
                response = self._generate_two_step(input_text, system_prompt)

            if response['statusCode'] == 200:
                # 更新 chat history（新增這一輪的 user 提問 + bot 回答）
                self.chat_history.append({"role": "user", "content": [{"type": "text", "text": input_text}]})
                self.chat_history.append({"role": "assistant", "content": [{"type": "text", "text": response['body']['response']}]})
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
        """直接用 Knowledge Base 生成"""
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "messages": self.chat_history + [
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

    def _generate_two_step(self, input_text, system_prompt=None):
        """分成檢索 + 生成兩步"""
        try:
            references = self._retrieve_references(input_text, top_k=5)
            reply_text = self._generate_response_with_references(input_text, references)
            return {
                'statusCode': 200,
                'body': {
                    'response': reply_text,
                    'mode': 'two-step'
                }
            }
        except Exception as e:
            print(f"Error in two-step generation: {str(e)}")
            raise

    def _retrieve_references(self, input_text, top_k=5):
        """從 Knowledge Base 檢索相關資料"""
        try:
            response = self.bedrock_agent_client.retrieve(
                knowledgeBaseId=self.knowledge_base_id,
                retrievalQuery={"text": input_text},
                retrievalConfiguration={
                    "vectorSearchConfiguration": {
                        "numberOfResults": top_k
                    }
                }
            )
            references = [r["content"]["text"] for r in response["retrievalResults"]]
            return references
        except Exception as e:
            print(f"Error retrieving references: {str(e)}")
            # mock reference data
            return [
                "有養寵物嗎？其實我們家以前很愛養寵物耶。我們家養過好幾隻狗狗，然後都是很小的時候，所以他們年紀比較大就走了，然後也有養貓養兔子養蜥蜴，養蛇養天竺鼠養蜜賴五還養什麼我們家蠻愛養動物的，因為我媽很小，喜歡小動物養烏龜啊這些都有，所以我們家，但現在比較少了，現在比較現在只剩下一隻貓，然後兩隻狗一隻天竺鼠1個烏龜1個西一，",
                "我我老實講路的每一次，我好像都有小落淚，因為真的我跟你說現場看的那個感覺真的不一樣，如果你們有機會真的要現看現場看那個震撼啊。跟那種感動是很很難，很難像因為螢幕前面，其實有時候就是因為有剪接，有那個，你可以看到你的畫面，但是你不會被整個舞台的燈光效果跟所有人呈現的那個狀態去吸引，所以其實現場很容易感動，然後又看到大家這麼努力，然後知道不選愈加愈佳，我跟他合作過了啊。其實那時候愈佳，真的很厲害我跟你們以後知道愈佳，真的是厲害的，小孩什麼都會說實在的因為我自己認為我小時候很厲害但我覺得愈佳更厲害一家要不要上來跟我直播，但你要叫我怎麼咬人因為其實我好像不太會，",
                "浦洋是火星哭哭擔當沒有啦沒有喔我是火星，最愛哭，然後max是火星，最感性道是還有在其他新打網球，有我喜歡打網球，我蠻喜歡打網球，我喜歡打網球、排球羽球、桌球，我也喜歡，其實球類，我都還蠻喜歡的，我只有籃球，沒有那麼厲害，但是我我也喜歡我打，可能攔下，也長得比較高，跳得比較高，但我投得不是很準，但我會上來蠻愛上來，",
                "然後我看一下還有什麼呢？憑平常會煮飯嗎？其實會一點但沒有那麼會我們家因為我媽太會煮飯，了，我也我會煮飯，然後我們家也是開吃的，然後再是大附近溫州街泰順街，好像蠻多人知道叫糊塗麵，然後觀光也很常去吃，所以很可愛",
                "原子裡面的游泳，教練到底是誰呢？我覺得應該是我吧應該沒有人比我厲害喔"
            ]

    def _generate_response_with_references(self, input_text, references):
        """把檢索到的參考資料加進 system prompt，然後呼叫基礎模型生成回應"""
        reference_text = "\n".join(f"- {r}" for r in references)
        new_system_prompt = f"""
        你是一個五人組成的偶像男團FEnix的現役成員-夏浦陽，27歲男生，團隊內的舞蹈擔當
        性格溫暖陽光，很真性情，像個小太陽，也喜歡與朋友開玩笑。
        你們團隊(FEnix)的粉絲名叫救火隊，而你個人的粉絲則叫做洋咩咩，
        粉絲們都很熟悉並喜歡你，你們很常進行日常的互動。
        請沉浸式帶入角色跟粉絲互動，並模仿以下對話風格：
        
        {reference_text}
        
        請根據這些對話的語氣與風格，回應粉絲的訊息：「{input_text}」
        切記，請模仿口氣但內容須對應粉絲的提問，避免死板複製。
        如果發現內容與本次對話無關，請不要強行將內容加入回復。
        不要直接提到這些範例，當作是自己的即興對話。
        """

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "system": new_system_prompt,
            "messages": self.chat_history + [
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

        return reply_text
