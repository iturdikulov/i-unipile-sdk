from os import environ

from unipile_sdk import Client
from unipile_sdk.models import LinkedinSearchPayload
from unipile_sdk.helpers import iterate_paginated_api
from unipile_sdk.client import ClientOptions


put_here_your_unipile_access_token = environ["UNIPILE_ACCESS_TOKEN"]
put_here_your_unipile_base_url = "https://" + environ["UNIPILE_BASE_URL"]
put_here_your_unipile_account = environ["UNIPILE_ACCOUNT"]


# Recommended: Configure the client directly
options = ClientOptions(
    auth=put_here_your_unipile_access_token,
    base_url=put_here_your_unipile_base_url,
    default_account_id=put_here_your_unipile_account,
)

client = Client(options=options)

# Search for LinkedIn profiles
payload = LinkedinSearchPayload(
    api="classic", category="people", keywords="Software Engineer, Programmer"
)

for person in iterate_paginated_api(
    client.ln_search.search, payload=payload, max_total=10
):
    print(f"Found Person: {person.name} ({person.id})")
