from os import environ
import pytest
from logging import getLogger
from unipile_sdk import Client
from unipile_sdk.client import ClientOptions

logger = getLogger(__name__)


def pytest_addoption(parser):
    """
    Add custom command-line option to run messaging tests
    """
    parser.addoption(
        "--with-activities",
        action="store_true",
        default=False,
        help="Run tests with activities",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "activities: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    """
    Filter tests based on the --messaging option
    """
    if not config.getoption("--with-activities"):
        # --messaging not given in cli: skip messaging tests
        skip_messaging = pytest.mark.skip(
            reason="use --with-activities to run"
        )
        for item in items:
            if "activities" in item.keywords:
                item.add_marker(skip_messaging)


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
