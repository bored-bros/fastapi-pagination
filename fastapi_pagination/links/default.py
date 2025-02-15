from __future__ import annotations

__all__ = ["Page"]

from collections.abc import MutableMapping
from math import ceil
from typing import Any, Generic, TypeVar

from fastapi_pagination.default import Page as BasePage

from .bases import Links, create_links, validation_decorator

T = TypeVar("T")


class Page(BasePage[T], Generic[T]):
    links: Links

    @validation_decorator
    def __root_validator__(cls, value: Any) -> Any:
        if isinstance(value, MutableMapping) and "links" not in value:
            page, size, total = [value[k] for k in ("page", "size", "total")]

            value["links"] = create_links(
                first={"page": 1},
                last={"page": ceil(total / size) if total > 0 and size > 0 else 1},
                next={"page": page + 1} if page * size < total else None,
                prev={"page": page - 1} if page - 1 >= 1 else None,
            )

        return value
