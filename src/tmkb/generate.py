from argparse import ArgumentParser
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from tabulate import tabulate

from tmkb.configuration import ConfigSchema, load_config
from tmkb.constants import WHITE_TO_BLACK_KEY_RATIO
from tmkb.kb_modules import *


@dataclass
class ModelGeneratorResult:
    model_name: str
    n_prints: int
    path: Path


def _generate_octave(
    dir: Path,
    conf: ConfigSchema,
) -> tuple[OctaveBuilder, tuple[ModelGeneratorResult, ...]]:
    octaves_cnt = conf.key_count // 12
    octave = OctaveBuilder(7, conf)
    octave_path = octave.full_export(dir, "full_octave")[-1]

    backplate_path = BackplateBuilder(octave, conf).full_export(
        dir, "full_octave_backplate"
    )[-1]

    return octave, (
        ModelGeneratorResult(
            model_name="Full Octave", n_prints=octaves_cnt, path=octave_path
        ),
        ModelGeneratorResult(
            model_name="Full Octave backplate",
            n_prints=octaves_cnt,
            path=backplate_path,
        ),
    )


@cache
def _get_partial_keys_cnt(key_count: int) -> tuple[int, int]:
    free_keys = key_count % 12
    partial_octave_keys = max(
        filter(lambda x: sum(x) <= free_keys, WHITE_TO_BLACK_KEY_RATIO.items()), key=sum
    )
    # returns white keys, black keys combo
    return partial_octave_keys


def _generate_partial_octave(
    dir: Path, conf: ConfigSchema
) -> tuple[ModelGeneratorResult, ...]:
    wk_count, _ = _get_partial_keys_cnt(conf.key_count)

    partial_octave = OctaveBuilder(wk_count, conf)
    partial_octave_path = partial_octave.full_export(dir, "partial_octave")[-1]
    backplate_path = BackplateBuilder(partial_octave, conf).full_export(
        dir, "partial_octave_backplate"
    )[-1]

    return (
        ModelGeneratorResult(
            model_name="Partial Octave", n_prints=1, path=partial_octave_path
        ),
        ModelGeneratorResult(
            model_name="Partial Octave Backplate",
            n_prints=1,
            path=backplate_path,
        ),
    )


def _generate_keys(
    dir: Path,
    conf: ConfigSchema,
) -> tuple[ModelGeneratorResult, ...]:
    octave_cnt = conf.key_count // 12
    white_cnt = octave_cnt * 7
    black_cnt = octave_cnt * 5
    try:
        partial_white_cnt, partial_blk_cnt = _get_partial_keys_cnt(conf.key_count % 12)
        white_cnt += partial_white_cnt
        black_cnt += partial_blk_cnt
    except ValueError:
        print("skipped calculation of keys for partial octave")

    white_key_path = MxKeyBuilder.mx_key_factory(MxKeyType.WHITE, conf).full_export(
        dir, "white_key"
    )[-1]
    black_key_path = MxKeyBuilder.mx_key_factory(MxKeyType.BLACK, conf).full_export(
        dir, "black_key"
    )[-1]
    octave_key_path = MxKeyBuilder.mx_key_factory(
        MxKeyType.OCTAVE_CONTROLLER, conf
    ).full_export(dir, "octave_key")[-1]
    return (
        ModelGeneratorResult("White MX key", n_prints=white_cnt, path=white_key_path),
        ModelGeneratorResult("Black MX key", n_prints=black_cnt, path=black_key_path),
        ModelGeneratorResult(
            "Octave Controller MX key", n_prints=2, path=octave_key_path
        ),
    )


def _generate_controller_case(
    dir: Path, octave: OctaveBuilder, conf: ConfigSchema
) -> tuple[ModelGeneratorResult, ...]:
    case = CrontrollerCaseBuilder(octave, conf)
    case_path = case.full_export(dir, "controller_case")[-1]
    backplate_path = BackplateBuilder(case, conf).full_export(
        dir, "controller_case_backplate"
    )[-1]

    return (
        ModelGeneratorResult(model_name="Controller case", n_prints=1, path=case_path),
        ModelGeneratorResult(
            model_name="Controller case backplate", n_prints=1, path=backplate_path
        ),
    )


def _generate_end_cap(
    dir: Path, octave: OctaveBuilder, conf: ConfigSchema
) -> tuple[ModelGeneratorResult, ...]:
    end_cap = EndCapBuilder(octave, conf)
    end_cap_path = end_cap.full_export(dir, "end_cap")[-1]
    backplate_path = BackplateBuilder(end_cap, conf).full_export(
        dir, "end_cap_backplate"
    )[-1]

    return (
        ModelGeneratorResult(model_name="End Cap", n_prints=1, path=end_cap_path),
        ModelGeneratorResult(
            model_name="End Cap backplate", n_prints=1, path=backplate_path
        ),
    )


def generate_all(config_path: str) -> None:
    conf = load_config(Path(config_path))
    (conf.output_dir / "scads").mkdir(parents=True, exist_ok=True)
    (conf.output_dir / "stls").mkdir(parents=True, exist_ok=True)
    (conf.output_dir / "steps").mkdir(parents=True, exist_ok=True)

    results: list[ModelGeneratorResult] = []

    octave, octave_res = _generate_octave(conf.output_dir, conf)
    results.extend(octave_res)
    print("(1/5) Generated Octave")
    results.extend(_generate_controller_case(conf.output_dir, octave, conf))
    print("(2/5) Generated controller case")
    results.extend(_generate_end_cap(conf.output_dir, octave, conf))
    print("(3/5) Generated end cap")
    results.extend(_generate_keys(conf.output_dir, conf))
    print("(4/5) generated keys")

    try:
        partial_res = _generate_partial_octave(conf.output_dir, conf)
        results.extend(partial_res)
        print("(5/5) Generated partial octave")
    except ValueError:
        print("(5/5) Skipped partial octave")

    sorted_results = sorted(results, key=lambda x: x.n_prints)
    print(
        tabulate(
            sorted_results,  # type: ignore
            headers="keys",
            tablefmt="fancy_grid",
        )
    )


def main():
    arg_parser = ArgumentParser(
        "2Mkb generator",
        "uv run generate --conf <CONFIG YAML PATH>",
    )
    arg_parser.add_argument(
        "-c", "--conf", type=str, default="src/configs/default.conf.yaml"
    )
    args = arg_parser.parse_args()
    generate_all(args.conf)
