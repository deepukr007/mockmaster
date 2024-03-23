from pathlib import Path
import json

import pandas as pd

from .utils import generate_single_field, generate_from_schema, get_json_schema, validate_json_schema, get_content


class Mockmaster():

    def __init__(self, type):
        self.type = type

    def generate_and_get_json_from_shema(self):
        self.schema = get_json_schema(self.schema_path)
        self.processed_data_list = {}
        self.processed_data = {}
        self.processed_data_list["data"] = []
        self.response_raw = generate_from_schema(self.schema, self.limit)
        self.processed_data = get_content(self.response_raw)
        self.json_object = json.loads(self.processed_data)

        self.single_object = {}
        self.objects = list(self.json_object.values())[0]
        if len(self.objects) == 1:
            self.single_object = self.objects[0]
            validate_json_schema(self.single_object, self.schema)
            return self.single_object
        else:
            for object in self.objects:
                validate_json_schema(object, self.schema)
                self.single_object = object
                self.processed_data_list["data"].append(self.single_object)

        return self.processed_data_list

    def generate_and_get_json(self, fields):
        if self.limit > 0:
            data = {}
            for field in fields:
                response_raw = generate_single_field(field, self.limit)
                response = get_content(response_raw)
                json_response = json.loads(response)
                data[field] = list(json_response.values())[0]
            processed_data_list = {}
            processed_data_list["data"] = []

            keys = list(data.keys())
            for i in range(self.limit):
                processed_data = {}
                for j in range(len(keys)):
                    key = keys[j]
                    processed_data[key] = data[key][i]
                if (self.limit == 1):
                    return processed_data
                processed_data_list["data"].append(processed_data)
            return processed_data_list

    def generate(self, fields, limit, schema_path=None):
        self.limit = limit

        if schema_path:
            self.schema_path = Path(schema_path)
            output = self.generate_and_get_json_from_shema()
        else:
            output = self.generate_and_get_json(fields)

        if self.type == "json":
            return output
        elif self.type == "csv":
            output_data = output.get("data", output)
            df = pd.json_normalize(output_data)
            return df

    def save_to_path(self, content, output_path):
        self.output_path = Path(output_path)

        if self.type == "json":
            with open(Path(f"{self.output_path}/output.json"), "w") as file:
                json.dump(content, file, indent=4)

        elif self.type == "csv":
            content.to_csv(Path(f"{self.output_path}/output.csv"),
                           index=False, encoding='utf-8')
