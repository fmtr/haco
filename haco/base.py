from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass(kw_only=True)
class Base:
    DATA = dict()

    def model_dump(self) -> dict[str, Any]:
        data = {} | self.DATA
        for fld in fields(self):
            meta = fld.metadata
            if meta.get('exclude', False):
                continue

            value = getattr(self, fld.name)

            if hasattr(value, self.model_dump.__name__):
                value = value.model_dump()
            elif isinstance(value, list):
                value = [v.model_dump() if hasattr(v, self.model_dump.__name__) else v for v in value]

            if value is not None:
                data[fld.name] = value
        return data
