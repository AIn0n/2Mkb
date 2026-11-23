from solid2 import cylinder, cube

from tmkb.configuration import ConfigSchema

from .base_builders import ModelBuilder


class StandBuilder(ModelBuilder):
    def __init__(self, height: float, conf: ConfigSchema):
        self.r = conf.stand_r_mm
        self.h = height
        self.hole_r = conf.stand_screw_r_mm
        self.fn = conf.segments
        super().__init__(0, 0, 0, conf.stand_r_mm, conf.stand_r_mm, height)

    def _hole(self):
        return (
            cylinder(h=self.h, r=self.hole_r, _fn=self.fn)
            + cube([self.hole_r, self.hole_r, self.h])
        ).rotateZ(45 + 180)

    def _stand(self):
        return cylinder(h=self.h, r=self.r, _fn=self.fn) - self._hole()

    def build(self):
        return self._stand().translate([self.x, self.y, self.z])

    def get_hole(self):
        return self._hole().translate([self.x, self.y, self.z])
