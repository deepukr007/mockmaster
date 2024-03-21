from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import json
from jsonschema import validate
import pandas as pd
from pyfiglet import Figlet
from tabulate import tabulate
from termcolor import colored


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


def make_prompt_with_schema(schema, number):

    return [{"role": "system", "content": f"Generate {number} example data for given json schema by user and of the schema is invalid just return none. The output should be strictly in json array format  with key as data"},
            {"role": "user", "content": f"{schema}"}
            ]


def get_content(response):
    return response.content


def underscorify(input):
    input = input.replace(" ", "_")
    return input


def generate_single_field(input, number):
    message = make_prompt_no_schema(
        f"Give me {number} random  {input} in json format", input)
    response = gptservice(message)
    return response


def generate_from_schema(schema, limit):
    message = make_prompt_with_schema(schema, limit)
    response = gptservice(message)
    return response


def gptservice(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message


def welcome_message():
    GREEN = '\033[92m'
    ENDC = '\033[0m'
    f = Figlet(font='slant')
    welcome_message = f.renderText("Welcome to DDGen!")
    print(f"{GREEN}{welcome_message}{ENDC}")


def print_colored_df(df):
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.width', 100)
    pd.set_option('display.colheader_justify', 'center')
    table = tabulate(df, headers='keys', tablefmt='grid', showindex=False)
    lines = table.split('\n')

    lines[1] = colored(lines[1], 'red')
    for line in lines:
        if '---' in line:
            print(colored(line, 'yellow'))
        elif lines.index(line) == 1:
            print(colored(line, 'red'))
        else:
            print(colored(line, 'white'))


def sttolist(str):
    return str.split(",")
