import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from api_to_dataframe import ClientBuilder, RetryStrategies
from api_to_dataframe.models.get_data import GetData


@pytest.fixture
def mock_response():
    """Fixture que retorna um mock de resposta da API."""
    mock = MagicMock()
    mock.json.return_value = {
        "USDBRL": {
            "code": "USD",
            "codein": "BRL",
            "name": "Dólar Americano/Real Brasileiro",
            "high": "5.50",
            "low": "5.45",
            "varBid": "0.01",
            "pctChange": "0.18",
            "bid": "5.48",
            "ask": "5.49",
            "timestamp": "1610000000",
            "create_date": "2021-01-01 00:00:00"
        }
    }
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def client_builder():
    """Fixture que retorna uma instância de ClientBuilder com um endpoint mockado."""
    return ClientBuilder(
        endpoint="https://api.example.com/data",
        headers={"Content-Type": "application/json"},
        retry_strategy=RetryStrategies.NO_RETRY_STRATEGY,
        retries=3,
        initial_delay=1,
        connection_timeout=5
    )


def test_constructor_raises():
    """Testa as validações do construtor."""
    with pytest.raises(ValueError):
        ClientBuilder(endpoint="")

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", retries=-1)

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", initial_delay=-1)

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", connection_timeout=-1)

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", retries="")

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", initial_delay="")

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="https://api.example.com", connection_timeout="")


def test_constructor_with_headers():
    """Testa a inicialização com headers personalizados."""
    custom_headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    client = ClientBuilder(
        endpoint="https://api.example.com",
        headers=custom_headers
    )
    assert client.headers == custom_headers


def test_constructor_with_retry_strategy():
    """Testa a inicialização com estratégia de retry personalizada."""
    client = ClientBuilder(
        endpoint="https://api.example.com",
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=5,
        initial_delay=2
    )
    assert client.retry_strategy == RetryStrategies.LINEAR_RETRY_STRATEGY
    assert client.retries == 5
    assert client.delay == 2


@patch('requests.get')
def test_get_api_data_success(mock_get, client_builder, mock_response):
    """Testa o método get_api_data com sucesso."""
    # Configura o mock
    mock_get.return_value = mock_response
    
    # Chama o método
    result = client_builder.get_api_data()
    
    # Verifica se o método foi chamado corretamente
    mock_get.assert_called_once_with(
        client_builder.endpoint,
        timeout=client_builder.connection_timeout,
        headers=client_builder.headers
    )
    
    # Verifica o resultado
    assert isinstance(result, dict)
    assert "USDBRL" in result


def test_api_to_dataframe():
    """Testa o método estático api_to_dataframe."""
    # Dados de teste no formato esperado pelo método
    test_data = {
        "id": [1, 2],
        "name": ["Item 1", "Item 2"],
        "value": [10.5, 20.5]
    }
    
    # Converte para DataFrame
    df = ClientBuilder.api_to_dataframe(test_data)
    
    # Verifica o resultado
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["id", "name", "value"]


@patch('requests.get')
def test_get_api_data_http_error(mock_get, client_builder):
    """Testa o tratamento de erros HTTP."""
    # Configura o mock para levantar uma exceção
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Erro 404")
    mock_get.return_value = mock_response
    
    # Verifica se a exceção é levantada
    with pytest.raises(requests.exceptions.HTTPError):
        client_builder.get_api_data()


@patch('requests.get')
def test_get_api_data_connection_error(mock_get, client_builder):
    """Testa o tratamento de erros de conexão."""
    # Configura o mock para levantar uma exceção de conexão
    mock_get.side_effect = requests.exceptions.ConnectionError("Erro de conexão")
    
    # Verifica se a exceção é levantada
    with pytest.raises(requests.exceptions.ConnectionError):
        client_builder.get_api_data()
