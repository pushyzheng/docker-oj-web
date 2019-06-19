# encoding:utf-8
from app import app, mq

if __name__ == '__main__':
    mq.run_with_flask_app()