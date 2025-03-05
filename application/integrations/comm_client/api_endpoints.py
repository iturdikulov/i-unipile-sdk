"""
Unipile API endpoints.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from application.integrations.comm_client.models import (
    CommonSearchParameter,
    LinkedinSearchParametersResponse,
    LinkedinSearchPayload,
    LinkedinUserMe,
    LinkedinUserProfile,
    LinkedinUsersInvitePayload,
    LinkedinUsersInviteResponse,
)

from .helpers import pick
from .typing import AccountLinkType, AccountProvider, SyncAsync

if TYPE_CHECKING:  # pragma: no cover
    from .client import BaseClient


class Endpoint:
    def __init__(self, parent: "BaseClient") -> None:
        self.parent = parent

class UsersEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def me(self, account_id: str) -> LinkedinUserMe:
        """
        Retrieve informations about account owner.

        Endpoint documentation: https://developer.unipile.com/reference/userscontroller_getaccountownerprofile
        """
        return LinkedinUserMe(
            **self.parent.request(
                path="users/me",
                method="GET",
                query={"account_id": account_id},
            )
        )

    def retrieve(self, identifier: str, account_id: str) -> LinkedinUserProfile:
        """
        Retrieve the profile of a user. Ensure careful implementation of this action and consult
        provider limits and restrictions:
        https://developer.unipile.com/docs/provider-limits-and-restrictions

        Endpoint documentation: https://developer.unipile.com/reference/userscontroller_getprofilebyidentifier
        """
        return LinkedinUserProfile(
            **self.parent.request(
                path=f"users/{identifier}",
                method="GET",
                query={"account_id": account_id},
            )
        )

    def invite(
        self,
        payload: LinkedinUsersInvitePayload,
    ) -> LinkedinUsersInviteResponse:
        """
        Send an invitation to add someone to your contacts. Ensure careful implementation of this
        action and consult provider limits and restrictions:
        https://developer.unipile.com/docs/provider-limits-and-restrictions

        Endpoint documentation: https://developer.unipile.com/reference/userscontroller_adduserbyidentifier
        """

        return LinkedinUsersInviteResponse(
            **self.parent.request(
                path="users/invite",
                method="POST",
                body=payload.model_dump(exclude_none=True),
            )
        )

class MessagesEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def attendee_messages(self):
        """
        """
        # https://developer.unipile.com/reference/chatattendeescontroller_listmessagesbyattendee
        pass

    def send_message(self):
        """
        """
        # https://developer.unipile.com/reference/chatscontroller_sendmessageinchat
        pass

# def test_get_chat_details():
#     for chat in chats["items"]:
#         chat_id = chat["id"]
#         chat_details = requests.get(f"https://{UNIPILE_DSN}/api/v1/chats/{chat_id}",
#                                     headers=headers).json()
#         pprint(chat_details)
#         messages = requests.get(f"https://{UNIPILE_DSN}/api/v1/chats/{chat_id}/messages",
#                             headers=headers,
#                             ).json()
#         pprint(messages)
#         break

# def send_message():
#     for item in chats["items"]:
#         # Send message
#         response = requests.post(f"https://{UNIPILE_DSN}/api/v1/chats/{item['id']}/messages",
#         headers={
#             "accept": "application/json",
#             "X-API-KEY": UNIPILE_ACCESS_TOKEN,
#         }, data={"text" : "Thank you for connection."})
#         print(response.text)
#         break

class AccountsEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def accounts(self, cursor: str|None = None, limit: int = 100) -> SyncAsync[Any]:
        """
        Returns a list of the accounts linked to Unipile.

        Endpoint documentation: https://developer.unipile.com/reference/accountscontroller_listaccounts
        """
        return self.parent.request(
            path="accounts",
            method="GET",
        )

    def delete(self, account_id: str):
        return self.parent.request(
            path=f"accounts/{account_id}",
            method="DELETE",
        )

class HostedEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def link(self,
             expiries_on: datetime,
             api_url: str,
             success_redirect_url: str|None = None,
             failure_redirect_url: str|None = None,
             notify_url: str|None = None,
             name: str|None = None,
             type: AccountLinkType = "create",
             providers: list[AccountProvider] = ["LINKEDIN"]) -> SyncAsync[Any]:
        """
        Create a url which redirect to Unipile's hosted authentication to connect or reconnect an account.

        Endpoint documentation: https://developer.unipile.com/reference/hostedcontroller_requestlink
        """

        expiries_on_str = f"{expiries_on.strftime('%Y-%m-%dT%H:%M:%S')}.{str(expiries_on.microsecond)[:3]}Z"

        payload = {
            "type": type,
            "providers": providers,
            "api_url": api_url,
            "expiresOn": expiries_on_str,
            "notify_url": notify_url,
            "name": name,
            "success_redirect_url": success_redirect_url,
            "failure_redirect_url": failure_redirect_url,
        }

        return self.parent.request(
            path="hosted/accounts/link",
            method="POST",
            body=payload
        )

    def retrieve(self):
        pass

class SearchEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def search(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        payload: LinkedinSearchPayload|LinkedinURLSearchPayload,
        cursor: str | None = None,
        limit: int = 10,
    ) -> SearchResponse:
        """
        Search people and companies from the Linkedin Classic as well as Sales Navigator APIs.
        Check out our Guide with examples to master LinkedIn search :
        https://developer.unipile.com/docs/linkedin-search

        Endpoint documentation: https://developer.unipile.com/reference/linkedincontroller_search
        """
        response = self.parent.request(
            path="linkedin/search",
            method="POST",
            query={"cursor": cursor, "account_id": account_id, "limit": limit},
            body=payload.model_dump(exclude_none=True),
        )
        return SearchResponse(**response)

    def search_param(self, account_id: str, type: CommonSearchParameter, keywords: str) -> LinkedinSearchParametersResponse:
        """
        LinkedIn doesn't accept raw text as search parameters, but IDs. This route will help you
        get the right IDs for your inputs. Check out our Guide with examples to master LinkedIn
            search : https://developer.unipile.com/docs/linkedin-search

        Endpoint documentation: https://developer.unipile.com/reference/linkedincontroller_getsearchparameterslist
        """
        return LinkedinSearchParametersResponse(**self.parent.request(
            path="linkedin/search/parameters",
            method="GET",
            query={"account_id": account_id, "type": type.value, "keywords": keywords},
        ))
