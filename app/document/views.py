from flask import request, jsonify

from database import db
from . import document
from .models import Documents


@document.route('/', methods=['POST'])
def create_document():
    data = request.get_json()
    new_document = Documents(user_id=data['user_id'], title=data['title'], content=data['content'])
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': 'Document created!', 'code': '200'})


@document.route('/<int:document_id>', methods=['GET'])
def get_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    return jsonify({'document': doc.to_dict(), 'code': '200'})


@document.route('/user/<int:user_id>', methods=['GET'])
def get_documents_by_user(user_id):
    docs = Documents.query.filter_by(user_id=user_id).all()
    if not docs:
        return jsonify({'message': 'No documents found for this user!', 'code': '400'})
    return jsonify({'documents': [doc.to_dict() for doc in docs], 'code': '200'})


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


@document.route('/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '400'})
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted!', 'code': '200'})
