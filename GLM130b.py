from random import randint
import re
from typing import Callable
from wudao.api_request import getToken,executeSSE




def randomTaskCode():
    return "%019d" % randint(0, 10**19)


# 接口API KEY
API_KEY = "b50621c0b771425d9193a9a02535ddc6"
# 公钥
PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALfEf2ntKBHTZS34g7mTY5dSjTTLkdKNB4P1ALdoLkWLBx4byituYmDRsG/wTmBfspiLjlklFzAgxZO2nidK9+sCAwEAAQ=="

# 能力类型
ability_type = "chatGLM"
# 引擎类型
engine_type = "chatGLM"

token_result = getToken(API_KEY, PUBLIC_KEY)

_FIELD_SEPARATOR = ":"

def punctuation_converse_auto(msg):
    punkts = [
        [",", "，"],
        ["!", "！"],
        [":", "："],
        [";", "；"],
        ["\?", "？"],
    ]
    for item in punkts:
        msg = re.sub(r"([\u4e00-\u9fff])%s" % item[0], r"\1%s" % item[1], msg)
        msg = re.sub(r"%s([\u4e00-\u9fff])" % item[0], r"%s\1" % item[1], msg)
    return msg

def prepare_print_diff(nextStr: Callable[[any], str], printError: Callable[[], None]):
    previous = ""
    def print_diff(input):
        nonlocal previous
        str = nextStr(input)
        if (not str.startswith(previous)):
            last_line_index = str.rfind("\n") + 1
            if (previous.startswith(str[0: last_line_index])):
                print("\r%s" % str[last_line_index:], end="", flush=True)
            else:
                print()
                print(1, "[[previous][%s]]" % previous)
                printError(input)
        else:
            print(str[len(previous):], end="", flush=True)
        previous = str

    return print_diff

def print_history(history):
    is_request = True
    for history_item in history:
        print("Request:" if is_request else "Response:")
        print("\t", history_item)
        is_request = not is_request

if __name__ == "__main__":
    import requests
    import pprint
    if token_result and token_result["code"] == 200:
        token = token_result["data"]
        history = []
        print()
        print("'clear' to clear history and 'history' to show history. Ctrl-C to exit")
        while (True):
            print("Your Input:")
            prompt_line = input()
            prompt_line_list = []
            while(len(prompt_line_list) == 0 or not (prompt_line == "")):
                prompt_line_list.append(prompt_line)
                prompt_line = input()
            prompt = "\n".join(prompt_line_list).strip()


            if prompt == "clear":
                history = []
                print("History Cleared.")
                continue
            elif prompt == "history":
                print_history(history)
                print()
                continue


            print("Sending Request...")
            print()

            json = {
                "top_p": 0.7,
                "temperature": 0.9,
                "risk": 0.15,
                "prompt": prompt,
                "requestTaskNo": randomTaskCode(),
                "history": history,
            }

            client = executeSSE(ability_type, engine_type, token, json)
            print_diff = prepare_print_diff(lambda e: e.data, lambda e: pprint.pprint(e.__dict__))
            print('Response: ')
            for event in client.events():
                if (event.data):
                    event.data = punctuation_converse_auto(event.data)
                if (event.event == "add"):
                    print_diff(event)
                elif (event.event == "finish" or event.event == "interrupted"):
                    print_diff(event)
                    print()
                    history.extend([prompt, event.data])
                    break
                elif (event.event == "error"):
                    print_diff(event)
                    print()
                    break
                else:
                    pprint.pprint(event.__dict__)
            print()
    else:
        print("获取token失败，请检查 API_KEY 和 PUBLIC_KEY")
