from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import json
from jsonschema import validate

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
)


def get_json_schema(schema_path):
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
        return schema


def validate_json_schema(json, schema):
    try:
        validate(instance=json, schema=schema)
    except Exception as e:
        print("GPT failed to generate output according to schema")
        print(str(e))


def make_prompt_no_schema(user_message, input):

    return [{"role": "system", "content": f"Generate output in json and main key of the json will be named {input} strictly with no extra letters, and the value should be an array of {input} "},
            {"role": "user", "content": f"{user_message}"}
            ]


def make_prompt_with_schema(schema):

    return [{"role": "system", "content": f"Generate example data for given json schema by user and of the schema is invalid just return none. The output should be in json format "},
            {"role": "user", "content": f"{schema}"}
            ]


def underscorify(input):
    input = input.replace(" ", "_")
    return input


def generate_single_field(input, number):
    message = make_prompt_no_schema(
        f"Give me {number} random  {input} in json format", input)
    response = gptservice(message)
    return response


def generate_from_schema(schema):
    message = make_prompt_with_schema(schema)
    response = gptservice(message)
    return response


def gptservice(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message
