import logging
import logbook
from logbook.more import ColorizedStderrHandler
from logstash_formatter import LogstashFormatter

# Set up logging configuration
def setup_logging(config):
    # Create logger
    logger = logging.getLogger('my_app')

    # Set logging level
    logger.level = logging.DEBUG

    # Create Logbook handler
    handler = ColorizedStderrHandler(level=logging.DEBUG)
    handler.formatter = LogstashFormatter()

    # Add handler to logger
    logger.handlers.append(handler)

    # Set up ELK Stack logging
    if config['logging']['elk_stack']['enabled']:
        elk_handler = logbook.SysLogHandler(
            address=(config['logging']['elk_stack']['host'], config['logging']['elk_stack']['port']),
            level=logging.DEBUG
        )
        elk_handler.formatter = LogstashFormatter()
        logger.handlers.append(elk_handler)

    return logger

# Example usage
config = load_config("config.json")
logger = setup_logging(config)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
