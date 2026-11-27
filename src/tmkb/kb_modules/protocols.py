from tmkb.kb_modules.mx_keys import MxKeyType
from typing import Protocol, Sequence


class HasKeys(Protocol):
    def get_total_key_positions(
        self, key_type: MxKeyType
    ) -> Sequence[tuple[float, float, float]]: ...

    def build(self, printing_orientation: bool = True): ...
