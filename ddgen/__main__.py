import os
from pathlib import Path
import argparse
import json
import pandas as pd
from pprint import pprint
from .ddgen import Ddgen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'type', choices=["json", "csv"], help="Type of data to be produced")
    parser.add_argument("--schema", action="store_true",
                        help="flag to generate json from json schema")
    parser.add_argument("--path", default=None, help="Path of Json schema")

    parser.add_argument("fields",
                        nargs='*', help="Enter name of the fields")
    parser.add_argument("--limit", "-l", type=int, default=1,
                        help="Number of examples you want to print")
    parser.add_argument("--output_path", "-o", type=str,
                        help="Output file path")

    args = parser.parse_args()

    script_path = os.path.abspath(
        args.path) if args.path is not None else args.path

    output_path = os.path.abspath(
        args.output_path) if args.output_path is not None else args.output_path

    ddgen = Ddgen(type=args.type)

    output = ddgen.generate(
        limit=args.limit, fields=args.fields, schema_path=script_path)

    pprint(output, indent=2)

    if (output_path):
        ddgen.save_to_path(output, output_path)


if __name__ == "__main__":
    main()
