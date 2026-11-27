from itertools import accumulate
from math import atan2, degrees, sqrt
from typing import Any

from solid2 import cube, square

from tmkb.primitives.base_builders import ModelBuilder, GroupBuilder
from tmkb.primitives.cube_builders import CubeBuilder
from tmkb.primitives.copy_fields import OptionalCopyField, resolve_optional_copy_field


class SlopeBuilder(ModelBuilder):
    def __init__(self, dx: float, dy: float, dz: float):
        super().__init__(0, 0, 0, dx, dy, dz)

    def copy_and_modify(
        self,
        new_x: OptionalCopyField = None,
        new_y: OptionalCopyField = None,
        new_z: OptionalCopyField = None,
        new_dx: OptionalCopyField = None,
        new_dy: OptionalCopyField = None,
        new_dz: OptionalCopyField = None,
    ) -> SlopeBuilder:
        copy = SlopeBuilder(
            resolve_optional_copy_field(self.dx, new_dx),
            resolve_optional_copy_field(self.dy, new_dy),
            resolve_optional_copy_field(self.dz, new_dz),
        )
        copy.move(
            [
                resolve_optional_copy_field(self.x, new_x),
                resolve_optional_copy_field(self.y, new_y),
                resolve_optional_copy_field(self.z, new_z),
            ]
        )
        return copy

    def _slope(self):
        sqr = square([self.dx, self.dy])
        rad_angle = atan2(self.dy, self.dz)
        angle = degrees(rad_angle)

        return sqr.linear_extrude(self.dz) - sqr.linear_extrude(
            sqrt(self.dx**2 + self.dy**2) * 1.5
        ).rotateX(-angle)

    def build(self):
        return self._slope().translate([self.x, self.y, self.z])


class SquareXPunchedSlopeBuilder(GroupBuilder):
    def __init__(
        self,
        dx: float,
        dy: float,
        dz: float,
        distances: list[float],
        hole_dx: float,
    ) -> None:
        self.holes: list[CubeBuilder] = []
        for dist in accumulate(distances):
            hole = CubeBuilder(hole_dx, dy, dz)
            hole.move([dist, 0, 0])
            self.holes.append(hole)
        self.slope = SlopeBuilder(dx, dy, dz)
        super().__init__()

    def build(self) -> Any:
        model = self.slope.build()
        for hole in self.holes:
            model -= hole.build()
        return model
