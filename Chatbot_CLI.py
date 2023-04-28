import requests
import os
import platform

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'

API2Durl = "http://10.23.52.95:8001/"
CHATGLMurl = "http://10.23.52.95:8000/"

history = []
WELCOME_STRING = "欢迎使用API2D，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"
AITYPE_STRING = "请选择使用API2D或"
print(WELCOME_STRING)
while True:
    AIType = input()
    query = input("\n用户：")
    if query.strip() == "stop":
        break
    if query.strip() == "clear":
        history = []
        os.system(clear_command)
        print(WELCOME_STRING)
        continue
    #count = 0
    payload = {
        "prompt": query,
        "history": []
    }

    response = requests.post(url, json=payload)

    #count += 1
    print(f"API2D: {response.json()['choices'][0]['message']['content']}")