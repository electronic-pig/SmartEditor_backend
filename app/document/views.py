import json
from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import *
from . import document
from .models import Documents


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


# 创建文档
@document.route('', methods=['POST'])
@jwt_required()
def create_document():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_document = Documents(user_id=user_id, title='未命名文档', content=data['content'])
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': '创建成功!', 'id': new_document.id, 'code': '200'})


# 查询单个文档
@document.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    cache_key = f"document:{document_id}"
    cached_doc = redis_client.get(cache_key)
    if cached_doc:
        print('cache hit!')
        return jsonify({'document': json.loads(cached_doc), 'code': '200'})
    else:
        doc = Documents.query.get(document_id)
        if doc is None:
            return jsonify({'message': '查询失败!', 'code': '400'})
        redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
        return jsonify({'document': doc.to_dict(), 'code': '200'})


# 查询用户的所有文档
@document.route('/user', methods=['GET'])
@jwt_required()
def get_documents_by_user():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=False).all()
    if not docs:
        return jsonify({'message': '该用户无任何文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 更新文档
@document.route('/<int:document_id>', methods=['PUT'])
@jwt_required()
def update_document(document_id):
    data = request.get_json()
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.title = data['title']
    doc.content = data['content']
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '更新成功!', 'code': '200'})


# 物理删除文档
@document.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    db.session.delete(doc)
    db.session.commit()
    # 清理Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.delete(cache_key)
    return jsonify({'message': '删除成功!', 'code': '200'})


# 收藏文档
@document.route('/favorite/<int:document_id>', methods=['PUT'])
@jwt_required()
def favorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_favorite = True
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '收藏成功!', 'code': '200'})


# 取消收藏文档
@document.route('/unfavorite/<int:document_id>', methods=['PUT'])
@jwt_required()
def unfavorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_favorite = False
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '取消收藏成功!', 'code': '200'})


# 查询用户的所有收藏文档
@document.route('/favorites/user', methods=['GET'])
@jwt_required()
def get_favorite_documents():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_favorite=True).all()
    if not docs:
        return jsonify({'message': '该用户无任何收藏文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 逻辑删除文档
@document.route('/delete/<int:document_id>', methods=['PUT'])
@jwt_required()
def delete_document_logic(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_deleted = True
    doc.is_favorite = False
    doc.is_template = False
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '放入回收站成功!', 'code': '200'})


# 恢复逻辑删除的文档
@document.route('/recover/<int:document_id>', methods=['PUT'])
@jwt_required()
def recover_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_deleted = False
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '恢复成功!', 'code': '200'})


# 查询用户的所有逻辑删除的文档
@document.route('/deleted/user', methods=['GET'])
@jwt_required()
def get_deleted_documents():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=True).all()
    if not docs:
        return jsonify({'message': '该用户无任何回收站文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 查询模板库文档
@document.route('/template', methods=['GET'])
def get_document_template():
    docs = Documents.query.filter_by(user_id=1).all()
    if not docs:
        return jsonify({'message': '模板库无任何文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 根据用户的查询参数进行模糊查询
@document.route('/search/<string:title>', methods=['GET'])
@jwt_required()
def search_documents_by_user(title):
    user_id = get_jwt_identity()
    docs = Documents.query.filter(Documents.user_id == user_id,
                                  Documents.is_deleted == False,
                                  Documents.title.like(f"%{title}%")).all()
    if not docs:
        return jsonify({'message': '未查询到匹配文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 查询用户的模板文档
@document.route('/template/user', methods=['GET'])
@jwt_required()
def get_template_documents_by_user():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_template=True, is_deleted=False).all()
    if not docs:
        return jsonify({'message': '该用户无任何模板文档!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 将文档设置为模板
@document.route('/template/<int:document_id>', methods=['PUT'])
@jwt_required()
def set_document_template(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_template = True
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '另存为模板成功!', 'code': '200'})


# 将模板文档取消模板
@document.route('/untemplate/<int:document_id>', methods=['PUT'])
@jwt_required()
def unset_document_template(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': '查询失败!', 'code': '400'})
    doc.is_template = False
    db.session.commit()
    # 更新Redis缓存
    cache_key = f"document:{document_id}"
    redis_client.set(cache_key, json.dumps(doc.to_dict(), cls=CustomJSONEncoder))
    return jsonify({'message': '撤销模板成功!', 'code': '200'})
