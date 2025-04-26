# local_run.py
import os
from dotenv import load_dotenv
from src.chatbot_inference import ChatbotInference

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize chatbot
    #chatbot = BedrockClient()
    chatbot = ChatbotInference()
    
    print("Chatbot initialized. Type 'quit' to exit.")
    
    #if user_input.lower() == 'quit':

    while(True):
        print()
        print(f"You     : ", end="")
        user_input = input()
        response = chatbot.ask(user_input)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
