from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class PostsGetLGetPostQuery(BaseModel):
        account_id: str
class PostsGetLListAllCommentsQuery(BaseModel):
        cursor: Optional[str] = None
	comment_id: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class PostsGetLListAllReactionsQuery(BaseModel):
        cursor: Optional[str] = None
	comment_id: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
class EmailsGetCListMailsQuery(BaseModel):
        cursor: Optional[str] = None
	include_headers: Optional[bool] = None
	after: Optional[str] = None
	account_id: str
	meta_only: Optional[bool] = None
	to: Optional[str] = None
	limit: Optional[int] = None
	from: Optional[str] = None
	before: Optional[str] = None
	any_email: Optional[str] = None
	folder: Optional[str] = None
class EmailsGetCGetMailQuery(BaseModel):
        include_headers: Optional[bool] = None
	account_id: Optional[str] = None
class EmailsDeleteCDeleteMailQuery(BaseModel):
        account_id: Optional[str] = None
class EmailsPutCUpdateMailQuery(BaseModel):
        account_id: Optional[str] = None
class EmailsGetCGetAttachmentQuery(BaseModel):
        account_id: Optional[str] = None
class EmailsGetIListFoldersQuery(BaseModel):
        account_id: Optional[str] = None
class EmailsGetIGetFolderQuery(BaseModel):
        account_id: Optional[str] = None
class UsersGetHListAllUserInvitationsSentQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class UsersGetHListAllUserInvitationsReceivedQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class UsersGetHGetAccountOwnerProfileQuery(BaseModel):
        account_id: str
class UsersGetHGetRelationsQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	filter: Optional[str] = None
	limit: Optional[int] = None
class UsersGetHGetFollowersQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class UsersGetHGetProfileByIdentifierQuery(BaseModel):
        linkedin_api: Optional[str] = None
	account_id: str
	notify: Optional[bool] = None
class UsersGetHListAllPostsQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
	is_company: Optional[bool] = None
class UsersGetHListAllCommentsQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class UsersGetHListAllReactionsQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class UsersDeleteHCancelInvitationQuery(BaseModel):
        account_id: str
class MessagingGetTListAllChatsQuery(BaseModel):
        cursor: Optional[str] = None
	after: Optional[str] = None
	account_type: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
	before: Optional[str] = None
	unread: Optional[bool] = None
class MessagingGetTGetChatQuery(BaseModel):
        account_id: Optional[str] = None
class MessagingGetTListChatMessagesQuery(BaseModel):
        cursor: Optional[str] = None
	after: Optional[str] = None
	limit: Optional[int] = None
	before: Optional[str] = None
	sender_id: Optional[str] = None
class MessagingGetOListAllMessagesQuery(BaseModel):
        cursor: Optional[str] = None
	after: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
	before: Optional[str] = None
	sender_id: Optional[str] = None
class MessagingGetLListAllAttendeesQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
class MessagingGetLListChatsByAttendeeQuery(BaseModel):
        cursor: Optional[str] = None
	after: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
	before: Optional[str] = None
class MessagingGetLListMessagesByAttendeeQuery(BaseModel):
        cursor: Optional[str] = None
	after: Optional[str] = None
	account_id: Optional[str] = None
	limit: Optional[int] = None
	before: Optional[str] = None
class AccountsGetListAccountsQuery(BaseModel):
        cursor: Optional[str] = None
	limit: Optional[int] = None
class AccountsGetResyncAccountQuery(BaseModel):
        after: Optional[float] = None
	before: Optional[float] = None
	linkedin_product: Optional[str] = None
class WebhooksGetOListWebhooksQuery(BaseModel):
        cursor: Optional[str] = None
	limit: Optional[int] = None
class LinkedinspecificGetCGetHiringProjectsQuery(BaseModel):
        cursor: Optional[str] = None
	account_id: str
	limit: Optional[int] = None
class LinkedinspecificGetCGetCompanyProfileQuery(BaseModel):
        account_id: str
class LinkedinspecificGetCGetInmailBalanceQuery(BaseModel):
        account_id: str
