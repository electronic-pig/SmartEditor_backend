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
        prompt = ("这是从文档截取的一部分文本内容。\n" + text +
                  "\n请帮我续写这部分内容，保持原有的写作风格和语气。续写内容应连贯且自然，长度约为两段，每段不少于100字。"
                  "请确保续写部分与原文内容主题一致，并继续探讨相关话题。只需要续写内容，不需要返回其他内容。")
    elif command == '润色':
        prompt = ("这是从文档截取的一部分文本内容。\n" + text +
                  "\n请帮我润色这部分内容，保持原有的写作风格和语气。润色后的内容应更加流畅、自然，并纠正任何语法或拼写错误。"
                  "请确保内容的主题和信息不变。只需要返回润色后的内容，不需要返回其他内容。")
    elif command == '校对':
        prompt = ("这是从文档截取的一部分文本内容。\n" + text +
                  "\n请帮我校对这部分内容，保持原有的写作风格和语气。校对后的内容应纠正所有语法、拼写和标点错误。"
                  "请确保不改变原文的主题和信息。只需要返回校对后的内容，不需要返回其他内容。")
    elif command == '翻译':
        prompt = ("这是从文档截取的一部分文本内容。\n" + text +
                  "\n根据原有的语言，请帮我将这部分内容翻译成中文或英文，保持原有的写作风格和语气。"
                  "翻译后的内容应准确传达原文的意思，并且自然流畅。只需要返回翻译后的内容，不需要返回其他内容。")
    elif command == '内容简化':
        prompt = ("这是一份文档的文本内容。\n" + text +
                  "\n请帮我简化这些内容，使其更易于理解。保留关键信息和主要观点，去除冗余和复杂的表达。"
                  "简化后的内容应保持原文的主题和信息不变，但更简洁明了。只需要返回简化后的内容，不需要返回其他内容。")
    elif command == '全文翻译':
        prompt = ("这是一份文档的文本内容。\n" + text +
                  "\n根据原有的语言，请将这些内容翻译成中文或英文，保持原有的写作风格和语气。"
                  "翻译后的内容应准确传达原文的意思，并且自然流畅。只需要返回翻译后的内容，不需要返回其他内容。")
    elif command == '全文总结':
        prompt = ("这是一份文档的文本内容。\n" + text +
                  "\n请帮我总结这些内容，保持原有的写作风格和语气。"
                  "总结后的内容应概括文档的主要观点和结论，并且简洁明了。只需要返回总结后的内容，不需要返回其他内容。")
    elif command == '重点提取':
        prompt = ("这是一份文档的文本内容。\n" + text +
                  "\n请帮我提取这些内容的重点信息。重点信息应包括主要观点、关键数据和重要结论。"
                  "提取后的内容应简洁明了，涵盖文档的核心内容。只需要返回提取后的内容，不需要返回其他内容。")
    else:
        prompt = f"请采用{data['tone']}的生成风格，{data['prompt']}" if data['tone'] else data['prompt']

    def generate():
        response = erniebot.ChatCompletion.create(model="ernie-4.0",
                                                  messages=[{"role": "user", "content": prompt}],
                                                  stream=True)
        for chunk in response:
            result = chunk.get_result()
            yield f"{result}"

    return Response(generate(), content_type='text/event-stream')


@function.route('/typography', methods=['POST'])
# @jwt_required()
def typography():
    data = request.get_json()
    text = data['text']
    title = data['title']
    font = data['font']
    font_size = data['font_size']
    line_spacing = data['line_spacing']
    paragraph = data['paragraph']
    prompt = (
        f"这是一份文档的HTML文本内容。\n"
        f"{text}\n"
        f"请将上述HTML内容重新排版为{title}的格式。要求如下：\n"
        f"- 字体：{font}\n"
        f"- 字号：{font_size}\n"
        f"- 行距：{line_spacing}\n"
        f"- 段落：{paragraph}\n"
        f"只需要返回生成后的HTML文本，不需要返回其他内容。"
    )

    def generate():
        response = erniebot.ChatCompletion.create(model="ernie-4.0",
                                                  messages=[{"role": "user", "content": prompt}],
                                                  stream=True)
        for chunk in response:
            result = chunk.get_result()
            yield f"{result}"

    return Response(generate(), content_type='text/event-stream')
