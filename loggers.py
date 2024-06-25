import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

main_logger = logging.getLogger('main')
main_logger.setLevel(logging.INFO)
count_handler = RotatingFileHandler('main.log',maxBytes=2000000, backupCount=5)
count_handler.setFormatter(formatter)
main_logger.addHandler(count_handler)
main_logger.addHandler(stream_handler)

logger_list = logging.getLogger('player_list')
logger_list.setLevel(logging.INFO)
list_handler = RotatingFileHandler('player_list.log', maxBytes=2000000, backupCount=5)
list_handler.setFormatter(formatter)
logger_list.addHandler(count_handler)
logger_list.addHandler(stream_handler)