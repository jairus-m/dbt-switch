import logging.config
import sys

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        }
    },
    "loggers": {
        __name__: {"handlers": ["console"], "level": "INFO", "propagate": True}
    },
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
