# libraries to install in Terminal
# pip install termcolor
# pip install tabulate
# pip install pyfiglet

#importing libraries
import threading
import time
import sys
from pathlib import Path
from ddgen import generate_and_get_json, generate_and_get_json_from_shema
import argparse
import json
import pandas as pd
from tabulate import tabulate
from termcolor import colored
from pyfiglet import Figlet


# --------------------------------------------------------------
# Beautifying settings
# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 100)
pd.set_option('display.colheader_justify', 'center')

# Initialize loading flag and lock
loading = False
loading_lock = threading.Lock()

# welcome message
def print_welcome_message():
    f = Figlet(font='slant')  # You can experiment with different fonts
    welcome_message = f.renderText("Welcome to DDGen!")
    print(f"{GREEN}{welcome_message}{ENDC}")

def print_colorful_df(df):
    # Converting df to a table using tabulate
    table = tabulate(df, headers='keys', tablefmt='grid', showindex=False)
    # Spliting the table into lines
    lines = table.split('\n')

    # Apply color to the header line
    lines[1] = colored(lines[1], 'red')
    for line in lines:
        if '---'  in line:  # Separator line
            print(colored(line, 'yellow'))
        elif lines.index(line) == 1:  # Header line
            print(colored(line, 'red'))
        else:  # Other lines
            print(colored(line, 'white'))  # Color other lines 


# Loading Bar / Progress Bar
def print_loading_bar():
    global loading
    bar_length = 40
    completed_percentage = 0
    increase_step = 4
    with loading_lock:
        loading = True
    sys.stdout.write("\n")
    while loading:
        with loading_lock:
            completed_percentage = min(completed_percentage + increase_step, 100)
            bar = '█' * (completed_percentage * bar_length // 100)
            bar += '-' * (bar_length - len(bar))
            sys.stdout.write(f"\rLoading: [{YELLOW}{bar}{ENDC}] {completed_percentage}%%")
            sys.stdout.flush()
            if completed_percentage >= 100:
                loading = False
        time.sleep(0.1)  # Simulate loading progress
    sys.stdout.write("\n") 
# --------------------------------------------------------------

def print_instructions():
    instructions = f"""
{GREEN}Instructions:{ENDC}
- Use the 'json' argument to output data in JSON format.
- Use the 'csv' argument to output data in CSV format.
- Use '--schema' followed by a path to generate data from a JSON schema.
- Use '--limit' followed by a number to specify the number of data entries.
- Provide field names as additional arguments to generate specific fields.

Example usage:
  python3 __main__.py csv name place --limit 10
  python3 __main__.py json --schema schema.json --limit 5 
"""
    print(instructions)

# --------------------------------------------------------------
# Capitalize the first letter of each column name
def capitalize_column_names(df):
    df.columns = [col.capitalize() for col in df.columns]
    return df

# --------------------------------------------------------------
if __name__ == "__main__":
    print_welcome_message()
    print_instructions()

    if not loading:
        with loading_lock:
            loading_thread = threading.Thread(target=print_loading_bar)
            loading_thread.start()
    
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=["json", "csv"], help="Type of data to be produced")
    parser.add_argument("--schema", action="store_true", help="Flag to generate json from json schema")
    parser.add_argument("--path", help="Path of Json schema")
    parser.add_argument("fields", nargs='*', help="Enter name of the fields")
    parser.add_argument("--limit", "-l", type=int, default=1, help="Number of examples you want to print")
    parser.add_argument("--output_path", "-o", type=str, help="Output file path")

    args = parser.parse_args()

    try:
        time.sleep(0.1)
        if args.type == "json" or args.type == "csv":
            if args.schema:
                output = generate_and_get_json_from_shema(args.path, args.limit)
            else:
                output = generate_and_get_json(args.fields, args.limit)
           
            if args.type == "json":
                pretty_json_output = json.dumps(output, indent=4)  # For pretty printing
                if args.output_path is not None:
                    with open(Path(f"{args.output_path}/output.json"), 'w') as file:
                        file.write(pretty_json_output)  # Writing the prettified JSON to a file
                else:
                    print(pretty_json_output)  # Printing JSON to the console

            elif args.type == "csv":
                output_data = output.get("data", output)
                df = pd.json_normalize(output_data)
            # Capitalizing column names
                df = capitalize_column_names(df)
                if args.output_path is not None:
                    csv_path = Path(f"{args.output_path}/output.csv")
                    df.to_csv(csv_path, index=False, encoding='utf-8')
                print_colorful_df(df)  # Print beautified df
    except Exception as e:
        print(f"{RED}An error occurred: {e}{ENDC}")
    finally:
        with loading_lock:  # Acquire lock before changing 'loading' state
            loading = False
        loading_thread.join()  # Wait for the loading bar to finish
