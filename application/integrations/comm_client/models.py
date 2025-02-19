from __future__ import annotations

from enum import Enum
from typing import Any, Literal, Union

from pydantic import BaseModel, Field


# Hosted models
class ConnectAccountResponse(BaseModel):
    status: Literal["CREATION_SUCCESS", "RECONNECTED"]
    account_id: str
    name: str


# ---


class SearchQuery(BaseModel):
    cursor: str | None
    account_id: str
    limit: int | None


class SearchClassicPeople(BaseModel):
    keywords: str
    account_id: str
    limit: int | None


# Common Enums
class ApiType(str, Enum):
    CLASSIC = "classic"
    SALES_NAVIGATOR = "sales_navigator"
    RECRUITER = "recruiter"


class CategoryType(str, Enum):
    PEOPLE = "people"
    COMPANIES = "companies"
    POSTS = "posts"
    JOBS = "jobs"


class NetworkDistance(str, Enum):
    SELF = "SELF"
    DISTANCE_1 = "DISTANCE_1"
    DISTANCE_2 = "DISTANCE_2"
    DISTANCE_3 = "DISTANCE_3"
    OUT_OF_NETWORK = "OUT_OF_NETWORK"


# Base Models
class CursorParam(BaseModel):
    cursor: str = Field(min_length=1)


class DateRange(BaseModel):
    year: int | None = None
    month: int | None = None


class TenureInfo(BaseModel):
    years: int
    months: int


class Position(BaseModel):
    company: str
    company_id: str | None = None
    description: str | None = None
    role: str
    location: str | None = None
    tenure_at_role: TenureInfo | None = None
    tenure_at_company: TenureInfo | None = None
    start: DateRange | None = None
    end: DateRange | None = None


class Education(BaseModel):
    degree: str | None = None
    school: str
    school_id: str | None = None
    start: DateRange
    end: DateRange | None = None


class WorkExperience(BaseModel):
    company: str
    company_id: str | None = None
    role: str
    industry: str | None = None
    start: DateRange
    end: DateRange | None = None


class Author(BaseModel):
    public_identifier: str
    name: str
    is_company: bool


class LastOutreachActivity(BaseModel):
    type: Literal["SEND_MESSAGE", "ACCEPT_INVITATION"]
    performed_at: str


# Search Result Models
class PeopleSearchResult(BaseModel):
    object: Literal["SearchResult"]
    type: Literal["PEOPLE"]
    id: str
    public_identifier: str | None = None
    public_profile_url: str | None = None
    profile_url: str | None = None
    profile_picture_url: str | None = None
    profile_picture_url_large: str | None = None
    member_urn: str | None = None
    name: str | None = None
    first_name: str
    last_name: str
    network_distance: NetworkDistance
    location: str | None = None
    industry: str | None = None
    keywords_match: str
    headline: str
    connections_count: int
    pending_invitation: bool
    can_send_inmail: bool
    recruiter_candidate_id: str
    premium: bool
    open_profile: bool
    shared_connections_count: int
    recent_posts_count: int
    recently_hired: bool
    mentioned_in_the_news: bool
    last_outreach_activity: LastOutreachActivity | None = None
    current_positions: list[Position]
    education: list[Education]
    work_experience: list[WorkExperience]


class CompanySearchResult(BaseModel):
    object: Literal["SearchResult"]
    type: Literal["COMPANY"]
    id: str
    name: str
    location: str | None = None
    profile_url: str
    industry: str
    summary: str | None = None
    followers_count: int
    job_offers_count: int
    headcount: str


# Search Parameters
class LocationParam(BaseModel):
    id: str = Field(min_length=1)
    priority: Literal["CAN_HAVE", "MUST_HAVE", "DOESNT_HAVE"] | None = None
    scope: Literal["CURRENT", "OPEN_TO_RELOCATE_ONLY", "CURRENT_OR_OPEN_TO_RELOCATE"] | None = None


class CompanyParam(BaseModel):
    include: list[str] | None = None
    exclude: list[str] | None = None


# Request Models
class ClassicPeopleSearch(BaseModel):
    api: Literal["classic"]
    category: Literal["people"]
    keywords: str | None = None
    industry: list[str] | None = None
    location: list[str] | None = None
    profile_language: list[str] | None = Field(None, min_length=2, max_length=2)
    network_distance: list[int] | None = Field(None, ge=1, le=3)
    company: list[str] | None = None
    past_company: list[str] | None = None
    school: list[str] | None = None
    service: list[str] | None = None
    connections_of: list[str] | None = None
    followers_of: list[str] | None = None
    open_to: list[Literal["proBono", "boardMember"]] | None = None
    advanced_keywords: dict[str, str] | None = None


class SearchResponse(BaseModel):
    object: Literal["LinkedinSearch"]
    items: list[Union[PeopleSearchResult, CompanySearchResult]]
    config: dict[str, Any]  # This could be more specific based on your needs
    paging: dict[str, Any]  # This could be more specific based on your needs
    cursor: str | None = None


# Error Response Models
class ErrorResponse(BaseModel):
    title: str
    detail: str | None = None
    instance: str | None = None
    status: int


class BadRequestResponse(ErrorResponse):
    type: Literal[
        "errors/invalid_parameters",
        "errors/malformed_request",
        "errors/content_too_large",
        "errors/invalid_url",
        "errors/too_many_characters",
        "errors/unescaped_characters",
        "errors/missing_parameters",
    ]
    status: Literal[400]


class LinkedinUserPlanDisconnected(BaseModel):
    error: Literal["DISCONNECTED"]


class LinkedinUserOrganization(BaseModel):
    id: str
    mailbox_id: str
    name: str


class LinkedinUserPlanInfo(BaseModel):
    owner_seat_id: str
    contract_id: str


class LinkedinUserMe(BaseModel):
    provider: Literal["LINKEDIN"]
    provider_id: str
    entity_urn: str
    object_urn: str
    first_name: str
    last_name: str
    profile_picture_url: str | None = None
    public_profile_url: str | None = None
    public_identifier: str | None = None
    headline: str | None = None
    location: str | None = None
    email: str
    premium: bool
    open_profile: bool
    occupation: str | None = None
    organizations: list[LinkedinUserOrganization | None]
    recruiter: LinkedinUserPlanInfo | LinkedinUserPlanDisconnected | None = None
    sales_navigator: LinkedinUserPlanInfo | LinkedinUserPlanDisconnected | None = None
    object: Literal["AccountOwnerProfile"]

# --- User profile
class Social(BaseModel):
    type: str
    name: str

class ContactInfo(BaseModel):
    emails: list[str] | None = None
    phones: list[str] | None = None
    adresses: list[str] | None = None
    socials: list[Social] | None = None

class Birthdate(BaseModel):
    month: float
    day: float

class PrimaryLocale(BaseModel):
    country: str
    language: str


class WorkExperienceItem(BaseModel):
    position: str
    company_id: str | None = None
    company: str
    location: str | None = None
    description: str | None = None
    skills: list[str]
    current: bool | None = None
    status: str | None = None
    start: str | Any
    end: str | Any


class VolunteeringExperienceItem(BaseModel):
    company: str
    description: str
    role: str
    cause: str
    start: str | Any
    end: str | Any


class EducationItem(BaseModel):
    degree: str | None = None
    school: str
    field_of_study: str | None = None
    start: str | Any
    end: str | Any


class Skill(BaseModel):
    name: str
    endorsement_count: float
    endorsement_id: float | Any
    insights: list[str]
    endorsed: bool


class Language(BaseModel):
    name: str
    proficiency: str | None = None


class Certification(BaseModel):
    name: str
    organization: str
    url: str | None = None


class Project(BaseModel):
    name: str
    description: str
    skills: list[str]
    start: str | Any
    end: str | Any


class Invitation(BaseModel):
    type: Literal["SENT"] | Literal["RECEIVED"]
    status: Literal["PENDING"] | Literal["IGNORED"] | Literal["WITHDRAWN"]


class LinkedinUserProfile(BaseModel):
    provider: Literal["LINKEDIN"]
    provider_id: str
    public_identifier: str | Any
    first_name: str | Any
    last_name: str | Any
    headline: str
    summary: str | None = None
    contact_info: ContactInfo | None = None
    birthdate: Birthdate | None = None
    primary_locale: PrimaryLocale | None = None
    location: str | None = None
    websites: list[str]
    profile_picture_url: str | None = None
    profile_picture_url_large: str | None = None
    background_picture_url: str | None = None
    hashtags: list[str] | None = None
    can_send_inmail: bool | None = None
    is_open_profile: bool | None = None
    is_premium: bool | None = None
    is_influencer: bool | None = None
    is_creator: bool | None = None
    is_hiring: bool | None = None
    is_open_to_work: bool | None = None
    is_saved_lead: bool | None = None
    is_crm_imported: bool | None = None
    is_relationship: bool | None = None
    is_self: bool | None = None
    invitation: Invitation | None = None
    work_experience: list[WorkExperienceItem] | None = None
    volunteering_experience: list[VolunteeringExperienceItem] | None = None
    education: list[EducationItem] | None = None
    skills: list[Skill] | None = None
    languages: list[Language] | None = None
    certifications: list[Certification] | None = None
    projects: list[Project] | None = None
    follower_count: float | None = None
    connections_count: float | None = None
    shared_connections_count: float | None = None
    network_distance: Literal["FIRST_DEGREE", "SECOND_DEGREE", "THIRD_DEGREE", "OUT_OF_NETWORK"] | None = None
    public_profile_url: str | None = None
    object: Literal["UserProfile"]
#/ --- User profile

class LinkedinUsersInvitePayload(BaseModel):
    provider_id: str = Field(
        ..., description="The id of the user to add. It has to be the provider’s id."
    )
    account_id: str = Field(
        ..., description="The id of the account where the user will be added."
    )
    user_email: str|None = Field(
        default=None,
        description="The email address of the user when it's required (Linkedin specific).",
    )
    message: str|None = Field(
        default=None,
        description="An optional message to go with the invitation (max 300 chars).",
        max_length=300,
    )

class LinkedinUsersInviteResponse(BaseModel):
    object: Literal["UserInvitationSent"]
    invitation_id: str
    usage: float | None = Field(
        default=None,
        description="A percentage of query usage based on the limit set by the"
                    "provider. Triggers only on passing a new landing "
                    "(50, 75, 90, 95)."
    )

# Search
class NetworkDistanceEnum(float, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3


class OpenToEnum(str, Enum):
    PRO_BONO = "proBono"
    BOARD_MEMBER = "boardMember"


class AdvancedKeywords(BaseModel):
    first_name: str | None = Field(
        default=None, description="Linkedin native filter : KEYWORDS / FIRST NAME."
    )
    last_name: str | None = Field(
        default=None, description="Linkedin native filter : KEYWORDS / LAST NAME."
    )
    title: str | None = Field(
        default=None, description="Linkedin native filter : KEYWORDS / TITLE."
    )
    company: str | None = Field(
        default=None, description="Linkedin native filter : KEYWORDS / LAST NAME."
    )
    school: str | None = Field(
        default=None, description="Linkedin native filter : KEYWORDS / LAST NAME."
    )


# WARN: patterns doesn't work!
class LinkedinSearchPayload(BaseModel):
    api: Literal["classic"] = "classic"
    category: Literal["people"] = "people"
    keywords: str | None = Field(default=None, description="Linkedin native filter : KEYWORDS.")
    industry: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type INDUSTRY on the List search parameters route to find out the right ID.\nLinkedin native filter : INDUSTRY.",
        min_length=1,
        # pattern=r"^[0-9]+$",
    )
    location: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type LOCATION on the List search parameters route to find out the right ID.\nLinkedin native filter : LOCATIONS.",
        min_length=1,
        # pattern=r"^[0-9]+$",
    )
    profile_language: list[str] | None = Field(
        default=None,
        description="ISO 639-1 language code.\nLinkedin native filter : PROFILE LANGUAGE.",
        max_length=2,
        min_length=2,
    )
    network_distance: list[NetworkDistanceEnum] | None = Field(
        default=None,
        description="First, second or third+ degree.\nLinkedin native filter : CONNECTIONS.",
    )
    company: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type COMPANY on the List search parameters route to find out the right ID.\nLinkedin native filter : CURRENT COMPANY.",
        min_length=1,
        # pattern="^\\d+$",
    )
    past_company: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type COMPANY on the List search parameters route to find out the right ID.\nLinkedin native filter : PAST COMPANY.",
        min_length=1,
        # pattern="^\\d+$",
    )
    school: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type SCHOOL on the List search parameters route to find out the right ID.\nLinkedin native filter : SCHOOL.",
        min_length=1,
        # pattern="^\\d+$",
    )
    service: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type SERVICE on the List search parameters route to find out the right ID.\nLinkedin native filter : SERVICE CATEGORIES.",
        min_length=1,
        # pattern="^\\d+$",
    )
    connections_of: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type PEOPLE on the List search parameters route to find out the right ID.\nLinkedin native filter : CONNECTIONS OF.",
        min_length=1,
        # pattern="^.+$",
    )
    followers_of: list[str] | None = Field(
        default=None,
        description="The ID of the parameter. Use type PEOPLE on the List search parameters route to find out the right ID.\nLinkedin native filter : FOLLOWERS OF.",
        min_length=1,
        # pattern="^.+$",
    )
    open_to: list[OpenToEnum] | None = Field(
        default=None, description="Linkedin native filter : OPEN TO."
    )
    advanced_keywords: AdvancedKeywords | None = None


class CommonSearchParameter(str, Enum):
    LOCATION = "LOCATION"
    PEOPLE = "PEOPLE"
    COMPANY = "COMPANY"
    SCHOOL = "SCHOOL"
    INDUSTRY = "INDUSTRY"
    SERVICE = "SERVICE"
    JOB_FUNCTION = "JOB_FUNCTION"
    JOB_TITLE = "JOB_TITLE"
    EMPLOYMENT_TYPE = "EMPLOYMENT_TYPE"
    SKILL = "SKILL"


class SalesNavSearchParameter(str, Enum):
    GROUPS = "GROUPS"
    DEPARTMENT = "DEPARTMENT"
    PERSONA = "PERSONA"
    ACCOUNT_LISTS = "ACCOUNT_LISTS"
    LEAD_LISTS = "LEAD_LISTS"
    TECHNOLOGIES = "TECHNOLOGIES"
    SAVED_ACCOUNTS = "SAVED_ACCOUNTS"
    SAVED_SEARCHES = "SAVED_SEARCHES"
    RECENT_SEARCHES = "RECENT_SEARCHES"


class RecruiterSearchParameter(str, Enum):
    GROUPS = "GROUPS"
    DEPARTMENT = "DEPARTMENT"
    HIRING_PROJECTS = "HIRING_PROJECTS"
    SAVED_SEARCHES = "SAVED_SEARCHES"
    SAVED_FILTERS = "SAVED_FILTERS"


class LinkedinSearchParameter(BaseModel):
    object: Literal["LinkedinSearchParameter"]
    id: str = Field(description="A unique identifier.", min_length=1, title="UniqueId")
    title: str
    additional_data: dict[str, Any] | None = None


class Paging(BaseModel):
    page_count: float


class LinkedinSearchParametersResponse(BaseModel):
    object: Literal["LinkedinSearchParametersList"]
    items: list[LinkedinSearchParameter]
    paging: Paging


class SearchResultsPaging(BaseModel):
    start: int = Field(ge=0)
    page_count: int = Field(ge=0)
    total_count: int = Field(ge=0)

# --- ERRORS
class BadRequestType(str, Enum):
    ERRORS_INVALID_PARAMETERS = "errors/invalid_parameters"
    ERRORS_MALFORMED_REQUEST = "errors/malformed_request"
    ERRORS_CONTENT_TOO_LARGE = "errors/content_too_large"
    ERRORS_INVALID_URL = "errors/invalid_url"
    ERRORS_TOO_MANY_CHARACTERS = "errors/too_many_characters"
    ERRORS_UNESCAPED_CHARACTERS = "errors/unescaped_characters"
    ERRORS_MISSING_PARAMETERS = "errors/missing_parameters"

class UnauthorizedType(str, Enum):
    ERRORS_MISSING_CREDENTIALS = "errors/missing_credentials"
    ERRORS_MULTIPLE_SESSIONS = "errors/multiple_sessions"
    ERRORS_INVALID_CHECKPOINT_SOLUTION = "errors/invalid_checkpoint_solution"
    ERRORS_CHECKPOINT_ERROR = "errors/checkpoint_error"
    ERRORS_INVALID_CREDENTIALS = "errors/invalid_credentials"
    ERRORS_EXPIRED_CREDENTIALS = "errors/expired_credentials"
    ERRORS_INSUFFICIENT_PRIVILEGES = "errors/insufficient_privileges"
    ERRORS_DISCONNECTED_ACCOUNT = "errors/disconnected_account"
    ERRORS_DISCONNECTED_FEATURE = "errors/disconnected_feature"
    ERRORS_INVALID_CREDENTIALS_BUT_VALID_ACCOUNT_IMAP = (
        "errors/invalid_credentials_but_valid_account_imap"
    )
    ERRORS_EXPIRED_LINK = "errors/expired_link"
    ERRORS_WRONG_ACCOUNT = "errors/wrong_account"

class ForbiddenType(str, Enum):
    ERRORS_ACCOUNT_RESTRICTED = "errors/account_restricted"
    ERRORS_INSUFFICIENT_PERMISSIONS = "errors/insufficient_permissions"
    ERRORS_SESSION_MISMATCH = "errors/session_mismatch"
    ERRORS_FEATURE_NOT_SUBSCRIBED = "errors/feature_not_subscribed"
    ERRORS_UNKNOWN_AUTHENTICATION_CONTEXT = "errors/unknown_authentication_context"
    ERRORS_RESOURCE_ACCESS_RESTRICTED = "errors/resource_access_restricted"

class NotFoundType(str, Enum):
    ERRORS_RESOURCE_NOT_FOUND = "errors/resource_not_found"
    ERRORS_INVALID_RESOURCE_IDENTIFIER = "errors/invalid_resource_identifier"

class UnprocessableEntityType(str, Enum):
    ERRORS_INVALID_ACCOUNT = "errors/invalid_account"
    ERRORS_INVALID_RECIPIENT = "errors/invalid_recipient"
    ERRORS_NO_CONNECTION_WITH_RECIPIENT = "errors/no_connection_with_recipient"
    ERRORS_BLOCKED_RECIPIENT = "errors/blocked_recipient"
    ERRORS_UNPROCESSABLE_ENTITY = "errors/unprocessable_entity"
    ERRORS_INVALID_MESSAGE = "errors/invalid_message"
    ERRORS_INVALID_POST = "errors/invalid_post"
    ERRORS_NOT_ALLOWED_INMAIL = "errors/not_allowed_inmail"
    ERRORS_INSUFFICIENT_CREDITS = "errors/insufficient_credits"
    ERRORS_CANNOT_RESEND_YET = "errors/cannot_resend_yet"
    ERRORS_LIMIT_EXCEEDED = "errors/limit_exceeded"
    ERRORS_ALREADY_INVITED_RECENTLY = "errors/already_invited_recently"
    ERRORS_CANNOT_INVITE_ATTENDEE = "errors/cannot_invite_attendee"
    ERRORS_PARENT_MAIL_NOT_FOUND = "errors/parent_mail_not_found"
    ERRORS_INVALID_REPLY_SUBJECT = "errors/invalid_reply_subject"
    ERRORS_INVALID_HEADERS = "errors/invalid_headers"
    ERRORS_SEND_AS_DENIED = "errors/send_as_denied"
    ERRORS_INVALID_FOLDER = "errors/invalid_folder"
    ERRORS_LIMIT_TOO_HIGH = "errors/limit_too_high"
    ERRORS_UNAUTHORIZED = "errors/unauthorized"
    ERRORS_SENDER_REJECTED = "errors/sender_rejected"
    ERRORS_RECIPIENT_REJECTED = "errors/recipient_rejected"
    ERRORS_IP_REJECTED_BY_SERVER = "errors/ip_rejected_by_server"
    ERRORS_PROVIDER_UNREACHABLE = "errors/provider_unreachable"
    ERRORS_ACCOUNT_CONFIGURATION_ERROR = "errors/account_configuration_error"

class TooManyRequestsErrorType(str, Enum):
    ERRORS_TOO_MANY_REQUESTS = "errors/too_many_requests"

class InternalServerErrorType(str, Enum):
    ERRORS_UNEXPECTED_ERROR = "errors/unexpected_error"
    ERRORS_PROVIDER_ERROR = "errors/provider_error"
    ERRORS_AUTHENTICATION_INTENT_ERROR = "errors/authentication_intent_error"

class NotImplementedErrorType(str, Enum):
    ERRORS_FEATURE_NOT_IMPLEMENTED = "errors/feature_not_implemented"

class ServiceUnavailableErrorType(str, Enum):
    ERRORS_NO_CLIENT_SESSION = "errors/no_client_session"
    ERRORS_NO_CHANNEL = "errors/no_channel"
    ERRORS_NO_HANDLER = "errors/no_handler"
    ERRORS_NETWORK_DOWN = "errors/network_down"
    ERRORS_SERVICE_UNAVAILABLE = "errors/service_unavailable"

class RequestTimeoutErrorType(str, Enum):
    ERRORS_REQUEST_TIMEOUT = "errors/request_timeout"

APIErrorTypes = {
    400: BadRequestType,
    401: UnauthorizedType,
    403: ForbiddenType,
    404: NotFoundType,
    422: UnprocessableEntityType,
    429: TooManyRequestsErrorType,
    500: InternalServerErrorType,
    501: NotImplementedErrorType,
    503: ServiceUnavailableErrorType,
    408: RequestTimeoutErrorType,
}
