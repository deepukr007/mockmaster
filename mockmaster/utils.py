from openai import OpenAI
import os
from pathlib import Path
import json
from jsonschema import validate
import pandas as pd
from pyfiglet import Figlet
from tabulate import tabulate
from termcolor import colored
from dotenv import load_dotenv, set_key

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'


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

    return [{"role": "system", "content": f"Generate {number} example data for given json schema by user. The output should be strictly in json array format  with key as data"},
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
    f = Figlet(font='slant')
    welcome_message = f.renderText("Welcome to MockMaster!")
    print(f"{GREEN}{welcome_message}{ENDC}")


def init_openai_client(api_key):
    global client
    client = OpenAI(
        api_key=api_key
    )
    return client


def get_set_api_key(change=False):
    env_file = Path(os.path.abspath(".env"))
    api_key = os.environ.get("OPENAI_API_KEY")

    if env_file.is_file():
        load_dotenv(env_file)
        api_key = os.environ.get("OPENAI_API_KEY")
    else:
        env_file.touch()

    if (api_key):
        if (change):
            if (set):
                prompt = input(
                    "Do you want to replace existing API key ? (Y/n) ")
                if (prompt.lower() == "y"):
                    api_key = input("Enter API Key : ")
                    os.environ["OPENAI_API_KEY"] = api_key.strip()
                    set_key(env_file, "OPENAI_API_KEY",
                            os.environ["OPENAI_API_KEY"])
                    print("API key is changed")
                else:
                    print("API key is not changed")
        return api_key

    else:
        prompt = input(
            "No API key found,Do you want to store new API Key ? (Y/n) ")
        if (prompt.lower() == "y"):
            api_key = input("Enter API Key : ")
            os.environ["OPENAI_API_KEY"] = api_key.strip()
            set_key(env_file, "OPENAI_API_KEY",
                    os.environ["OPENAI_API_KEY"])
            print("API key is added")
            return api_key
    return None


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


def print_instructions():
    instructions = f"""
        {GREEN}Instructions:{ENDC}
        {YELLOW}- Use 'generate' for data generation mode after initialising
        - Use the 'json' argument to output data in JSON format.
        - Use the 'csv' argument to output data in CSV format.
        - Use '--schema' followed by a path to generate data from a JSON schema.
        - Use '--limit' followed by a number to specify the number of data entries.
        - Provide field names as additional arguments to generate specific fields.{ENDC}

        {GREEN}Example usage:{ENDC}
        {YELLOW}mockmaster generate csv name place --limit 10
        mockmaster generate json name place gender --limit 18
        mockmaster generate json --schema schema.json --limit 5{ENDC}
        """
    print(instructions)
