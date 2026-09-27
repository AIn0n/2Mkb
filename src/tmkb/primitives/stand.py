from solid2 import cylinder

from tmkb.configuration import ConfigSchema

from .base_builders import ModelBuilder


class StandBuilder(ModelBuilder):
    def __init__(self, height: float, conf: ConfigSchema):
        self.r = conf.stand_r_mm
        self.h = height
        self.hole_r = conf.stand_screw_r_mm
        super().__init__(0, 0, 0, conf.stand_r_mm, conf.stand_r_mm, height)

    def _stand(self):
        return cylinder(h=self.h, r=self.r) - cylinder(h=self.h, r=self.hole_r)

    def build(self):
        return self._stand().translate([self.x, self.y, self.z])
