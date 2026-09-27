from itertools import accumulate
from typing import Any

from solid2 import cube, cylinder, square

from tmkb.configuration import ConfigSchema

from .base_builders import ModelBuilder
from .copy_fields import OptionalCopyField, resolve_optional_copy_field


class CubeBuilder(ModelBuilder):
    def __init__(self, dx, dy, dz) -> None:
        super().__init__(0, 0, 0, dx, dy, dz)

    def copy_and_modify(
        self,
        new_x: OptionalCopyField = None,
        new_y: OptionalCopyField = None,
        new_z: OptionalCopyField = None,
        new_dx: OptionalCopyField = None,
        new_dy: OptionalCopyField = None,
        new_dz: OptionalCopyField = None,
    ) -> CubeBuilder:
        copy = CubeBuilder(
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

    def build(self):
        return cube([self.dx, self.dy, self.dz]).translate([self.x, self.y, self.z])


class KeyRowBuilder(ModelBuilder):
    def __init__(
        self,
        width: float,
        len_: float,
        x_key_offsets: list[float],
        y_offset: float,
        conf: ConfigSchema,
    ):
        self.conf = conf
        self.x_key_offsets = x_key_offsets
        self.y_offset = y_offset
        super().__init__(0, 0, 0, width, len_, self.conf.mount_plate_width)

    def to_cube(self) -> CubeBuilder:
        cube = CubeBuilder(self.dx, self.dy, self.dz)
        cube.move([self.x, self.y, self.z])
        return cube

    def generate_key_row(self):
        mx_hole = square([self.conf.mount_u, self.conf.mount_u]).translateY(
            self.y_offset
        )
        mounting_plate = square([self.dx, self.dy])

        for sep in accumulate(self.x_key_offsets):
            mounting_plate -= mx_hole.translateX(sep)

        return mounting_plate.linear_extrude(self.dz)

    def build(self):
        return self.generate_key_row().translate([self.x, self.y, self.z])


class XRoundedCubeBuilder(ModelBuilder):
    def __init__(self, dx: float, dy: float, dz: float):
        assert dy >= dz
        self.r = dz / 2
        super().__init__(0, 0, 0, dx, dy, dz)

    def build(self) -> Any:
        cyl = cylinder(h=self.dx, d=self.dz)
        c_len = self.dy - self.dz
        c = cube([self.dz, c_len, self.dx])
        return (
            (cyl.translateX(self.r) + c + cyl.translateX(self.r).translateY(c_len))
            .rotateY(90)
            .translateZ(self.dz)
            .translateY(self.r)
            .translate([self.x, self.y, self.z])
        )
