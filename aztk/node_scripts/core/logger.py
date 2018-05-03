import logging

log = logging.getLogger("aztk")

DEFAULT_FORMAT = '%(message)s'

def setup_logging():
    log.setLevel(logging.INFO)
    logging.basicConfig(format=DEFAULT_FORMAT)
