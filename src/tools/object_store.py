from __future__ import annotations

from api_connection import authenticated_client, post
from models import (
    DeleteObjectStoreRequest,
    GetObjectStoreJobIdRequest,
    GetObjectStorePropertiesRequest,
    GetObjectStorePropertiesResponse,
    GetObjectStoreResponse,
    GetObjectStoreURLRequest,
    ListObjectStoreRequest,
    ListObjectStoreResponse,
    ObjectStoreBinaryFile,
    RestResponse,
)
from mcp.server.fastmcp import FastMCP


def register_object_store_tools(mcp: FastMCP) -> None:
    """Expose QuantConnect Object Store utilities."""

    @mcp.tool(annotations={"title": "Upload Object Store file", "idempotentHint": True})
    async def upload_object(model: ObjectStoreBinaryFile) -> RestResponse:
        """Upload a file to the Object Store."""

        async with authenticated_client() as (client, headers, settings):
            try:
                response = await client.post(
                    "/object/set",
                    headers=headers,
                    data={
                        "organizationId": model.organizationId,
                        "key": model.key,
                    },
                    files={"objectData": model.objectData},
                    timeout=settings.api_timeout,
                )
                response.raise_for_status()
                return response.json()
            except Exception as exc:  # pragma: no cover - httpx raises HTTPError subclasses
                raise RuntimeError("Failed to upload Object Store file") from exc

    @mcp.tool(
        annotations={
            "title": "Read Object Store file properties",
            "readOnlyHint": True,
        }
    )
    async def read_object_properties(
        model: GetObjectStorePropertiesRequest,
    ) -> GetObjectStorePropertiesResponse:
        """Read metadata for a specific Object Store key."""

        return await post("/object/properties", model)

    @mcp.tool(
        annotations={
            "title": "Read Object Store file job Id",
            "destructiveHint": False,
        }
    )
    async def read_object_store_file_job_id(
        model: GetObjectStoreJobIdRequest,
    ) -> GetObjectStoreResponse:
        """Create a download job and return its identifier."""

        return await post("/object/get", model)

    @mcp.tool(
        annotations={
            "title": "Read Object Store file download URL",
            "readOnlyHint": True,
        }
    )
    async def read_object_store_file_download_url(
        model: GetObjectStoreURLRequest,
    ) -> GetObjectStoreResponse:
        """Return a pre-signed download URL for an Object Store key."""

        return await post("/object/get", model)

    @mcp.tool(
        annotations={"title": "List Object Store files", "readOnlyHint": True}
    )
    async def list_object_store_files(
        model: ListObjectStoreRequest,
    ) -> ListObjectStoreResponse:
        """List Object Store files within a directory."""

        return await post("/object/list", model)

    @mcp.tool(
        annotations={
            "title": "Delete Object Store file",
            "idempotentHint": True,
        }
    )
    async def delete_object(model: DeleteObjectStoreRequest) -> RestResponse:
        """Delete an Object Store key."""

        return await post("/object/delete", model)
