from unipile_sdk.client import Client


def test_accounts(comm_client: Client):
    accounts = comm_client.accounts.accounts(limit=100)
    assert len(accounts.items) > 0 and len(accounts.items) <= 10, (
        "at least one connected account is expected"
    )


def test_duplicate_amount(comm_client: Client):
    duplicates = comm_client.accounts.duplicate_amount()
    assert duplicates >= 0
