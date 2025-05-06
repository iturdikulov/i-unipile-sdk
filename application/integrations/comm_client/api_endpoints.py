"""
Unipile API endpoints.
"""

# WARN: use ranged limits type

from datetime import datetime
from typing import TYPE_CHECKING, Any

from typing_extensions import Annotated
from pydantic import StringConstraints

from application.config import Config
from application.integrations.comm_client.models import (
    Accounts,
    ChatAttendeesResponse,
    ChatsMessagesResponse,
    ChatsResponse,
    ChatsSendMessageResponse,
    ChatsStartedResponse,
    CommonSearchParameter,
    LinkedinAccountsConnect,
    LinkedinAccountsConnectResponse,
    LinkedinCompanyProfile,
    LinkedinSalesNavSearchPayload,
    LinkedinSearchParametersResponse,
    LinkedinSearchPayload,
    LinkedinURLSearchPayload,
    LinkedinUserMe,
    LinkedinUserProfile,
    LinkedinUsersInvitePayload,
    LinkedinUsersInviteResponse,
    SearchResponse,
    UsersRelationsResponse,
)

from .typing import AccountLinkType, AccountProvider, SyncAsync

if TYPE_CHECKING:  # pragma: no cover
    from .client import BaseClient


class Endpoint:
    def __init__(self, parent: "BaseClient") -> None:
        self.parent = parent

class UsersEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def connect(
        self,
        payload: LinkedinAccountsConnect,
    ) -> LinkedinAccountsConnectResponse:
        """
        Link to Uniple an account of the given type and provider.

        Endpoint documentation: https://developer.unipile.com/reference/accountscontroller_createaccount
        """

        return LinkedinAccountsConnectResponse(
            **self.parent.request(
                path="accounts",
                method="POST",
                body=payload.model_dump(exclude_none=True),
            )
        )

    def me(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
    ) -> LinkedinUserMe:
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

    def retrieve(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        identifier: Annotated[str, StringConstraints(min_length=1)],
    ) -> LinkedinUserProfile:
        """
        Retrieve the profile of a user. Ensure careful implementation of this action and consult
        provider limits and restrictions:
        https://developer.unipile.com/docs/provider-limits-and-restrictions

        Endpoint documentation: https://developer.unipile.com/reference/userscontroller_getprofilebyidentifier
        """
        return LinkedinUserProfile(
            **self.parent.request(
                path=f"users/{identifier}/",  # NOTE: that slash is required, otherwise it will return 301
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

    def relations(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        filter: str | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> UsersRelationsResponse:
        """
        Returns a list of all the relations of an account. Ensure careful implementation of this
        action and consult provider limits and restrictions:
        https://developer.unipile.com/docs/provider-limits-and-restrictions

        Endpoint documentation: https://developer.unipile.com/reference/userscontroller_getrelations
        """
        return UsersRelationsResponse(
            **self.parent.request(
                path="users/relations",
                method="GET",
                query={
                    "account_id": account_id,
                    "filter": filter,
                    "cursor": cursor,
                    "limit": limit,
                },
            )
        )


class MessagesEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def chat_attendees(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        cursor: str | None = None,
        limit: int = 100,
    ):
        """
        Returns a list of messaging attendees. Some optional parameters are available to filter the
        results.

        Endpoint documentation: https://developer.unipile.com/reference/chatattendeescontroller_listallattendees
        """
        return ChatAttendeesResponse(
            **self.parent.request(
                path="chat_attendees",
                method="GET",
                query={
                    "account_id": account_id,
                    "cursor": cursor,
                    "limit": limit,
                },
            )
        )

    # WARN: add befor/after support
    def list_chats_by_attendee(
        self,
        attendee_id: str,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        cursor: str|None = None,
        limit: int = 100
    ):
        """
        Returns a list of chats where a given attendee is involved.

        Endpoint documentation: https://developer.unipile.com/reference/chatattendeescontroller_listchatsbyattendee
        """
        return ChatsResponse(
            **self.parent.request(
                path=f"chat_attendees/{attendee_id}/chats",
                method="GET",
                query={
                    "account_id": account_id,
                    "cursor": cursor,
                    "limit": limit,
                },
            )
        )

    # WARN: add before/after support
    def messages(
        self,
        chat_id: Annotated[str, StringConstraints(min_length=1)],
        sender_id: Annotated[str, StringConstraints(min_length=1)]|None = None,
        cursor: str|None = None,
        limit: int = 100
    ):
        """
        Returns a list of chats where a given attendee is involved.

        Endpoint documentation: https://developer.unipile.com/reference/chatattendeescontroller_listchatsbyattendee
        """
        response = self.parent.request(
                path=f"chats/{chat_id}/messages",
                method="GET",
                query={
                    "sender_id": sender_id,
                    "cursor": cursor,
                    "limit": limit,
                },
            )
        return ChatsMessagesResponse(**response)

    def send_message(
        self,
        chat_id: Annotated[str, StringConstraints(min_length=1)],
        account_id: Annotated[str, StringConstraints(min_length=1)],
        text: str|None = None,  # WARN: need to add restrictions here!
    ) -> ChatsSendMessageResponse:
        """
        Send a message to the given chat with the possibility to link some attachments.

        NOTE: unipile support thread_id (slack messaging), voice_message and video_message, but we
        don't use it, so required parameters are not implemented.

        Endpoint documentation: https://developer.unipile.com/reference/chatscontroller_sendmessageinchat
        """

        return ChatsSendMessageResponse(**self.parent.request(
            path=f"chats/{chat_id}/messages",
            method="POST",
            body={
                "account_id": account_id,
                "text": text,
            }
        ))

    def send_message_to_attendees(
        self,
        attendees_ids: list[Annotated[str, StringConstraints(min_length=1)]],
        account_id: Annotated[str, StringConstraints(min_length=1)],
        text: str|None = None,
    ) -> ChatsStartedResponse:
        """
        Start a new conversation with one or more attendee. ⚠️ Interactive documentation does not
        work for Linkedin specific parameters (child parameters not correctly applied in snippet),
        the correct format is linkedin[inmail] = true, linkedin[api]...

        Endpoint documentation: https://developer.unipile.com/reference/chatscontroller_startnewchat
        """

        return ChatsStartedResponse(**self.parent.request(
            path="chats",
            method="POST",
            body={
                "account_id": account_id,
                "attendees_ids": attendees_ids,
                "text": text,
            }
        ))


class AccountsEndpoint(Endpoint):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def accounts(self, cursor: str|None = None, limit: int = 100) -> Accounts:
        """
        Returns a list of the accounts linked to Unipile.

        Endpoint documentation: https://developer.unipile.com/reference/accountscontroller_listaccounts
        """
        return Accounts(**self.parent.request(
            path="accounts",
            method="GET",
            query={"cursor": cursor, "limit": limit},
        ))

    def delete(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
    ):
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
        payload: LinkedinSearchPayload | LinkedinSalesNavSearchPayload | LinkedinURLSearchPayload,
        cursor: str | None = None,
        limit: int|None = None,
    ) -> SearchResponse:
        """
        Search people and companies from the Linkedin Classic as well as Sales Navigator APIs.
        Check out our Guide with examples to master LinkedIn search :
        https://developer.unipile.com/docs/linkedin-search

        Endpoint documentation: https://developer.unipile.com/reference/linkedincontroller_search
        """

        # Set default limit
        if limit is None:
            is_sales_search = False
            if isinstance(payload, LinkedinSalesNavSearchPayload):
                is_sales_search = True
            elif isinstance(payload, LinkedinURLSearchPayload):
                if payload.url.startswith("https://www.linkedin.com/sales/search"):
                    is_sales_search = True
            limit = (
                Config.LINKEDIN_SEARCH_SALES_LEADS_PER_PAGE
                if is_sales_search
                else Config.LINKEDIN_SEARCH_DEFAULT_LEADS_PER_PAGE
            )

        response = self.parent.request(
            path="linkedin/search",
            method="POST",
            query={"cursor": cursor, "account_id": account_id, "limit": limit},
            body=payload.model_dump(exclude_none=True),
        )
        return SearchResponse(**response)

    def search_param(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        type: CommonSearchParameter,
        keywords: str,
    ) -> LinkedinSearchParametersResponse:
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

    def retrieve_company(
        self,
        account_id: Annotated[str, StringConstraints(min_length=1)],
        identifier: Annotated[str, StringConstraints(min_length=1)],
    ) -> LinkedinCompanyProfile:
        """
        Get a company profile from its name or ID.

        Endpoint documentation: https://developer.unipile.com/reference/linkedincontroller_getcompanyprofile
        """
        return LinkedinCompanyProfile(**self.parent.request(
            path=f"linkedin/company/{identifier}",
            method="GET",
            query={"account_id": account_id},
        ))

