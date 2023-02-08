#!/usr/bin/env python3

from VideoTree import videotree
from os import path
import traceback
import argparse
import sys
from VideoTree.output import structure_output_as_json, structure_output_as_text

abspath = path.abspath

output_format_list = {
    "text": structure_output_as_text,
    "json": structure_output_as_json,
}


def run() -> None:
    args = argparse.ArgumentParser()
    args.add_argument("path", type=str, help="Path to the directory")
    args.add_argument(
        "-f",
        "--filter",
        type=int,
        help="Filter videos by length equal or greater than the given value in minutes",
        default=10,
    )
    args.add_argument(
        "-j", "--json", action="store_true", help="Output as json", default=False
    )

    path = abspath(args.parse_args().path)
    f = args.parse_args().filter or 10
    is_json = args.parse_args().json

    if not is_json:
        print(f"VideoTree is running on {path} with filter {f}")

    try:
        fn = output_format_list["json" if is_json else "text"]

        out = videotree(path, fn, time_filter=f)

        if out == "" and not is_json:
            print("Found no videos in the given path")
            return

        print(out)
    except Exception:
        print("Error running VideoTree", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)


run()
