import logging


def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%Y-%m-%d %H:%M:%S,%%(msecs)03d %(levelname)s [%(name)s:%(funcName)s] %(message)s"
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
