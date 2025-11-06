from os import environ

def test_init(comm_client):
    me = comm_client.users.me(account_id=environ["UNIPILE_ACCOUNT"])
    assert me is not None
