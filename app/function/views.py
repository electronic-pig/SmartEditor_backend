import os
from time import sleep
import base64
import requests
from dotenv import load_dotenv
from flask import jsonify, request, Response
from flask_jwt_extended import jwt_required
import erniebot

from . import function

load_dotenv()
erniebot.api_type = "aistudio"
erniebot.access_token = os.getenv('ACCESS_TOKEN')


@function.route('/ocr', methods=['POST'])
def ocr():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'message': '无文件上传!', 'code': 400})
    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify({'message': '无文件上传!', 'code': 400})
    # 二进制读取文件内容
    image_bytes = file.read()
    image_base64 = base64.b64encode(image_bytes).decode('ascii')
    # 设置鉴权信息
    headers = {
        "Authorization": f"token {os.getenv('ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    # 设置请求体
    payload = {
        "image": image_base64  # Base64编码的文件内容或者文件链接
    }
    try:
        resp = requests.post(url=os.getenv('OCR_API_URL'), json=payload, headers=headers)
        resp.raise_for_status()  # 将引发异常，如果状态码不是 200-399
        ocr_result = resp.json()["result"]
        result = ''
        for text in ocr_result["texts"]:
            result += text["text"]
            result += '\n'
        return jsonify({'message': result, 'code': 200})
    except Exception as e:
        print(f"处理响应时发生错误: {e}")
        return jsonify({'message': '后端小模型OCR服务未启动！', 'code': 400})


@function.route('/asr', methods=['POST'])
def asr():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'message': '无文件上传!', 'code': 400})

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify({'message': '无文件上传!', 'code': 400})

    # TODO：调用后端小模型ASR服务
    sleep(1.33)
    return jsonify({'message': '后端小模型ASR服务未启动！', 'code': 400})

    # Demo：返回固定文本
    # return jsonify({'message': '早上八点我从北京到广州花了四百二十六元', 'code': 200})


@function.route('/AIFunc', methods=['POST'])
# @jwt_required()
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

    def generate():
        response = erniebot.ChatCompletion.create(model="ernie-4.0",
                                                  messages=[{"role": "user", "content": prompt}],
                                                  stream=True)
        for chunk in response:
            # 确保chunk.get_result()返回的是字符串
            result = chunk.get_result()
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            yield f"data: {result}\n\n"

    return Response(generate(), content_type='text/event-stream')
