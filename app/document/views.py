from flask import request, jsonify

from database import db
from . import document
from .models import Documents


@document.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    new_document = Documents(user_id=data['user_id'], title=data['title'], content=data['content'])
    db.session.add(new_document)
    db.session.commit()
    return jsonify({'message': 'Document created!', 'code': '200'})


@document.route('/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '200'})
    return jsonify({'title': doc.title, 'content': doc.content})


@document.route('/documents/user/<int:user_id>', methods=['GET'])
def get_documents_by_user(user_id):
    docs = Documents.query.filter_by(user_id=user_id).all()
    if not docs:
        return jsonify({'message': 'No documents found for this user!', 'code': '200'})
    return jsonify({'documents': [{'id': doc.id, 'title': doc.title, 'content': doc.content} for doc in docs]})


@document.route('/documents/<int:document_id>', methods=['PUT'])
def update_document(document_id):
    data = request.get_json()
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '200'})
    doc.title = data['title']
    doc.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Document updated!'})


@document.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    doc = Documents.query.get(document_id)
    if doc is None:
        return jsonify({'message': 'Document not found!', 'code': '200'})
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted!'})
