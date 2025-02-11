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
