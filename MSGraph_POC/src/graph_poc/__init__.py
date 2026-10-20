"""Small Microsoft Graph SDK proof of concept."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from urllib.parse import quote

from kiota_abstractions.method import Method
from kiota_abstractions.request_information import RequestInformation
from msgraph import GraphServiceClient
from msgraph.generated.models.drive_item import DriveItem
from msgraph.generated.models.drive_item_collection_response import (
    DriveItemCollectionResponse,
)
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

from .graph_client import create_graph_client

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"


async def _get_folder_children(
    graph_client: GraphServiceClient, folder_path: str
) -> list[DriveItem]:
    """Fetch every page of children for a folder addressed by its OneDrive path."""
    encoded_folder_path = quote(folder_path.strip("/"), safe="/")
    url = (
        "https://graph.microsoft.com/v1.0/me/drive/root:/"
        f"{encoded_folder_path}:/children"
    )
    items: list[DriveItem] = []

    while url:
        result = await _send_children_request(graph_client, url)
        items.extend(result.value or [])
        url = result.odata_next_link or ""

    return items


async def _send_children_request(
    graph_client: GraphServiceClient, url: str
) -> DriveItemCollectionResponse:
    """Send one children request through the Graph SDK adapter."""
    request = RequestInformation()
    request.http_method = Method.GET
    request.url = url
    request.headers.try_add("Accept", "application/json")

    result = await graph_client.request_adapter.send_async(
        request,
        DriveItemCollectionResponse,
        {"XXX": ODataError},
    )
    if result is None:
        return DriveItemCollectionResponse()
    return result


async def _find_files_recursively(
    graph_client: GraphServiceClient,
    folder_path: str,
    relative_path: str = "",
) -> list[str]:
    """Return file paths beneath a folder, recursively traversing subfolders."""
    files: list[str] = []
    for item in await _get_folder_children(graph_client, folder_path):
        item_relative_path = f"{relative_path}/{item.name}".strip("/")
        if item.folder:
            child_folder_path = f"{folder_path.rstrip('/')}/{item.name}"
            files.extend(
                await _find_files_recursively(
                    graph_client, child_folder_path, item_relative_path
                )
            )
        else:
            files.append(item_relative_path)
    return files


async def list_files(folder_path: str, config: dict) -> None:
    """Recursively list files beneath a OneDrive folder."""
    graph_session = create_graph_client(
        config["client_mode"],
        tenant_id=os.getenv("ENTRA_TENANT_ID"),
        client_id=os.getenv("ENTRA_CLIENT_ID"),
        scopes=config.get("graph_scopes", ["Files.Read"]),
    )
    try:
        files = await _find_files_recursively(graph_session.client, folder_path)
        if not files:
            print("No files found.")
        else:
            for file_path in files:
                print(file_path)
    finally:
        await graph_session.aclose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Try a Microsoft Graph SDK folder listing.")
    parser.add_argument("--config", type=Path, default=CONFIG_PATH, help="Path to app config JSON")
    parser.add_argument(
        "--folder-path",
        help="Override the folder path relative to the root of your OneDrive",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    folder_path = args.folder_path or config["folder_path"]
    asyncio.run(list_files(folder_path, config))
