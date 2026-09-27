from argparse import ArgumentParser
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from tmkb.configuration import ConfigSchema, load_config
from tmkb.constants import WHITE_TO_BLACK_KEY_RATIO
from tmkb.kb_modules import *


@dataclass
class ModelGeneratorResult:
    model_name: str
    n_prints: int
    path: Path


def _generate_octave(conf: ConfigSchema) -> tuple[OctaveBuilder, ModelGeneratorResult]:
    octaves_cnt = conf.key_count // 12
    octave_path = conf.output_dir / "full_octave.stl"
    octave = OctaveBuilder(7, conf)

    octave.to_stl(octave_path)

    return octave, ModelGeneratorResult(
        model_name="Full Octave", n_prints=octaves_cnt, path=octave_path
    )


@cache
def _get_partial_keys_cnt(key_count: int) -> tuple[int, int]:
    free_keys = key_count % 12
    partial_octave_keys = max(
        filter(lambda x: sum(x) <= free_keys, WHITE_TO_BLACK_KEY_RATIO.items()), key=sum
    )
    # returns white keys, black keys combo
    return partial_octave_keys


def _generate_partial_octave(conf: ConfigSchema) -> ModelGeneratorResult:
    wk_count, _ = _get_partial_keys_cnt(conf.key_count)
    partial_octave_path = conf.output_dir / "partial_octave.stl"

    partial_octave = OctaveBuilder(wk_count, conf)
    partial_octave.to_stl(partial_octave_path)

    return ModelGeneratorResult(
        model_name="Partial Octave", n_prints=1, path=partial_octave_path
    )


def _generate_white_keys(conf: ConfigSchema) -> ModelGeneratorResult:
    octave_cnt = conf.key_count // 12
    white_cnt = octave_cnt * 7
    black_cnt = octave_cnt * 5
    try:
        partial_white_cnt, partial_blk_cnt = _get_partial_keys_cnt(conf.key_count % 12)
        white_cnt += partial_white_cnt
        black_cnt += partial_blk_cnt
    except ValueError as e:
        print("skipped calculation of keys for partial octave")


def generate_all(config_path: str) -> None:
    conf = load_config(Path(config_path))
    conf.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[ModelGeneratorResult] = []

    octave, octave_res = _generate_octave(conf)

    results.append(octave_res)
    try:
        partial_res = _generate_partial_octave(conf)
        results.append(partial_res)
    except ValueError as e:
        print("skipped partial octave generation")

    print("generate all the parts!")


def main():
    arg_parser = ArgumentParser(
        "2Mkb generator",
        "uv run generate_all --conf <CONFIG YAML PATH>",
    )
    arg_parser.add_argument(
        "-c", "--conf", type=str, default="src/configs/default.conf.yaml"
    )
    args = arg_parser.parse_args()
    generate_all(args.conf)
