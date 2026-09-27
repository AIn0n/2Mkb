from typing import Any

from solid2 import circle, polygon, square
from solid2.extensions.bosl2 import round_corners

from tmkb.configuration import ConfigSchema
from tmkb.primitives import ModelBuilder


class MxKeyBuilder(ModelBuilder):
    def __init__(self, dx: float, dy: float, conf: ConfigSchema):
        self.u = conf.keycap_u
        self.h = conf.keycap_height_mm
        self.rounding_radius = conf.keycap_rounding_corner_mm
        super().__init__(0, 0, 0, dx, dy, 0)

    def _generate_mx_stem(self):
        mx_stem_l = 4.0
        mx_stem_w = 1.2
        mx_stem_h = 3.5

        mx_stem_arm = square([mx_stem_l, mx_stem_w], center=True)
        mx_stem_base = circle(d=5.5) - (mx_stem_arm + mx_stem_arm.rotateZ(90))

        return mx_stem_base.linear_extrude(height=mx_stem_h)

    def _generate_key(self):
        stem = self._generate_mx_stem()
        keycap_base = square([self.u * self.dx, self.u * self.dy], center=True)
        rounded_keycap = polygon(
            round_corners(path=keycap_base, radius=self.rounding_radius)
        ).linear_extrude(height=self.h)
        return rounded_keycap + stem.up(self.h - 0.01)

    def build(self) -> Any:
        return self._generate_key().translate([self.x, self.y, self.z])

    @staticmethod
    def mx_key_factory(white: bool, conf: ConfigSchema) -> MxKeyBuilder:
        if white:
            return MxKeyBuilder(
                conf.white_key_dims.width, conf.white_key_dims.length, conf
            )
        return MxKeyBuilder(conf.black_key_dims.width, conf.black_key_dims.length, conf)
