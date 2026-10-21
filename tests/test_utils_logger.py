import logging
import pytest
from api_to_dataframe.utils.logger import logger


def test_logger_exists():
    """Test logger is properly initialized."""
    assert logger.name == "api-to-dataframe"
    # Verificar apenas que é uma instância de logger, sem verificar propriedades específicas
    assert isinstance(logger, logging.Logger)


def test_logger_can_log():
    """Test logger can log messages without errors."""
    # Tentativa de logging não deve lançar exceções
    try:
        logger.info("Test message")
        logger.warning("Test warning")
        logger.error("Test error")
        # Se chegamos aqui, não houve exceções
        assert True
    except Exception as e:
        assert False, f"Logger raised an exception: {e}"
