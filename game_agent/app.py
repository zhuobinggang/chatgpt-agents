import tiktoken
from revChatGPT.V1 import Chatbot
import os
import time

def request(chatbot, prompt = "昭和年代日本最流行的歌曲包括哪些？"):
    ress = []
    for data in chatbot.ask(prompt):
        response = data["message"]
        ress.append(response)
    print(response)
    return response

def test_tokenizer():
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    ids = encoding.encode('You are a man from ancient days.')
    print(len(ids))


def run():
    chatbot = Chatbot(config={"access_token": os.getenv('OPENAI_TOKEN')})

def send_and_reset(chatbot, prompt):
    chatbot.reset_chat() # NOTE: NEED THIS TO AVOID HISTORY
    return request(chatbot, prompt)
