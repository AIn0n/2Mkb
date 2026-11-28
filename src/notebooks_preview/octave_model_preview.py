# %%

from pathlib import Path

import scad123d
from ocp_vscode import show

from tmkb.configuration import load_config
from tmkb.kb_modules import BackplateBuilder, OctaveBuilder

# %%

conf = load_config(Path("../configs/default.conf.yaml"))
conf

# %%

builder = OctaveBuilder(7, conf)

# %%

scad_path = conf.output_dir / "scads"
scad_path.mkdir(exist_ok=True, parents=True)


# %%

part = scad123d.import_scad(builder.as_scad(scad_path / "full_octave.scad"))

show(part)
