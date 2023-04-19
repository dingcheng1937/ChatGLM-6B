import os

port = '17860'
print('WebUI 端口号', port)

red = "\033[1;32m"
green = "\033[1;31m"
white = "\033[1;37m"
llm_type = 'glm6b'
print('LLM模型类型', llm_type)


def load_LLM():
    try:
        from importlib import import_module
        LLM = import_module('plugins.llm_'+llm_type)
        return LLM

    except Exception as e:
        print("LLM模型加载失败，请阅读说明：https://github.com/l15y/wenda", e)


if llm_type == "glm6b":
    glm_path = "THUDM/chatglm-6b"
    print('glm模型地址', glm_path)
    glm_strategy = 'cuda fp16'
    print('glm模型参数', glm_strategy)
    if 'int4' in glm_path:
        # 判断glm_strategy是否以'i4'或'i8'结尾
        if glm_strategy.endswith('i4') or glm_strategy.endswith('i8'):
            # 报错并退出程序
            print('Error: 请不要使用预量化的模型再设置开始量化参数')
            exit()

    glm_lora_path = os.environ.get('glm_lora_path')
    if not (glm_lora_path == '' or glm_lora_path == None):
        print('glm LoRA 微调启用: ', glm_lora_path)



logging = os.environ.get('logging') != "0"
print('日志记录', logging)

zsk_type = 'bing'
print('知识库类型', zsk_type)
zsk_show_soucre = os.environ.get('zsk_show_soucre')!="0"
print('知识库显示来源', zsk_show_soucre)
if zsk_type == 'x':
    embeddings_path = os.environ.get('embeddings_path')
    print('embeddings模型地址', embeddings_path)
    vectorstore_path = os.environ.get('vectorstore_path')
    print('vectorstore保存地址', vectorstore_path)

# 只输出了zhishiku_bing.py的地址
def load_zsk():
    try:
        from importlib import import_module
        zhishiku = import_module('plugins.zhishiku_'+zsk_type)
        return zhishiku

    except Exception as e:
        print("知识库加载失败，请阅读说明：https://github.com/l15y/wenda", e)


# chunk_size = int(os.environ.get('200'))
# 大数据集分成多个小块，分别处理每个小块以减小单次处理的数据规模和内存压力，从而提高程序效率
chunk_size = 200
print('chunk_size', chunk_size)
# chunk_count = int(os.environ.get('5'))
chunk_count = 1
print('chunk_count', chunk_count)

zhishiku_folder_name = os.environ.get('zsk_folder', "txt")
print('知识库文件夹名称为:', zhishiku_folder_name)
