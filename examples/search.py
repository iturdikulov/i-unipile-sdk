#!/usr/bin/env python3

# Before running, set the following environment variables (sh and derivatives
# like bash, zsh, etc.):
#
# export UNIPILE_ACCESS_TOKEN="your_api_key_here"
# export UNIPILE_BASE_URL="your_base_url_here"
# export UNIPILE_ACCOUNT="your_account_id_here"

from os import environ

from unipile_sdk import Client
from unipile_sdk.models import LinkedinSearchPayload
from unipile_sdk.helpers import iterate_paginated_api
from unipile_sdk.client import ClientOptions


# Configure the client
options = ClientOptions(
    auth=environ["UNIPILE_ACCESS_TOKEN"],
    base_url=f'https://{environ["UNIPILE_BASE_URL"]}',
    default_account_id=environ["UNIPILE_ACCOUNT"],
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
