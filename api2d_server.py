from fastapi import FastAPI, Request
import uvicorn, json, datetime
import requests
from urllib.error import HTTPError

app = FastAPI()


@app.post("/")
async def create_item(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    #log = "[" + "] " + '", prompt:"' + prompt + '", history:"' + repr(history) + '"'
    #print(log)

    url = "https://openai.api2d.net/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer fk198935-lRy9e4ADx6JO1Dmwxi1t3Ib1CPXpZoiO'
        # <-- 把 fkxxxxx 替换成你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    if response.status_code != 200:
        raise HTTPError(status_code=response.status_code, detail=response.text)
    return response.json()


if __name__ == '__main__':
    uvicorn.run('api2d_server:app', host='0.0.0.0',
                port=8000, workers=1)