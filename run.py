# encoding:utf-8
from app import rabbitmq

if __name__ == '__main__':
    rabbitmq.run_with_flask_app()