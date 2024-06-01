from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from . import document
from .models import Documents


# 创建文档
@document.route('/', methods=['POST'])
@jwt_required()
def create_document():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_document = Documents(user_id=user_id, title=data['title'], content=data['content'])
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': 'Document created!', 'code': '200'})


# 查询单个文档
@document.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    return jsonify({'document': doc.to_dict(), 'code': '200'})


# 查询用户的所有文档
@document.route('/user', methods=['GET'])
@jwt_required()
def get_documents_by_user():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=False).all()
    if not docs:
        return jsonify({'message': 'No documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 更新文档
@document.route('/<int:document_id>', methods=['PUT'])
@jwt_required()
def update_document(document_id):
    data = request.get_json()
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.title = data['title']
    doc.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Document updated!', 'code': '200'})


# 物理删除文档
@document.route('/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted!', 'code': '200'})


# 收藏文档
@document.route('/favorite/<int:document_id>', methods=['PUT'])
@jwt_required()
def favorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_favorite = True
    db.session.commit()
    return jsonify({'message': 'Document favorited!', 'code': '200'})


# 取消收藏文档
@document.route('/unfavorite/<int:document_id>', methods=['PUT'])
@jwt_required()
def unfavorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_favorite = False
    db.session.commit()
    return jsonify({'message': 'Document unfavorited!', 'code': '200'})


# 查询用户的所有收藏文档
@document.route('/favorites/user', methods=['GET'])
@jwt_required()
def get_favorite_documents():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_favorite=True).all()
    if not docs:
        return jsonify({'message': 'No favorite documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 逻辑删除文档
@document.route('/delete/<int:document_id>', methods=['PUT'])
@jwt_required()
def delete_document_logic(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_deleted = True
    doc.is_favorite = False
    db.session.commit()
    return jsonify({'message': 'Document deleted!', 'code': '200'})


# 恢复逻辑删除的文档
@document.route('/recover/<int:document_id>', methods=['PUT'])
@jwt_required()
def recover_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_deleted = False
    db.session.commit()
    return jsonify({'message': 'Document recovered!', 'code': '200'})


# 查询用户的所有逻辑删除的文档
@document.route('/deleted/user', methods=['GET'])
@jwt_required()
def get_deleted_documents():
    user_id = get_jwt_identity()
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=True).all()
    if not docs:
        return jsonify({'message': 'No deleted documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 查询文档模板
@document.route('/template', methods=['GET'])
def get_document_template():
    docs = Documents.query.filter_by(user_id=1).all()
    if not docs:
        return jsonify({'message': 'No document template found!', 'code': '400'})
    return jsonify({'document': [doc.to_dict() for doc in docs], 'code': '200'})
