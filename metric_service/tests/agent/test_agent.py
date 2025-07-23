import json
import pytest
from unittest.mock import patch, MagicMock

import agent

@pytest.fixture
def mock_psutil():
    with patch('agent.psutil') as mock:
        mock.cpu_count.return_value = 4
        mock.virtual_memory.return_value.total = 8000000000
        mock.virtual_memory.return_value.percent = 65.5
        mock.virtual_memory.return_value.available = 2800000000
        yield mock


@patch('agent.pika.BlockingConnection')
def test_send_metrics(mock_pika, mock_psutil):
    mock_channel = MagicMock()
    mock_connection = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_pika.return_value = mock_connection

    agent.send_metrics()

    mock_channel.queue_declare.assert_called_once_with(queue='metrics')

    assert mock_channel.basic_publish.call_count == 10

    call_args = mock_channel.basic_publish.call_args
    body = call_args[1]['body']
    message = json.loads(body)

    assert 'CPU' in message
    assert 'Virtual Memory' in message
    assert 'Used RAM' in message
    assert 'Memory Left' in message

    assert isinstance(message['CPU'], int)
    assert isinstance(message['Virtual Memory'], int)
    assert isinstance(message['Used RAM'], float)
    assert isinstance(message['Memory Left'], float)
