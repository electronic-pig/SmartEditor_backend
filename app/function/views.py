import os
from time import sleep

from dotenv import load_dotenv
from flask import jsonify, request
from flask_jwt_extended import jwt_required
import erniebot
from . import function

load_dotenv()
erniebot.api_type = "aistudio"
erniebot.access_token = os.getenv('ERNIE_BOT_ACCESS_TOKEN')


@function.route('/ocr', methods=['POST'])
def ocr():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'message': '无文件上传!', 'code': 400})

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify({'message': '无文件上传!', 'code': 400})

    # 保存文件
    # file.save(os.path.join('./static/uploads', file.filename))

    return jsonify({'message': '后端小模型OCR服务未启动！', 'code': 400})

    sleep(2.13)
    result = '''
"文心一言"是百度公司开发的一款人工智能产品，它基于百度强大的搜索引擎和大数据技术，具备自然
语言处理、知识图谱、机器学习等能力。文心一言可以为用户提供智能问答、文本分析、情感分析、机
器翻译等多种服务，广泛应用于智能客服、内容推荐、智能写作等领域。
    '''

    return jsonify({'message': result, 'code': 200})


@function.route('/asr', methods=['POST'])
def asr():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'message': '无文件上传!', 'code': 400})

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify({'message': '无文件上传!', 'code': 400})

    # 保存文件
    # file.save(os.path.join('./static/uploads', file.filename))

    return jsonify({'message': '后端小模型ASR服务未启动！', 'code': 400})

    sleep(3.33)
    return jsonify({'message': '早上八点我从北京到广州花了四百二十六元', 'code': 200})


@function.route('/AIFunc', methods=['POST'])
@jwt_required()
def AIFunc():
    data = request.get_json()
    command = data['command']
    text = data['text']
    if command == '续写':
        prompt = "请帮我续写以下内容，限制内容到400字以内，仅返回生成内容。" + text
    elif command == '润色':
        prompt = "请帮我润色以下内容，仅返回生成内容。" + text
    elif command == '校对':
        prompt = "请帮我校对以下内容，仅返回生成内容。" + text
    elif command == '翻译':
        prompt = "请帮我翻译以下内容，仅返回生成内容。" + text
    elif command == '全文翻译':
        prompt = "请帮我全文翻译以下内容，保留HTML标签，且仅返回生成的HTML内容。" + text
    elif command == '全文总结':
        prompt = '请帮我用一段话总结以下内容，仅返回生成内容。' + text
    elif command == '重点提取':
        prompt = '请帮我用一段话提取以下内容的重点，仅返回生成内容。' + text
    else:
        prompt = f"请以{data['tone']}的风格，{data['prompt']}" if data['tone'] else data['prompt']

    response = erniebot.ChatCompletion.create(model="ernie-4.0",
                                              messages=[{"role": "user", "content": prompt}])

    return jsonify({'message': response.get_result(), 'code': 200})
