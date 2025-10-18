from __future__ import annotations

from api_connection import post
from models import (
    AbortOptimizationRequest,
    CreateOptimizationRequest,
    DeleteOptimizationRequest,
    EstimateOptimizationRequest,
    EstimateOptimizationResponse,
    ListOptimizationRequest,
    ListOptimizationResponse,
    ReadOptimizationRequest,
    ReadOptimizationResponse,
    RestResponse,
    UpdateOptimizationRequest,
)
from mcp.server.fastmcp import FastMCP


def register_optimization_tools(mcp: FastMCP) -> None:
    """Expose optimization helper endpoints."""

    @mcp.tool(
        annotations={
            "title": "Estimate optimization time",
            "readOnlyHint": True,
        }
    )
    async def estimate_optimization_time(
        model: EstimateOptimizationRequest,
    ) -> EstimateOptimizationResponse:
        """Estimate resource requirements for an optimization."""

        return await post("/optimizations/estimate", model)

    @mcp.tool(annotations={"title": "Create optimization", "destructiveHint": False})
    async def create_optimization(
        model: CreateOptimizationRequest,
    ) -> ListOptimizationResponse:
        """Start a new optimization job."""

        return await post("/optimizations/create", model)

    @mcp.tool(annotations={"title": "Read optimization", "readOnlyHint": True})
    async def read_optimization(
        model: ReadOptimizationRequest,
    ) -> ReadOptimizationResponse:
        """Retrieve the status of an optimization job."""

        return await post("/optimizations/read", model)

    @mcp.tool(annotations={"title": "List optimizations", "readOnlyHint": True})
    async def list_optimizations(
        model: ListOptimizationRequest,
    ) -> ListOptimizationResponse:
        """List optimizations for a project."""

        return await post("/optimizations/list", model)

    @mcp.tool(annotations={"title": "Update optimization", "idempotentHint": True})
    async def update_optimization(model: UpdateOptimizationRequest) -> RestResponse:
        """Update the name of an optimization job."""

        return await post("/optimizations/update", model)

    @mcp.tool(annotations={"title": "Abort optimization", "idempotentHint": True})
    async def abort_optimization(model: AbortOptimizationRequest) -> RestResponse:
        """Abort an optimization that is currently running."""

        return await post("/optimizations/abort", model)

    @mcp.tool(annotations={"title": "Delete optimization", "idempotentHint": True})
    async def delete_optimization(model: DeleteOptimizationRequest) -> RestResponse:
        """Delete an optimization job."""

        return await post("/optimizations/delete", model)
