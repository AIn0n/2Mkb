from solid2 import cube, cylinder

from .base_builders import ModelBuilder
from .copy_fields import OptionalCopyField, resolve_optional_copy_field


class ArcBuilder(ModelBuilder):
    def __init__(self, width: float, len_height: float, segments: int) -> None:
        self.fn = segments
        super().__init__(0, 0, 0, width, len_height, len_height)

    def copy_and_modify(
        self,
        new_dx: OptionalCopyField = None,
        new_dyz: OptionalCopyField = None,
        new_x: OptionalCopyField = None,
        new_y: OptionalCopyField = None,
        new_z: OptionalCopyField = None,
    ):
        copy = ArcBuilder(
            resolve_optional_copy_field(self.dx, new_dx),
            resolve_optional_copy_field(self.dy, new_dyz),
            self.fn,
        )
        copy.move(
            [
                resolve_optional_copy_field(self.x, new_x),
                resolve_optional_copy_field(self.y, new_y),
                resolve_optional_copy_field(self.z, new_z),
            ]
        )
        return copy

    def _arc(self):
        return (
            (
                cube([self.dy, self.dy, self.dx])
                - cylinder(r=self.dz, h=self.dx, _fn=self.fn)
            )
            .rotateY(90)
            .translateZ(self.dz)
        )

    def build(self):
        return self._arc().translate([self.x, self.y, self.z])


class InvertedArcBuilder(ModelBuilder):
    def __init__(self, width: float, len_height: float, segments: int) -> None:
        self.fn = segments
        super().__init__(0, 0, 0, width, len_height, len_height)

    def _arc(self):
        return (
            (
                cube([self.dy, self.dy, self.dx])
                - cylinder(r=self.dz, h=self.dx, _fn=self.fn).translate(
                    [self.dy, self.dy, 0]
                )
            )
            .rotateY(90)
            .translateZ(self.dz)
        )

    def build(self):
        return self._arc().translate([self.x, self.y, self.z])
