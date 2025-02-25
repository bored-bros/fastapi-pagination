from __future__ import annotations

__all__ = ["LimitOffsetPage"]

from collections.abc import MutableMapping
from math import floor
from typing import Any, Generic, TypeVar

from fastapi_pagination.limit_offset import LimitOffsetPage as BasePage

from .bases import Links, create_links, validation_decorator

T = TypeVar("T")


class LimitOffsetPage(BasePage[T], Generic[T]):
    links: Links

    @validation_decorator
    def __root_validator__(cls, value: Any) -> Any:
        if isinstance(value, MutableMapping) and "links" not in value:
            offset, limit, total = [value[k] for k in ("offset", "limit", "total")]

            # FIXME: it should not be so hard to calculate last page for limit-offset based pages
            start_offset = offset % limit
            last = start_offset + floor((total - start_offset) / limit) * limit

            if last == total:
                last = total - limit

            value["links"] = create_links(
                first={"offset": 0},
                last={"offset": last},
                next={"offset": offset + limit} if offset + limit < total else None,
                prev={"offset": offset - limit} if offset - limit >= 0 else None,
            )

        return value
