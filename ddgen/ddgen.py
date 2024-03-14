from pathlib import Path
from utils import generate_single_field, generate_from_schema, get_json_schema, validate_json_schema, get_content
import json


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
