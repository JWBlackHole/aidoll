# local_run.py
import os
from dotenv import load_dotenv
from src.chatbot_inference import ChatbotInference
from src.chatbot2 import BedrockClient

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize chatbot
    #chatbot = BedrockClient()
    chatbot = ChatbotInference()
    
    print("Chatbot initialized. Type 'quit' to exit.")
    
            # Get user input
    user_input = input("\nYou: ")
    
    #if user_input.lower() == 'quit':
        
    # Generate response
    system_prompt = "你是一個20歲男生性格活潑,喜歡與朋友開玩笑,調侃朋友"
    response = chatbot.ask(user_input)
    
    print(response)

if __name__ == "__main__":
    main()
