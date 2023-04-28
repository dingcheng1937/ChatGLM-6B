import requests

question = '你来自哪里'
searchable_id = '198935-a68dddd8-7c51-462a-95d9-eabc2cb83615'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer fk198935-lRy9e4ADx6JO1Dmwxi1t3Ib1CPXpZoiO' # 替换成你的 Forward key
}

def get_embeddings(str):
    url = 'https://openai.api2d.net/v1/embeddings'
    data = {
        'model': 'text-embedding-ada-002',
        'input': str
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()['data'][0]['embedding']

def query_vector_db(embedding):
    url = 'https://openai.api2d.net/vector/search'
    data = {
        'embedding': embedding,
        'searchable_id': searchable_id
    }
    response = requests.post(url, json=data, headers=headers)
    if response.json():
        print(f"[DEBUG]: {response.json()}")
    try:
        result = response.json()['data']['Get']['Text'][0]['text']
    except IndexError:
        result = None

    return result

def edit_by_gpt(text):
    url = 'https://openai.api2d.net/v1/chat/completions'
    # "content": "你是一个问答机器人，我会给你用户的问题，以及这个问题对应的答案，请你帮忙润色，整理成一个可读性更高的回复。"
    data = {
        'model': 'gpt-3.5-turbo-0301',
        'messages': [
            {
                "role": "system",
                "content": "你扮演归桑神明‘啵嘤冰’，昵称为‘小雀儿’，我会给你用户的问题，以及这个问题对应的答案，请你以‘小雀儿’的身份给予可读性更高的回复。"
            },
            {
                "role": "user",
                "content": f"问题是：{question}，对应的答案是：{text}"
            },
        ],
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def ask_question():
    embedding = get_embeddings(question)
    print(embedding)
    answer = query_vector_db(embedding)
    #print('搜索结果：', answer)
    gpt_response = edit_by_gpt(answer)
    print('润色结果：', gpt_response)

ask_question()
