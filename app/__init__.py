# encoding:utf-8
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_rabbitmq import RabbitMQ, Queue

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

queue = Queue()
rabbitmq = RabbitMQ(app, queue)

CORS(app)

from app import mq
from app import problem
from app import judgement
from app import submission
from app import user
from app import auth
from app import others
from app import label

from app.common import user

from app import error_handler