import logging

base_logger = logging.getLogger()
base_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('crawl.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

base_logger.addHandler(file_handler)
