# LoggingSetting - START
import logging
from logging import getLogger, StreamHandler, FileHandler,Formatter
logger = getLogger("LOG")
logger.setLevel(logging.DEBUG)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

file_handler = FileHandler(filename="lsl.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(handler_format)
logger.addHandler(file_handler)

# logger.debug("Hello World!")
# LoggingSetting - END

def Logger(*args):
    message = ""
    for a in args:
        message += str(a) + " "
    logger.debug(message)

def ListLogger(*args):
    message = ""
    print(args)
    for msg in args[0] :
        message += str(msg) + " "
        logger.debug(message)
        message = ""

