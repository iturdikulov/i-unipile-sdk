# Unipile Python SDK

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Integrate our email and messaging APIs to enable your users to converse
> directly through LinkedIn, Gmail, and WhatsApp, and trigger engagement actions
> like follow-ups, invites, or scheduling.

Fully functional unofficial unipile SDK.


> An unofficial, fully functional Python SDK for the Unipile API. Integrate email and messaging APIs to enable seamless conversations via LinkedIn, Gmail, WhatsApp, and more. Trigger actions like follow-ups, invites, or scheduling with ease.

The SDK provides both synchronous (`Client`) and asynchronous (`AsyncClient`) interfaces for interacting with Unipile's REST API. It handles authentication, pagination, error management, and LinkedIn-specific features like profile retrieval, search, and messaging.

Key features:

- **Account Management**: Connect, list, and verify LinkedIn (and other provider) accounts.
- **User Profiles**: Retrieve profiles, send invites, and fetch relations.
- **Messaging**: Send messages, list chats, retrieve attendees and message history.
- **Search**: Advanced LinkedIn searches (Classic, Sales Navigator) with filtering and pagination.
- **Hosted Authentication**: Generate links for user account linking.
- **Error Handling**: Custom exceptions for API responses, timeouts, and HTTP errors.
- **Type Safety**: Built with Pydantic models for request/response validation.

For official documentation, visit [Unipile Developer Docs](https://developer.unipile.com/docs/getting-started).

## Installation

Install the SDK using [uv](https://docs.astral.sh/uv/), it's recommended for fast dependency resolution

```bash
# Using uv (preferred)
uv add FUTURE_PROJECT_NAME

# Alternative installation method, using pip
pip install FUTURE_PROJECT_NAME
```

Set environment variables for authentication:

```bash
export UNIPILE_BASE_URL="api.unipile.com"
export UNIPILE_ACCESS_TOKEN="your_api_key_here"
```

## Usage

### Basic Setup

Import the client and create an instance. The SDK defaults to the production Unipile API.

```python
from unipile_sdk import Client

# Synchronous client
client = Client()
# Or with custom options
client = Client(auth="your_token", base_url="https://api.unipile.com", timeout_ms=30000)
```

For async usage:

```python
import asyncio
from unipile_sdk import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Your async code here

asyncio.run(main())
```

### Account Connection (LinkedIn Example)

Connect a LinkedIn account using cookies/tokens:

```python
from unipile_sdk import Client
from unipile_sdk.models import LinkedinAccountsConnect

client = Client()

payload = LinkedinAccountsConnect(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    access_token="your_li_at_token",
    premium_token="your_li_a_token",  # Optional for Premium features
    country="US"
)

response = client.accounts.connect(payload)
print(f"Account ID: {response.account_id}")
```

List connected accounts:

```python
accounts = client.accounts.accounts(limit=50)
for account in accounts.items:
    print(f"Account: {account.name} (ID: {account.id})")
```

### User Profile Retrieval

Fetch a user's profile by identifier (e.g., public profile URL or ID):

```python
profile = client.users.retrieve(
    account_id="your_account_id",
    identifier="john-doe-123",
    linkedin_section="experience"  # Optional: Filter sections
)
print(f"Headline: {profile.headline}")
print(f"Experience: {profile.work_experience}")
```

Send a connection invite:

```python
from unipile_sdk.models import LinkedinUsersInvitePayload

payload = LinkedinUsersInvitePayload(
    provider_id="target_user_provider_id",
    account_id="your_account_id",
    message="Let's connect!",
    user_email="target@example.com"  # Optional for LinkedIn
)

response = client.users.invite(payload)
print(f"Invitation ID: {response.invitation_id}")
```

### Messaging

List chats for an attendee:

```python
chats = client.messages.list_chats_by_attendee(
    attendee_id="attendee_id",
    account_id="your_account_id",
    limit=20
)
for chat in chats.items:
    print(f"Chat: {chat.name} (Unread: {chat.unread_count})")
```

Send a message:

```python
response = client.messages.send_message(
    chat_id="chat_id",
    account_id="your_account_id",
    text="Hello from Unipile SDK!"
)
print(f"Message ID: {response.message_id}")
```

Start a new chat with attendees:

```python
response = client.messages.send_message_to_attendees(
    attendees_ids=["attendee_id1", "attendee_id2"],
    account_id="your_account_id",
    text="Starting a new conversation!"
)
print(f"Chat ID: {response.chat_id}, Message ID: {response.message_id}")
```

### LinkedIn Search

Search for people using Classic API:

```python
from unipile_sdk.models import LinkedinSearchPayload, NetworkDistanceEnum

payload = LinkedinSearchPayload(
    keywords="Software Engineer",
    location=["102713980"],  # Location ID (use search_param to get IDs)
    network_distance=[NetworkDistanceEnum.FIRST, NetworkDistanceEnum.SECOND],
    limit=25
)

results = client.ln_search.search(
    account_id="your_account_id",
    payload=payload,
    limit=10  # Global limit after filtering
)
for person in results.items:
    print(f"Name: {person.name}, Headline: {person.headline}, Distance: {person.network_distance}")
```

Get search parameters (e.g., location IDs):

```python
params = client.ln_search.search_param(
    account_id="your_account_id",
    type="LOCATION",
    keywords="New York"
)
for param in params.items:
    print(f"Location: {param.title} (ID: {param.id})")
```

For Sales Navigator:

```python
from unipile_sdk.models import LinkedinSalesNavSearchPayload

payload = LinkedinSalesNavSearchPayload(
    keywords="Marketing Manager",
    location={"include": ["102713980"]},
    industry={"include": ["industry_id"]},
    network_distance=[1, 2]
)

results = client.ln_search.search(account_id="your_account_id", payload=payload)
```

### Hosted Account Linking

Generate a hosted auth link:

```python
from datetime import datetime, timedelta
from unipile_sdk.models import AccountLinkType, AccountProvider

link_data = client.hosted.link(
    expiries_on=datetime.utcnow() + timedelta(hours=1),
    api_url="https://yourapp.com/api/callback",
    success_redirect_url="https://yourapp.com/success",
    providers=[AccountProvider.LINKEDIN],
    type=AccountLinkType.create
)
print(f"Hosted Link: {link_data['url']}")
```

### Error Handling

The SDK raises custom exceptions:

```python
from unipile_sdk.errors import APIResponseError, RequestTimeoutError

try:
    # API call
    pass
except APIResponseError as e:
    print(f"API Error: {e.error} - {e.detail}")
except RequestTimeoutError:
    print("Request timed out")
except Exception as e:
    print(f"Unexpected: {e}")
```

## Project Structure

- **`__init__.py`**: Package entry point; exports main classes (`Client`, `AsyncClient`, `APIResponseError`).
- **`api_endpoints.py`**: Defines endpoint classes (e.g., `UsersEndpoint`, `MessagesEndpoint`, `SearchEndpoint`) for API interactions.
- **`client.py`**: Core `BaseClient`, `Client` (sync), and `AsyncClient` (async) implementations; handles HTTP requests with httpx.
- **`errors.py`**: Custom exceptions (`APIResponseError`, `HTTPResponseError`, `RequestTimeoutError`).
- **`helpers.py`**: Utilities for pagination (`iterate_paginated_api`), URL parsing, and response validation.
- **`logging.py`**: Configures console logging for the SDK.
- **`models.py`**: Pydantic models for requests/responses (e.g., `LinkedinUserProfile`, `SearchResponse`, error types).
- **`typing.py`**: Custom types (e.g., `SyncAsync`, `AccountProvider`).
- **`README.md`**: This documentation.

## Dependencies

The SDK relies on:
- `httpx` (>=0.27.0): For HTTP requests (sync/async).
- `pydantic` (>=2.5.0): For data validation and models.
- `typing-extensions`: For type hints.
- Standard library: `datetime`, `json`, `logging`, `urllib.parse`, `uuid`.

No additional runtime dependencies beyond these. Install via the package manager as shown in Installation.

## Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure code adheres to PEP 8, add tests for new features, and update documentation. For major changes, open an issue first to discuss.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
