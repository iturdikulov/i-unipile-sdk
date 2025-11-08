from os import environ, getenv
from random import choice
import pytest
from dotenv import find_dotenv, load_dotenv
from logging import getLogger
from unipile_sdk import Client
from unipile_sdk.client import ClientOptions

logger = getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    env_file = find_dotenv(".tests.env")
    load_dotenv(env_file)


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
def ln_default_user_urn():
    """
    Default LinkedIn urn to get some data
    """
    return environ["UNIPILE_LN_DEFAULT_USER_URN"]


@pytest.fixture
def user_urn_to_invite():
    """
    URN for a user to invite on LinkedIn
    """
    return environ["UNIPILE_LN_DEFAULT_USER_URN"]


@pytest.fixture
def user_urn_to_message():
    """
    URN for a user to send messages to
    """
    return getenv("UNIPILE_LN_USER_URN_TO_MESSAGE")


@pytest.fixture
def search_keyword():
    return "microsoft"


@pytest.fixture
def ln_sending_message():
    """
    Default LinkedIn default sending message
    """
    return choice(
        (
            "Thank you for the connection.",
            "Thank you for connecting with me.",
            "Thank you for connecting!",
            "Thank you for your connection request.",
        )
    )
