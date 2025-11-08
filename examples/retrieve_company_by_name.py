#!/usr/bin/env python3

# Before running, set the following environment variables (sh and derivatives
# like bash, zsh, etc.):
#
# export UNIPILE_ACCESS_TOKEN="your_api_key_here"
# export UNIPILE_BASE_URL="your_base_url_here"
# export UNIPILE_ACCOUNT="your_account_id_here"

from os import environ
from unipile_sdk import Client
from unipile_sdk.client import ClientOptions

# Configure the client
options = ClientOptions(
    auth=environ["UNIPILE_ACCESS_TOKEN"],
    base_url=f'https://{environ["UNIPILE_BASE_URL"]}',
    default_account_id=environ["UNIPILE_ACCOUNT"],
)
client = Client(options=options)

# Fetch company details using its name.
company = client.ln_search.retrieve_company(identifier="LinkedIn")
print(f"Company: {company.name} ({company.id})")
