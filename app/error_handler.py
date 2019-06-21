# encoding:utf-8
from app import app
from flask import jsonify

@app.errorhandler(400)
def error_404(error):
    return jsonify(
        code=400,
        data=None,
        message=str(error)
    )