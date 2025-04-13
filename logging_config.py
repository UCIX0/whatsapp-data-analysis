# logging_config.py
import logging

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_format)

# fILE
file_handler = logging.FileHandler('chat_processor.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Headers repetidos
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
