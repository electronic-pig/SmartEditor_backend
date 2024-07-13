import os

from dotenv import load_dotenv
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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

    return jsonify({'message': 'OCR返回文本结果测试!', 'code': 200})


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

    return jsonify({'message': 'ASR返回文本结果测试!', 'code': 200})


@function.route('/AIFunc', methods=['POST'])
@jwt_required()
def AIFunc():
    data = request.get_json()
    command = data['command']
    text = data['text']
    if command == '续写':
        prompt = "请帮我续写以下内容，仅返回生成内容。" + text
    elif command == '润色':
        prompt = "请帮我润色以下内容，仅返回生成内容。" + text
    elif command == '校对':
        prompt = "请帮我校对以下内容，仅返回生成内容。" + text
    elif command == '翻译':
        prompt = "请帮我翻译以下内容，仅返回生成内容。" + text
    elif command == '全文翻译':
        prompt = "请帮我全文翻译以下内容，保留HTML标签，且仅返回生成的HTML内容。" + text
    elif command == '全文总结':
        prompt = '请帮我总结以下内容，仅返回生成内容。' + text
    elif command == '摘要提取':
        prompt = '请帮我提取以下内容的摘要，仅返回生成内容。' + text
    elif command == '智能排版':
        prompt = ('请帮我将以下内容排版为论文格式，'
                  '保留原始的HTML标签，直接返回生成的HTML内容。') + text
    else:
        prompt = f"请以{data['tone']}的风格，{data['prompt']}" if data['tone'] else data['prompt']

    response = erniebot.ChatCompletion.create(model="ernie-3.5",
                                              messages=[{"role": "user", "content": prompt}])

    return jsonify({'message': response.get_result(), 'code': 200})
