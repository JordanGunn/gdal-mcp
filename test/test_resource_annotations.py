"""Regression tests for resource annotations."""

from __future__ import annotations

from collections.abc import Iterable

def _assert_annotations_evaluated(funcs: Iterable[object]) -> None:
    for func in funcs:
        underlying = getattr(func, "fn", func)
        annotations = getattr(underlying, "__annotations__", {})
        for value in annotations.values():
            module = getattr(underlying, "__module__", type(underlying).__module__)
            name = getattr(underlying, "__name__", type(underlying).__name__)
            assert not isinstance(value, str), (
                f"Expected evaluated annotations for {module}.{name}; "
                "found string annotations."
            )


def test_resource_annotations_are_eager() -> None:
    from src.resources.catalog import (
        get_workspace_summary,
        list_all,
        list_by_crs,
        list_raster,
        list_vector,
    )
    from src.resources.metadata.band import get_raster_band_metadata
    from src.resources.metadata.format_detection import get_format_metadata
    from src.resources.metadata.raster import get_raster_metadata
    from src.resources.metadata.statistics import get_raster_statistics
    from src.resources.metadata.vector import get_vector_metadata
    from src.resources.reference import (
        list_common_crs,
        list_compression_methods_resource,
        list_geospatial_terms,
        list_resampling_methods_resource,
        resampling_guide_resource,
    )

    _assert_annotations_evaluated(
        [
            list_all,
            list_by_crs,
            list_raster,
            list_vector,
            get_workspace_summary,
            get_format_metadata,
            get_raster_metadata,
            get_raster_statistics,
            get_raster_band_metadata,
            get_vector_metadata,
            list_common_crs,
            list_compression_methods_resource,
            list_resampling_methods_resource,
            resampling_guide_resource,
            list_geospatial_terms,
        ]
    )


def test_tool_annotations_are_eager() -> None:
    from src.tools.raster.convert import convert as raster_convert
    from src.tools.raster.info import info as raster_info
    from src.tools.raster.reproject import reproject as raster_reproject
    from src.tools.raster.stats import stats as raster_stats
    from src.tools.vector.buffer import buffer as vector_buffer
    from src.tools.vector.clip import clip as vector_clip
    from src.tools.vector.convert import convert as vector_convert
    from src.tools.vector.info import info as vector_info
    from src.tools.vector.reproject import reproject as vector_reproject
    from src.tools.vector.simplify import simplify as vector_simplify

    _assert_annotations_evaluated(
        [
            raster_convert,
            raster_info,
            raster_reproject,
            raster_stats,
            vector_buffer,
            vector_clip,
            vector_convert,
            vector_info,
            vector_reproject,
            vector_simplify,
        ]
    )
