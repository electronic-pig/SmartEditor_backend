from flask import jsonify

from . import auth


@auth.route('/data')
def get_data():
    data = {"name": "John", "age": 30, "city": "New York"}
    return jsonify(data)
