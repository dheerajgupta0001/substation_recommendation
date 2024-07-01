import logging
from logging.handlers import RotatingFileHandler
from logging import LoggerAdapter
import os
import zipfile
from os.path import basename

loggerAdapter = None

def rotator(source, dest):
    zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED).write(source, basename(source))
    os.remove(source)


def initFileLogger(name: str, fPath: str, backupCount: int, maxLogFileMb: int) -> LoggerAdapter:
    global loggerAdapter
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # streamHandler = logging.StreamHandler()
    fileHandler = RotatingFileHandler(fPath, backupCount=backupCount, maxBytes=1024*maxLogFileMb)
    fileHandler.namer = lambda name: name.replace(".log", "") + ".zip"
    fileHandler.rotator = rotator
    streamFormatter = logging.Formatter("%(asctime)s::%(levelname)s::%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # streamHandler.setFormatter(streamFormatter)
    fileHandler.setFormatter(streamFormatter)
    # logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    loggerAdapter = logging.LoggerAdapter(logger, extra={})
    return loggerAdapter

def getFileLogger():
    global loggerAdapter
    return loggerAdapter