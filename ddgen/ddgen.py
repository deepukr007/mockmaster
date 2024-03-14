from pathlib import Path
from utils import generate_single_field, generate_from_schema, get_json_schema, validate_json_schema, get_content
import argparse
import json
import pandas as pd


def generate_and_get_json_from_shema(schema_path, limit):
    schema_path = Path(schema_path)
    schema = get_json_schema(schema_path)
    processed_data_list = {}
    processed_data = {}
    processed_data_list["data"] = []
    response_raw = generate_from_schema(schema, limit)
    processed_data = get_content(response_raw)
    json_object = json.loads(processed_data)

    single_object = {}
    objects = list(json_object.values())[0]
    if len(objects) == 1:
        single_object = objects[0]
        validate_json_schema(single_object, schema)
        return single_object
    else:
        for object in objects:
            validate_json_schema(object, schema)
            single_object = object
            processed_data_list["data"].append(single_object)

    return processed_data_list


def generate_and_get_json(fields, limit):
    if limit > 0:
        data = {}
        for field in fields:
            response_raw = generate_single_field(field, limit)
            response = get_content(response_raw)
            json_response = json.loads(response)
            data[field] = list(json_response.values())[0]
        processed_data_list = {}
        processed_data_list["data"] = []

        keys = list(data.keys())
        for i in range(limit):
            processed_data = {}
            for j in range(len(keys)):
                key = keys[j]
                processed_data[key] = data[key][i]
            if (limit == 1):
                return processed_data
            processed_data_list["data"].append(processed_data)
        return processed_data_list


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
            print(output)

        if args.schema != True:
            output = generate_and_get_json(args.fields, args.limit)
            print(output)

        if args.type == "json":
            if args.output_path is not None:
                with open(Path(f"{args.output_path}/output.json"), 'w') as file:
                    json.dump(output, file)

        if args.type == "csv":
            output_data = output.get("data", output)
            df = pd.json_normalize(output_data)
            df.to_csv('output.csv', index=False, encoding='utf-8')
            print(df)
            if args.output_path is not None:
                df.to_csv(Path(f"{args.output_path}/output.csv"),
                          index=False, encoding='utf-8')
