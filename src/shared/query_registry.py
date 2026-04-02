"""In-memory registry for spatial query results."""

from __future__ import annotations

import os
from collections import OrderedDict
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

_DEFAULT_TTL_SECONDS = 900
_DEFAULT_MAX_RESULTS = 25


class _Registry:
    def __init__(self) -> None:
        self._records: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def _now(self) -> datetime:
        return datetime.now(UTC)

    def _ttl_seconds(self) -> int:
        value = os.getenv("GDAL_MCP_QUERY_TTL_SECONDS")
        if not value:
            return _DEFAULT_TTL_SECONDS
        try:
            return max(60, int(value))
        except ValueError:
            return _DEFAULT_TTL_SECONDS

    def _max_results(self) -> int:
        value = os.getenv("GDAL_MCP_QUERY_MAX_RESULTS")
        if not value:
            return _DEFAULT_MAX_RESULTS
        try:
            return max(1, int(value))
        except ValueError:
            return _DEFAULT_MAX_RESULTS

    def _prune_expired(self) -> None:
        now = self._now()
        expired_ids = [rid for rid, rec in self._records.items() if rec["expires_at"] <= now]
        for rid in expired_ids:
            self._records.pop(rid, None)

    def register(self, meta: dict[str, Any], payload: Any | None = None) -> dict[str, Any]:
        self._prune_expired()
        created_at = self._now()
        expires_at = created_at + timedelta(seconds=self._ttl_seconds())
        record_id = str(uuid4())

        record = {
            "id": record_id,
            "created_at": created_at,
            "expires_at": expires_at,
            "meta": meta,
            "payload": payload,
        }
        self._records[record_id] = record

        max_results = self._max_results()
        while len(self._records) > max_results:
            self._records.popitem(last=False)

        return self._serialize(record)

    def get(self, record_id: str) -> dict[str, Any] | None:
        self._prune_expired()
        record = self._records.get(record_id)
        if record is None:
            return None
        return self._serialize(record)

    def _serialize(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": record["id"],
            "created_at": self._format_ts(record["created_at"]),
            "expires_at": self._format_ts(record["expires_at"]),
            **record["meta"],
        }

    @staticmethod
    def _format_ts(value: datetime) -> str:
        return value.isoformat().replace("+00:00", "Z")


_REGISTRY = _Registry()


def register_query_result(meta: dict[str, Any], payload: Any | None = None) -> dict[str, Any]:
    """Register a query result and return serialized metadata."""
    return _REGISTRY.register(meta, payload=payload)


def get_query_result(query_id: str) -> dict[str, Any] | None:
    """Fetch a query result's metadata by id, if still available."""
    return _REGISTRY.get(query_id)


def clear_query_results() -> None:
    """Clear registry (for tests)."""
    _REGISTRY._records.clear()
