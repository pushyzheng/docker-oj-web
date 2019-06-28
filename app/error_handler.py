# encoding:utf-8
from app import app
from utils import logger
from flask import jsonify


@app.errorhandler(400)
def error_400(error):
    return jsonify(
        code=400,
        data=None,
        message=str(error)
    ), 400


@app.errorhandler(404)
def error_404(error):
    return jsonify(
        code=404,
        data=None,
        message=str(error)
    ), 404


@app.errorhandler(403)
def error_403(error):
    return jsonify(
        code=403,
        data=None,
        message=str(error)
    ), 403


@app.errorhandler(401)
def error_401(error):
    return jsonify(
        code=401,
        data=None,
        message=str(error)
    ), 401


@app.errorhandler(500)
def error_500(error):
    logger.error(str(error))
    return jsonify(
        code=500,
        data=None,
        message='The server encountered an internal error and was unable to complete your request'
    ), 500
