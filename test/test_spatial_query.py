"""Tests for spatial query tools and resources."""

from __future__ import annotations

import inspect

import pytest
from fastmcp.exceptions import ToolError

from src.resources.query.result import get_query_result_resource
from src.shared.query_registry import clear_query_results
from src.tools.raster.query import raster_query
from src.tools.vector.query import vector_query


@pytest.mark.asyncio
async def test_raster_query_in_memory(tiny_raster_gtiff) -> None:
    clear_query_results()
    result = await raster_query.fn(
        uri=str(tiny_raster_gtiff),
        geometry=[0, 0, 5, 5],
        purpose="test subset",
    )

    meta = result["metadata"]
    assert meta["kind"] == "raster"
    assert meta["persisted"] is False
    assert result["output"] is None
    assert meta["counts"]["pixel_count"] > 0
    assert meta.get("id")


@pytest.mark.asyncio
async def test_raster_query_persisted(tmp_path, tiny_raster_gtiff) -> None:
    clear_query_results()
    output_path = tmp_path / "subset.tif"
    result = await raster_query.fn(
        uri=str(tiny_raster_gtiff),
        geometry=[0, 0, 5, 5],
        output=str(output_path),
        purpose="persist subset",
    )

    meta = result["metadata"]
    assert meta["persisted"] is True
    assert output_path.exists()
    assert result["output"] is not None


@pytest.mark.asyncio
async def test_vector_query_in_memory(tiny_vector_geojson) -> None:
    clear_query_results()
    result = await vector_query.fn(
        uri=str(tiny_vector_geojson),
        geometry=[-0.5, -0.5, 0.5, 0.5],
        purpose="vector subset",
    )

    meta = result["metadata"]
    assert meta["kind"] == "vector"
    assert meta["counts"]["feature_count"] == 1
    assert meta["persisted"] is False


@pytest.mark.asyncio
async def test_query_result_resource(tiny_raster_gtiff) -> None:
    clear_query_results()
    result = await raster_query.fn(
        uri=str(tiny_raster_gtiff),
        geometry=[0, 0, 5, 5],
        purpose="resource lookup",
    )
    query_id = result["metadata"]["id"]

    resource_or_awaitable = get_query_result_resource.fn(query_id=query_id, ctx=None)
    resource = (
        await resource_or_awaitable
        if inspect.isawaitable(resource_or_awaitable)
        else resource_or_awaitable
    )
    assert resource["id"] == query_id
    assert resource["kind"] == "raster"


@pytest.mark.asyncio
async def test_spatial_query_reflection_required(tmp_path, monkeypatch) -> None:
    from src.middleware.reflection_store import DiskStore
    from src.middleware.reflection_transform import reflection_preflight_check

    test_store = DiskStore(root=str(tmp_path / "reflections"))
    monkeypatch.setattr("src.middleware.reflection_transform.get_store", lambda: test_store)

    with pytest.raises(ToolError) as exc_info:
        await reflection_preflight_check(
            "raster_query",
            {"geometry": [0, 0, 1, 1], "purpose": "test"},
        )

    assert "justify_query_extent" in str(exc_info.value)
