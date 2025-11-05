import io
import logging

import pytest

from api_to_dataframe.utils import logger as logger_module
from api_to_dataframe.utils.logger import DEFAULT_LOGGER_NAME, configure_logger, logger


@pytest.fixture(autouse=True)
def restore_logger_state():
    """Restore the original logger configuration after each test run."""

    original_logger = logger_module.logger
    original_handlers = list(original_logger.handlers)
    original_level = original_logger.level
    original_propagate = original_logger.propagate

    yield

    configure_logger(logger=original_logger)
    original_logger.handlers = original_handlers
    original_logger.setLevel(original_level)
    original_logger.propagate = original_propagate


def test_default_logger_is_exposed():
    """Ensure the module exposes the default logger with a NullHandler."""

    assert logger.name == DEFAULT_LOGGER_NAME
    assert any(isinstance(handler, logging.NullHandler) for handler in logger.handlers)


def test_configure_logger_accepts_custom_instance():
    """Ensure configure_logger can swap the default logger instance."""

    custom_logger = logging.getLogger("api-to-dataframe-custom")
    configured_logger = configure_logger(logger=custom_logger)

    assert configured_logger is custom_logger


def test_configure_logger_applies_custom_format():
    """Ensure configure_logger applies the provided formatter to handlers."""

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    format_str = "%(levelname)s -- %(message)s"

    configured_logger = configure_logger(
        handlers=[handler],
        level=logging.INFO,
        format=format_str,
    )
    configured_logger.info("custom message")
    handler.flush()

    log_output = stream.getvalue().strip()
    assert log_output == "INFO -- custom message"
