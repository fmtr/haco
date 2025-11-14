from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Function:
    mask: ClassVar[str] = '{code}'
    code: str

    def __str__(self):
        raw = self.mask.format(code=self.code)
        lines = [line.strip() for line in raw.splitlines()]
        line = ' '.join(lines).strip()
        return line


@dataclass
class Expression(Function):
    mask: ClassVar[str] = 'def (value,data) return {code} end'


@dataclass
class FunctionExpression(Function):

    def __str__(self):
        return f"{super().__str__()}(value,data)"
