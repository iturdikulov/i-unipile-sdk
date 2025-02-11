"""Synchronous and asynchronous clients for unipile's API."""
import json
import logging
from abc import abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self
import httpx
from httpx import Request, Response
from .api_endpoints import (
    # AttendeesEndpoint,
    # CommonEndpoint,
    # LinkedinSpecificEndpoint,
    # MailsEndpoint,
    # MessagingEndpoint,
    # PostsEndpoint,
    # UsersEndpoint,
    # CommentsEndpoint,
    # DatabasesEndpoint,
    # PagesEndpoint,
    AccountsEndpoint,
    HostedEndpoint,
    UsersEndpoint,
    SearchEndpoint,
)
from .errors import (
    APIResponseError,
    HTTPResponseError,
    RequestTimeoutError,
    is_api_error_code,
)
from .logging import make_console_logger
from .typing import SyncAsync

@dataclass
class ClientOptions:
    """Options to configure the client.
    Attributes:
        auth: Bearer token for authentication. If left undefined, the `auth` parameter
            should be set on each request.
        timeout_ms: Number of milliseconds to wait before emitting a
            `RequestTimeoutError`.
        base_url: The root URL for sending API requests. This can be changed to test with
            a mock server.
        log_level: Verbosity of logs the instance will produce. By default, logs are
            written to `stdout`.
        logger: A custom logger.
        unipile_version: unipile version to use.
    """
    auth: str | None = None
    base_url: str = "https://api2.unipile.com:13260"
    timeout_ms: int = 60_000
    log_level: int = logging.WARNING
    logger: logging.Logger | None = None
    unipile_version: str = "v1"

class BaseClient:
    def __init__(
        self,
        client: httpx.Client | httpx.AsyncClient,
        options: dict[str, Any] | ClientOptions | None = None,
        **kwargs: Any,
    ) -> None:
        if options is None:
            options = ClientOptions(**kwargs)
        elif isinstance(options, dict):
            options = ClientOptions(**options)
        self.logger = options.logger or make_console_logger()
        self.logger.setLevel(options.log_level)
        self.options = options
        self._clients: list[httpx.Client | httpx.AsyncClient] = []
        self.client = client
        self.accounts = AccountsEndpoint(self)
        self.users = UsersEndpoint(self)
        self.hosted = HostedEndpoint(self)
        self.ln_search = SearchEndpoint(self)
        # self.databases = DatabasesEndpoint(self)
        # self.users = UsersEndpoint(self)
        # self.pages = PagesEndpoint(self)
        # self.search = SearchEndpoint(self)
        # self.comments = CommentsEndpoint(self)

    @property
    def client(self) -> httpx.Client | httpx.AsyncClient:
        return self._clients[-1]

    @client.setter
    def client(self, client: httpx.Client | httpx.AsyncClient) -> None:
        client.base_url = httpx.URL(f"{self.options.base_url}/api/{self.options.unipile_version}/")
        client.timeout = httpx.Timeout(timeout=self.options.timeout_ms / 1_000)
        client.headers = httpx.Headers(
            {
                "User-Agent": "salesloop/comm_client",
            }
        )
        if self.options.auth:
            client.headers["X-API-KEY"] = f"{self.options.auth}"
        self._clients.append(client)

    def _build_request(
        self,
        method: str,
        path: str,
        query: dict[Any, Any] | None = None,
        body: dict[Any, Any] | None = None,
    ) -> Request:
        headers = httpx.Headers()
        self.logger.info(f"{method} {self.client.base_url}{path}")
        self.logger.debug(f"=> {query} -- {body}")
        return self.client.build_request(
            method, path, params=query, json=body, headers=headers
        )

    def _parse_response(self, response: Response) -> dict:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            try:
                body = error.response.json()
                code = body.get("code")
            except json.JSONDecodeError:
                code = None
            if code and is_api_error_code(code):
                raise APIResponseError(response, body["message"], code)
            raise HTTPResponseError(error.response)
        body = response.json()
        self.logger.debug(f"=> {body}")
        return body

    @classmethod
    @abstractmethod
    def request(
        cls,
        path: str,
        method: str,
        query: dict[Any, Any] | None = None,
        body: dict[Any, Any] | None = None,
    ) -> dict:
        # noqa
        pass

class Client(BaseClient):
    """Synchronous client for unipile's API."""
    client: httpx.Client

    def __init__(
        self,
        options: dict[Any, Any] | ClientOptions | None = None,
        client: httpx.Client | None = None,
        **kwargs: Any,
    ) -> None:
        if client is None:
            client = httpx.Client()
        super().__init__(client, options, **kwargs)

    def __enter__(self) -> Self:
        self.client = httpx.Client()
        self.client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        self.client.__exit__(exc_type, exc_value, traceback)
        del self._clients[-1]

    def close(self) -> None:
        """Close the connection pool of the current inner client."""
        self.client.close()

    def request(
        self,
        path: str,
        method: str,
        query: dict[Any, Any] | None = None,
        body: dict[Any, Any] | None = None,
    ) -> dict:
        """Send an HTTP request."""
        request = self._build_request(method, path, query, body)
        try:
            response = self.client.send(request)
        except httpx.TimeoutException:
            raise RequestTimeoutError()
        return self._parse_response(response)

class AsyncClient(BaseClient):
    """Asynchronous client for unipile's API."""
    client: httpx.AsyncClient

    def __init__(
        self,
        options: dict[str, Any] | ClientOptions | None = None,
        client: httpx.AsyncClient | None = None,
        **kwargs: Any,
    ) -> None:
        if client is None:
            client = httpx.AsyncClient()
        super().__init__(client, options, **kwargs)

    async def __aenter__(self) -> Self:
        self.client = httpx.AsyncClient()
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType | None,
    ) -> None:
        await self.client.__aexit__(exc_type, exc_value, traceback)
        del self._clients[-1]

    async def aclose(self) -> None:
        """Close the connection pool of the current inner client."""
        await self.client.aclose()

    async def request(
        self,
        path: str,
        method: str,
        query: dict[Any, Any] | None = None,
        body: dict[Any, Any] | None = None,
        auth: str | None = None,
    ) -> Any:
        """Send an HTTP request asynchronously."""
        request = self._build_request(method, path, query, body, auth)
        try:
            response = await self.client.send(request)
        except httpx.TimeoutException:
            raise RequestTimeoutError()
        return self._parse_response(response)
