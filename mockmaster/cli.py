import os
from pathlib import Path
import argparse
import json
import pandas as pd
from pprint import pprint

from .utils import get_set_api_key, init_openai_client, print_colored_df, print_instructions, welcome_message
from .mockmaster import Mockmaster


def main():
    try:
        parser = argparse.ArgumentParser(
            prog="Dummy Data Generator", description="A CLI tool to generate dummy data using GPT")

        subparsers = parser.add_subparsers(help="Commands for the CLI")
        init_parser = subparsers.add_parser(
            'init', help='Initialise the CLI app')
        init_parser.set_defaults(which='init')

        gen_parser = subparsers.add_parser('generate', help='Generate data')
        gen_parser.set_defaults(which='gen')

        gen_parser.add_argument(
            'type', choices=["json", "csv"], help="Type of data to be produced")
        gen_parser.add_argument("--schema", action="store_true",
                                help="flag to generate json from json schema")
        gen_parser.add_argument("--path", default=None,
                                help="Path of Json schema")
        gen_parser.add_argument("fields", nargs="*",
                                help="Enter name of the fields")
        gen_parser.add_argument("--limit", "-l", type=int, default=1,
                                help="Number of examples you want to print")
        gen_parser.add_argument("--output_path", "-o", type=str,
                                help="Output file path")
        gen_parser.add_argument("--print_raw", action="store_true",
                                help="Output file path")

        args = parser.parse_args()

        if (args.which == "init"):
            welcome_message()
            print_instructions()
            get_set_api_key(change=True)

        elif (args.which == "gen"):
            api_key = get_set_api_key(change=False)
            init_openai_client(api_key)

            script_path = os.path.abspath(
                args.path) if args.path is not None else args.path

            output_path = os.path.abspath(
                args.output_path) if args.output_path is not None else args.output_path

            ddgen = Mockmaster(type=args.type)
            output = ddgen.generate(
                limit=args.limit, fields=args.fields, schema_path=script_path)

            if args.type == "json":
                pprint(output, indent=2)

            elif args.type == "csv":
                print_colored_df(output)

            if (output_path):
                ddgen.save_to_path(output, output_path)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
