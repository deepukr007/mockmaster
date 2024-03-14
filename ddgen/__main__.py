from pathlib import Path
from ddgen import generate_and_get_json, generate_and_get_json_from_shema
import argparse
import json
import pandas as pd


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'type', choices=["json", "csv"], help="Type of data to be produced")
    parser.add_argument("--schema", action="store_true",
                        help="flag to generate json from json schema")
    parser.add_argument("--path", help="Path of Json schema")

    parser.add_argument("fields",
                        nargs='*', help="Enter name of the fields")
    parser.add_argument("--limit", "-l", type=int, default=1,
                        help="Number of examples you want to print")
    parser.add_argument("--output_path", "-o", type=str,
                        help="Output file path")

    args = parser.parse_args()

    if args.type == "json" or "csv":
        if args.schema:
            output = generate_and_get_json_from_shema(args.path, args.limit)

        if args.schema != True:
            output = generate_and_get_json(args.fields, args.limit)

        if args.type == "json":
            if args.output_path is not None:
                with open(Path(f"{args.output_path}/output.json"), 'w') as file:
                    json.dump(output, file)
            print(output)

        if args.type == "csv":
            output_data = output.get("data", output)
            df = pd.json_normalize(output_data)
            df.to_csv('output.csv', index=False, encoding='utf-8')
            print(df)
            if args.output_path is not None:
                df.to_csv(Path(f"{args.output_path}/output.csv"),
                          index=False, encoding='utf-8')
