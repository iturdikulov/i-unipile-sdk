import pytest
from unipile_sdk.client import Client


def test_me(comm_client: Client):
    assert comm_client.users.me() is not None


def test_retrieve_user(comm_client: Client, ln_default_user_urn: str):
    user_info = comm_client.users.retrieve(identifier=ln_default_user_urn)
    assert user_info.connections_count and user_info.connections_count > 0, (
        f"Expected connections_count for {ln_default_user_urn} URN to be greater than 0, but got {user_info.connections_count or 0}"
    )


@pytest.mark.activities
def test_invite_user(comm_client: Client, ln_invite_user_urn: str):
    connection_info = comm_client.users.invite(provider_id=ln_invite_user_urn)
    assert connection_info is not None


def test_user_relations(comm_client: Client):
    relations = comm_client.users.relations()
    assert len(relations.items) > 0, (
        f"Expected relations.items for current user to have at least one relation, but got {len(relations.items)}"
    )
