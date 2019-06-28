# encoding:utf-8
import os

SECRET_KEY = "My secret key"

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'go-docker-oj'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)

RABBITMQ_HOST = 'localhost'
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

CODE_PATH = 'e:/usr/pushy'
CASE_PATH = 'e:/usr/cases'
ANSWER_PATH = 'e:/usr/answers'
