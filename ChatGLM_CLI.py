import requests
import os
import platform

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'

url = "http://10.23.52.95:8000/"

history = []
WELCOME_STRING = "欢迎使用ChatGLM，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"
Prompt_string = "现在你以'啵嘤冰'的身份和用户进行聊天，'啵嘤冰'是一位来自归桑的神明。如果你不能理解我说的话，也不要说不知道，而是幽默地插科打诨。"
print(WELCOME_STRING)
while True:
    query = input("\n用户：")
    if query.strip() == "stop":
        break
    if query.strip() == "clear":
        history = []
        os.system(clear_command)
        print(WELCOME_STRING)
        continue
    #count = 0
    query = Prompt_string + "问题：" + query
    payload = {
        "prompt": query,
        "history": []
    }

    response = requests.post(url, json=payload)

    #count += 1
    print(f"ChatGLM: {response.json()['response']}")