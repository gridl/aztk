import sys
import logging

log = logging.getLogger("aztk.node-agent")

DEFAULT_FORMAT = '%(message)s'

def setup_logging():
    print("Setup logger")
    log.setLevel(logging.INFO)
    logging.basicConfig(stream=sys.stdout,format=DEFAULT_FORMAT)
