import requests

#knowledge = ['我喜欢吃水果', '我不喜欢吃蔬菜', '对于肉类，有时候我喜欢吃，有时候不喜欢吃，比如膻味很重的羊肉我就不爱吃']
with open('output2.txt', 'r') as f:
    knowledge = [line.strip() for line in f]

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer fk198935-lRy9e4ADx6JO1Dmwxi1t3Ib1CPXpZoiO' # 替换成你的 Forward key
}

def get_embeddings(str):
    response = requests.post('https://openai.api2d.net/v1/embeddings', json={
        'model': 'text-embedding-ada-002',
        'input': str
    }, headers=headers)
    return response.json()

def insert_into_vector_db(text, uuid, embedding):
    response = requests.post('https://openai.api2d.net/vector', json={
        'text': text,
        'uuid': uuid,
        'embedding': embedding
    }, headers=headers)
    return response.json()

def get_uuid():
    response = requests.get('https://openai.api2d.net/vector/uuid', headers=headers)
    return response.json()['uuid']

def insert_data():
    uuid = get_uuid()
    print('uuid: ', uuid)

    for text in knowledge:
        embedding_response = get_embeddings(text)
        print('输入文本：', text, '，embeddings 请求结果：', embedding_response)

        insert_response = insert_into_vector_db(text, uuid, embedding_response['data'][0]['embedding'])
        print('写入数据库请求结果：', insert_response)

insert_data()
