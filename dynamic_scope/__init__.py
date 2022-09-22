import inspect
from ast import Raise
from collections import abc
from types import FunctionType
from typing import Any, Dict, Iterator, Optional


class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}

    def __getitem__(self, key: str) -> Optional[Any]:
        if not self.env.__contains__(key):
            raise NameError(f"Name '{key}' is not defined.")
        return self.env[key]
    
    def __setitem__(self, key: str, value: Optional[Any]):
        self.env[key] = value

    def __iter__(self) -> Iterator[str]:
        return self.env.__iter__()
    
    def __len__(self) -> int:
        return self.env.__len__()


def get_dynamic_re() -> DynamicScope:
    return DynamicScope()
