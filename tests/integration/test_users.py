from unipile_sdk.client import Client


def test_me(comm_client: Client):
    assert comm_client.users.me() is not None


def test_retrieve_user(comm_client: Client, user_urn_to_retrieve: str):
    user_info = comm_client.users.retrieve(identifier=user_urn_to_retrieve)
    assert user_info.connections_count and user_info.connections_count > 0, (
        f"Expected connections_count for {user_urn_to_retrieve} URN to be greater than 0, but got {user_info.connections_count or 0}"
    )


def test_invite_user(comm_client: Client, user_urn_to_invite: str):
    connection_info = comm_client.users.invite(provider_id=user_urn_to_invite)
    assert connection_info is not None


def test_user_relations(comm_client: Client):
    relations = comm_client.users.relations()
    assert len(relations.items) > 0, (
        f"Expected relations.items for current user to have at least one relation, but got {len(relations.items)}"
    )
