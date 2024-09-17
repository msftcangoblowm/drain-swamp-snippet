"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

Logging fixtures

"""

import logging
import logging.config
import sys

import pytest


@pytest.fixture
def get_logger(caplog):
    """Get logger"""

    def _func(app_name, is_debug=False):
        """Boilerplate setup for logging

        :param app_name: dotted path to module
        :type app_name: str
        :param is_debug: Default False. True to use a more verbose formatter
        :type is_debug: bool | None
        :returns: logger
        :rtype: logging.Logger
        """
        IS_TESTING = "pytest" in sys.modules
        formatting = "verbose_with_color" if is_debug else "simple"
        # py39+ Cannot have LOGGING.loggers.root
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "{levelname} {name}: {message}",
                    "style": "{",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": formatting,
                },
                "null": {
                    "class": "logging.NullHandler",
                },
            },
            "loggers": {
                "django.server": {  # Suppress django HTTP logging because we do it in a middleware
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": IS_TESTING,
                },
                app_name: {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": IS_TESTING,
                },
            },
        }

        LOGGING["loggers"][app_name]["propagate"] = True
        logging.config.dictConfig(LOGGING)
        logger = logging.getLogger(name=app_name)
        logger.addHandler(hdlr=caplog.handler)
        caplog.handler.level = logger.level

        return logger

    return _func


@pytest.fixture()
def has_logging_occurred():
    """Display caplog capture text.

    Usage

    .. code-block: text

       import pytest
       import logging
       import logging.config
       from drain_swamp.constants import g_app_name, LOGGING

       def test_something(caplog, has_logging_occurred):
           LOGGING['loggers'][g_app_name]['propagate'] = True
           logging.config.dictConfig(LOGGING)
           logger = logging.getLogger(name=g_app_name)
           logger.addHandler(hdlr=caplog.handler)
           caplog.handler.level = logger.level
           assert has_logging_occurred(caplog)

    .. seealso::

       https://github.com/pytest-dev/pytest/discussions/11011
       https://github.com/thebuzzstop/pytest_caplog/tree/master
       `pass params fixture <https://stackoverflow.com/a/44701916>`_

    """

    def _func(caplog) -> bool:
        """Check if there is at least one log message. Print log messages.

        :returns: True if logging occurred otherwise False
        :rtype: bool
        """
        print("\nCAPLOG:")
        output = caplog.text.rstrip("\n").split(sep="\n")
        if output == [""]:
            print("Nothing captured")
            return False
        for i in range(len(output)):
            print(f"{i}: {output[i]}")
        return True

    return _func
