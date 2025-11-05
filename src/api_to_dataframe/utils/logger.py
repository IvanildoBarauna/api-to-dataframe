"""Utilities to manage the library logging configuration."""

from __future__ import annotations

import logging
from typing import Iterable, Optional

DEFAULT_LOGGER_NAME = "api-to-dataframe"


logger = logging.getLogger(DEFAULT_LOGGER_NAME)
if not any(isinstance(handler, logging.NullHandler) for handler in logger.handlers):
    logger.addHandler(logging.NullHandler())


def configure_logger(**kwargs) -> logging.Logger:
    """Configure the default logger or replace it with a custom instance.

    This helper avoids applying a global configuration automatically while
    allowing consumers to fine-tune the logger used by the library. The caller
    can provide an existing :class:`logging.Logger` instance or customize the
    default logger by supplying keyword arguments similar to ``logging.basicConfig``.

    Keyword Args:
        logger (logging.Logger, optional):
            Custom logger instance to use across the library.
        level (int, optional):
            Logging level to apply to the default logger.
        handlers (Iterable[logging.Handler], optional):
            Handlers that will replace the current ones of the default logger.
        formatter (logging.Formatter, optional):
            Formatter applied to every handler in the default logger.
        format (str, optional):
            Format string used to build a :class:`logging.Formatter`.
        datefmt (str, optional):
            Date format passed to :class:`logging.Formatter` when ``format`` is
            provided.
        propagate (bool, optional):
            Whether the default logger should propagate messages to ancestor
            loggers.

    Returns:
        logging.Logger: The configured logger instance.

    Raises:
        TypeError: If the provided ``logger`` argument is not a Logger instance.
    """

    global logger  # pylint: disable=global-statement

    custom_logger: Optional[logging.Logger] = kwargs.pop("logger", None)
    if custom_logger is not None:
        if not isinstance(custom_logger, logging.Logger):
            raise TypeError("The 'logger' argument must be an instance of logging.Logger")
        logger = custom_logger
        return logger

    level: Optional[int] = kwargs.get("level")
    if level is not None:
        logger.setLevel(level)

    propagate: Optional[bool] = kwargs.get("propagate")
    if propagate is not None:
        logger.propagate = propagate

    handlers: Optional[Iterable[logging.Handler]] = kwargs.get("handlers")
    if handlers is not None:
        logger.handlers = list(handlers)

    formatter: Optional[logging.Formatter] = kwargs.get("formatter")
    if formatter is None:
        fmt: Optional[str] = kwargs.get("format")
        datefmt: Optional[str] = kwargs.get("datefmt")
        if fmt is not None:
            formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    if formatter is not None:
        for handler in logger.handlers:
            handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    return logger
