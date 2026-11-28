# %%

from pathlib import Path

import scad123d
from ocp_vscode import show

from tmkb.configuration import load_config
from tmkb.kb_modules import *

# %%

conf = load_config(Path("../configs/default.conf.yaml"))
conf

# %%

scad_path = conf.output_dir / "scads"
scad_path.mkdir(exist_ok=True, parents=True)

# %%

octave = OctaveBuilder(7, conf)
part = scad123d.import_scad(octave.as_scad(scad_path / "full_octave.scad"))

show(part)

# %%

part = scad123d.import_scad(
    CrontrollerCaseBuilder(octave, conf).as_scad(scad_path / "controller_case.scad")
)

show(part)

# %%

part = scad123d.import_scad(
    EndCapBuilder(octave, conf).as_scad(scad_path / "end_cap.scad")
)

show(part)

# %%

part = scad123d.import_scad(
    MxKeyBuilder.mx_key_factory(MxKeyType.BLACK, conf).as_scad(
        scad_path / "black_key_keycap.scad"
    )
)

show(part)
# %%

part = scad123d.import_scad(
    MxKeyBuilder.mx_key_factory(MxKeyType.WHITE, conf).as_scad(
        scad_path / "white_key_keycap.scad"
    )
)

show(part)

# %%

part = scad123d.import_scad(
    MxKeyBuilder.mx_key_factory(MxKeyType.OCTAVE_CONTROLLER, conf).as_scad(
        scad_path / "octave_keycap.scad"
    )
)

show(part)
# %%
