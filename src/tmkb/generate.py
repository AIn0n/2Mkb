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
    conf: ConfigSchema,
) -> tuple[OctaveBuilder, tuple[ModelGeneratorResult, ...]]:
    octaves_cnt = conf.key_count // 12
    octave = OctaveBuilder(7, conf)
    octave_path = conf.output_dir / "full_octave.stl"
    octave.to_stl(octave_path)

    octave_backplate_path = conf.output_dir / "full_octave_backplate.stl"
    BackplateBuilder(octave, conf).to_stl(octave_backplate_path)

    return octave, (
        ModelGeneratorResult(
            model_name="Full Octave", n_prints=octaves_cnt, path=octave_path
        ),
        ModelGeneratorResult(
            model_name="Full Octave backplate",
            n_prints=octaves_cnt,
            path=octave_backplate_path,
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


def _generate_partial_octave(conf: ConfigSchema) -> tuple[ModelGeneratorResult, ...]:
    wk_count, _ = _get_partial_keys_cnt(conf.key_count)
    partial_octave_path = conf.output_dir / "partial_octave.stl"
    partial_octave_backplate_path = conf.output_dir / "partial_octave_backplate.stl"

    partial_octave = OctaveBuilder(wk_count, conf)
    partial_octave.to_stl(partial_octave_path)
    BackplateBuilder(partial_octave, conf).to_stl(partial_octave_backplate_path)

    return (
        ModelGeneratorResult(
            model_name="Partial Octave", n_prints=1, path=partial_octave_path
        ),
        ModelGeneratorResult(
            model_name="Partial Octave Backplate",
            n_prints=1,
            path=partial_octave_backplate_path,
        ),
    )


def _generate_keys(
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

    white_key_path = conf.output_dir / "white_key.stl"
    black_key_path = conf.output_dir / "black_key.stl"

    MxKeyBuilder.mx_key_factory(True, conf).to_stl(white_key_path)
    MxKeyBuilder.mx_key_factory(False, conf).to_stl(black_key_path)

    return (
        ModelGeneratorResult("White MX key", n_prints=white_cnt, path=white_key_path),
        ModelGeneratorResult("Black MX key", n_prints=black_cnt, path=black_key_path),
    )


def _generate_controller_case(
    octave: OctaveBuilder, conf: ConfigSchema
) -> tuple[ModelGeneratorResult, ...]:
    case_path = conf.output_dir / "controller_case.stl"
    case_backplate_path = conf.output_dir / "controller_case_backplate.stl"

    case = CrontrollerCaseBuilder(octave, conf)
    case.to_stl(case_path)
    BackplateBuilder(case, conf).to_stl(case_backplate_path)

    return (
        ModelGeneratorResult(model_name="Controller case", n_prints=1, path=case_path),
        ModelGeneratorResult(
            model_name="Controller case backplate", n_prints=1, path=case_backplate_path
        ),
    )


def _generate_end_cap(
    octave: OctaveBuilder, conf: ConfigSchema
) -> tuple[ModelGeneratorResult, ...]:
    end_cap_path = conf.output_dir / "end_cap.stl"
    end_cap_backplate_path = conf.output_dir / "end_cap_backplate.stl"

    end_cap = EndCapBuilder(octave, conf)
    end_cap.to_stl(end_cap_path)
    BackplateBuilder(end_cap, conf).to_stl(end_cap_backplate_path)

    return (
        ModelGeneratorResult(model_name="End Cap", n_prints=1, path=end_cap_path),
        ModelGeneratorResult(
            model_name="End Cap backplate", n_prints=1, path=end_cap_backplate_path
        ),
    )


def generate_all(config_path: str) -> None:
    conf = load_config(Path(config_path))
    conf.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[ModelGeneratorResult] = []

    octave, octave_res = _generate_octave(conf)
    results.extend(octave_res)
    print("(1/5) Generated Octave")
    results.extend(_generate_controller_case(octave, conf))
    print("(2/5) Generated controller case")
    results.extend(_generate_end_cap(octave, conf))
    print("(3/5) Generated end cap")
    results.extend(_generate_keys(conf))
    print("(4/5) generated keys")

    try:
        partial_res = _generate_partial_octave(conf)
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
