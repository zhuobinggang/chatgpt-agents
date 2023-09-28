from revChatGPT.V1 import Chatbot
import os
chatbot = Chatbot(config={"access_token": os.getenv('OPENAI_TOKEN')})
def request(prompt = "昭和年代日本最流行的歌曲包括哪些？"):
    ress = []
    for data in chatbot.ask(prompt):
        response = data["message"]
        ress.append(response)
    print(response)
    return response
