# encoding:utf-8
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s(func %(funcName)s, line %(lineno)d) - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

from .main import *
from .model import *
