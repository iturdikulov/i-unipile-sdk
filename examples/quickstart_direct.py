from unipile_sdk import Client
from unipile_sdk.client import ClientOptions

# Recommended: Configure the client directly
options = ClientOptions(
    auth="your_api_key_here",
    base_url="https://api.unipile.com",
    default_account_id="your_default_account_id_here",
)

client = Client(options=options)

# Get your user information
me = client.users.me()
print(f"Hello, {me.name}!")
