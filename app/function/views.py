import os
from time import sleep

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import function


@function.route('/ocr', methods=['POST'])
# @jwt_required()
def ocr():
    # user_id = get_jwt_identity()

    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request', 'code': 400})

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件是否存在
    if file.filename == '':
        return jsonify({'message': 'No selected file', 'code': 400})

    # 保存文件
    file.save(os.path.join('./static/uploads', file.filename))

    return jsonify({'message': 'OCR返回文本结果测试!', 'code': 200})


@function.route('/aiTest', methods=['POST'])
# @jwt_required()
def aiTest():
    # user_id = get_jwt_identity()
    data = request.get_json()
    print(data)
    sleep(2)
    reply = '''我是一个基于大规模语言模型的AI，设计来理解和生成文本。
    我的训绀和知识是由多种数据源累积而成，截止到我最后一次更新的知识都在2023年。
    我可以帮助解答问题、提供信息、撰写文章等。如果你有任何问题或需求，随时可以问我。'''

    return jsonify({'message': data, 'code': 200})
