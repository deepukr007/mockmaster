from pathlib import Path
from utils import generate_single_field, generate_from_schema, get_json_schema, validate_json_schema
import argparse
import json


def get_content(response):
    return response.content


def generate_and_get_json_from_shema(schema_path, limit):
    processed_data = {}
    schema_path = Path(schema_path)
    schema = get_json_schema(schema_path)
    processed_data_list = {}
    processed_data_list["data"] = []
    for i in range(limit):
        response_raw = generate_from_schema(schema)
        processed_data = get_content(response_raw)
        json_object = json.loads(processed_data)
        validate_json_schema(json_object, schema)
        if (limit == 1):
            return json_object
        processed_data_list["data"].append(json_object)
    return processed_data_list


def generate_and_get_json(fields, limit):
    processed_data = {}
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
            for j in range(len(keys)):
                key = keys[j]
                processed_data[key] = data[key][i]
                if (limit == 1):
                    return processed_data

            print(processed_data)
            processed_data_list["data"].append(processed_data)
            print(processed_data_list)
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
    parser.add_argument("--limit", type=int, default=1,
                        help="Number of examples you want to print")

    args = parser.parse_args()

    if args.type == "json" or "csv":
        if args.schema:
            output = generate_and_get_json_from_shema(args.path, args.limit)
            print(output)

        if args.schema != True:
            output = generate_and_get_json(args.fields, args.limit)
            print(output)
