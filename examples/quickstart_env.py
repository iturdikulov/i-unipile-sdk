from unipile_sdk import Client

# Alternative: Configure the client using environment variables
# Make sure to set the following environment variables:
#
# export UNIPILE_BASE_URL="api.unipile.com"
# export UNIPILE_ACCESS_TOKEN="your_api_key_here"
# export UNIPILE_ACCOUNT="your_default_account_id_here"

# The client will automatically pick up the environment variables
client = Client()

# Get your user information
me = client.users.me()
print(f"Hello, {me.name}!")
