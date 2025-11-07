from unipile_sdk.client import Client
from datetime import datetime, timedelta

def test_link(comm_client: Client):
    expiries_on = datetime.utcnow() + timedelta(days=1)
    link = comm_client.hosted.link(
        name="Test Link Name",
        expiries_on=expiries_on,
    )
    assert link is not None
