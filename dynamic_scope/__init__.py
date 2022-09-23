import inspect
from collections import abc
from typing import Any, Dict, Iterator, Optional

# Nick Lay
# Credit: Our Hours Special Dynamo Session - 9/22/22


class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}

    def __getitem__(self, key: str) -> Optional[Any]:
        if key not in self.env.keys():
            raise NameError(f"Name '{key}' is not defined.")
        if self.env[key] == '__unbound__':
            raise UnboundLocalError(
                f"Name '{key}' was referenced before assignment.")
        return self.env[key]

    def __setitem__(self, key: str, value: Optional[Any]):
        if key not in self.env.keys():
            self.env[key] = value

    def __iter__(self) -> Iterator[str]:
        return self.env.__iter__()

    def __len__(self) -> int:
        return len(self.env)


def get_dynamic_re() -> DynamicScope:
    dyn_scope = DynamicScope()
    stack = inspect.stack()
    for frame_info in stack[1::]:
        frame = frame_info.frame
        free_vars = list(frame.f_code.co_freevars)

        local_vars = {key: value for (
            key, value) in frame.f_locals.items() if key not in free_vars}
        for var_name, var_value in local_vars.items():
            dyn_scope[var_name] = var_value

        # No local variables in frame, but some variables exist
        # Therefore, we have unbound variables for this scope
        # Set as '__unbound__' as an indicator value for this condition
        # This allows NoneTypes to work
        all_vars = frame.f_code.co_cellvars+frame.f_code.co_varnames
        if not len(frame.f_locals) and len(all_vars):
            for var in all_vars:
                dyn_scope[var] = '__unbound__'

    return dyn_scope
