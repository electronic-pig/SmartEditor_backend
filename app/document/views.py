from flask import request, jsonify

from database import db
from . import document
from .models import Documents


# 创建文档
@document.route('/', methods=['POST'])
def create_document():
    data = request.get_json()
    new_document = Documents(user_id=data['user_id'], title=data['title'], content=data['content'])
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': 'Document created!', 'code': '200'})


# 查询单个文档
@document.route('/<int:document_id>', methods=['GET'])
def get_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    return jsonify({'document': doc.to_dict(), 'code': '200'})


# 查询用户的所有文档
@document.route('/user/<int:user_id>', methods=['GET'])
def get_documents_by_user(user_id):
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=False).all()
    if not docs:
        return jsonify({'message': 'No documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 更新文档
@document.route('/<int:document_id>', methods=['PUT'])
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
def delete_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted!', 'code': '200'})


# 收藏文档
@document.route('/favorite/<int:document_id>', methods=['PUT'])
def favorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_favorite = True
    db.session.commit()
    return jsonify({'message': 'Document favorited!', 'code': '200'})


# 取消收藏文档
@document.route('/unfavorite/<int:document_id>', methods=['PUT'])
def unfavorite_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_favorite = False
    db.session.commit()
    return jsonify({'message': 'Document unfavorited!', 'code': '200'})


# 查询用户的所有收藏文档
@document.route('/favorites/user/<int:user_id>', methods=['GET'])
def get_favorite_documents(user_id):
    docs = Documents.query.filter_by(user_id=user_id, is_favorite=True).all()
    if not docs:
        return jsonify({'message': 'No favorite documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


# 逻辑删除文档
@document.route('/delete/<int:document_id>', methods=['PUT'])
def delete_document_logic(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Document deleted!', 'code': '200'})


# 恢复逻辑删除的文档
@document.route('/recover/<int:document_id>', methods=['PUT'])
def recover_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    doc.is_deleted = False
    db.session.commit()
    return jsonify({'message': 'Document recovered!', 'code': '200'})


# 查询用户的所有逻辑删除的文档
@document.route('/deleted/user/<int:user_id>', methods=['GET'])
def get_deleted_documents(user_id):
    docs = Documents.query.filter_by(user_id=user_id, is_deleted=True).all()
    if not docs:
        return jsonify({'message': 'No deleted documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})
