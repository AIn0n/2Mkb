from typing import Callable

OptionalCopyField = float | Callable[[float], float] | None


def resolve_optional_copy_field(arg: float, field: OptionalCopyField) -> float:
    if field is None:
        return arg
    if isinstance(field, float) or isinstance(field, int):
        return field
    return field(arg)
