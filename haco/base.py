from __future__ import annotations

from typing import Any, ClassVar

from pydantic import ConfigDict

from corio import dm


class Base(dm.Base):
    """

    Base class for haco objects. Provides model dumping functionality.

    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')
    DATA: ClassVar[dict[str, Any]] = {}

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        """
        Dump this model for Home Assistant discovery payloads.

        Behavior differences from vanilla Pydantic:
        - Defaults to `exclude_none=True`.
        - Merges class-level `DATA` into the dumped mapping.
        - Excludes runtime extra attributes (used for dynamic callbacks) so they
          do not leak into announce payloads.
        """
        kwargs.setdefault("exclude_none", True)
        exclude = kwargs.pop("exclude", None)
        extra = getattr(self, "__pydantic_extra__", None) or {}
        extra_keys = set(extra.keys())
        if exclude is None:
            exclude = extra_keys
        elif isinstance(exclude, set):
            exclude |= extra_keys
        else:
            exclude = set(exclude) | extra_keys
        return self.DATA | super().model_dump(*args, exclude=exclude, **kwargs)
