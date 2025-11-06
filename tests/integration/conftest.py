import pytest
from logging import getLogger
from unipile_sdk import Client

logger = getLogger(__name__)


@pytest.fixture()
def comm_client():
    return Client()
