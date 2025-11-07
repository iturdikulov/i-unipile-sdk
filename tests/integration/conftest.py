from os import environ
import pytest
from logging import getLogger
from unipile_sdk import Client
from unipile_sdk.client import ClientOptions

logger = getLogger(__name__)


@pytest.fixture()
def comm_client():
    options = ClientOptions(
        auth=environ["UNIPILE_ACCESS_TOKEN"],
        base_url=f"https://{environ['UNIPILE_BASE_URL']}",
        default_account_id=environ["UNIPILE_ACCOUNT"],
    )
    return Client(options)


@pytest.fixture
def user_urn_to_retrieve():
    """
    Bill Gates URN: https://www.linkedin.com/in/williamhgates
    """
    return "ACoAAA8BYqEBCGLg_vT_ca6mMEqkpp9nVffJ3hc"


@pytest.fixture
def user_urn_to_invite():
    """
    Bill Gates URN: https://www.linkedin.com/in/williamhgates
    """
    return "ACoAAA8BYqEBCGLg_vT_ca6mMEqkpp9nVffJ3hc"

@pytest.fixture
def search_keyword():
    return "microsoft"
