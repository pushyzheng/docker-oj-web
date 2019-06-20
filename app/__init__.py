# encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_rabbitmq import RabbitMQ, Queue

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

queue = Queue()
rabbitmq = RabbitMQ(app, queue)

from app import views, models, mq
