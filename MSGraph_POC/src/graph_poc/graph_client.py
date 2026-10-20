"""Graph client setup for Dev Proxy mocks and future authenticated Graph access."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

import httpx
from azure.identity import DeviceCodeCredential
from kiota_abstractions.authentication.anonymous_authentication_provider import (
    AnonymousAuthenticationProvider,
)
from msgraph import GraphServiceClient
from msgraph_core import BaseGraphRequestAdapter, GraphClientFactory


@dataclass
class GraphClientSession:
    """A Graph client plus resources that need closing after a run."""

    client: GraphServiceClient
    http_client: httpx.AsyncClient | None = None
    credential: DeviceCodeCredential | None = None

    async def aclose(self) -> None:
        if self.http_client is not None:
            await self.http_client.aclose()
        if self.credential is not None:
            self.credential.close()


def create_graph_client(
    mode: Literal["devproxy", "graph"],
    *,
    tenant_id: str | None = None,
    client_id: str | None = None,
    scopes: list[str] | None = None,
) -> GraphClientSession:
    """Create the configured Graph client, defaulting to the mock-friendly proxy."""
    if mode == "devproxy":
        return _create_devproxy_client()
    if mode == "graph":
        return _create_authenticated_graph_client(
            tenant_id=tenant_id,
            client_id=client_id,
            scopes=scopes or ["Files.Read"],
        )
    raise ValueError(f"Unknown client_mode {mode!r}; use 'devproxy' or 'graph'.")


def _create_devproxy_client() -> GraphClientSession:
    proxy_url = os.getenv("DEVPROXY_URL", "http://127.0.0.1:8000")
    http_client = httpx.AsyncClient(
        proxy=proxy_url,
        verify=False,
        timeout=20.0,
    )
    graph_http_client = GraphClientFactory.create_with_default_middleware(
        client=http_client
    )
    adapter = BaseGraphRequestAdapter(
        AnonymousAuthenticationProvider(),
        http_client=graph_http_client,
    )
    client = GraphServiceClient(request_adapter=adapter)
    return GraphClientSession(client=client, http_client=graph_http_client)


def _create_authenticated_graph_client(
    *,
    tenant_id: str | None,
    client_id: str | None,
    scopes: list[str],
) -> GraphClientSession:
    if not tenant_id or not client_id:
        raise ValueError(
            "Graph mode needs ENTRA_TENANT_ID and ENTRA_CLIENT_ID environment variables."
        )

    credential = DeviceCodeCredential(
        tenant_id=tenant_id,
        client_id=client_id,
    )
    client = GraphServiceClient(credentials=credential, scopes=scopes)
    return GraphClientSession(client=client, credential=credential)
