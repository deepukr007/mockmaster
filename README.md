## Welcome to MockMaster

A CLI tool to generate dummy data in various formats using GPT ,designed to meet diverse needs of software engineers .
It can be used to bootstrap your database , serve dummy data to test out your frontend etc..

## Table of contents
- [Features](#features)
- [Basic Usage](#basic-usage)
- [Authors](#authors)
- [To-dos](#to-dos)

## Features
- :books:	Generate data in json or csv format ( more will be added)
- :toolbox:	 Generate data for dynamic fields with no fixed vocabulary.
- :mirror:	Generate json that follows json schema data fromat.
- :lock:	Store output in specified path.

## What's Unique and better
- :smile:	 Usage of GPT for dummy data generation
- :smiley: No pre built dictionary for fixed set of keys and values
- :sweat_smile: Data generation follows json schema and generated datafrom gpt is validated to make ouput more reliable

## What's not good
- :roll_eyes: Json or csv generated with field inputs may have no linking for all fields ex- email generated will not match with first name or last name
- :expressionless: only openAI GPT is supported for now
- :roll_eyes: only json and csv is supported 

## Basic Usage

### Step 1: Installation

#### Install from pip
```
pip install mockmaster==0.0.2
```

#### Installing from source

```
git clone https://github.com/deepukr007/mockmaster.git
cd mockmaster
```
```
pip install .
```

### Step 2:
Set or edit openAI API key and store it in .env file 
```
mockmaster init
```

### Step 3:

Example 1: Json with fields
```
mockmaster generate json name place age zip_code --limit 10
```

Example 2: Json with schema
```
mockmaster generate json --schema --path <path_to_schema>
```

Example 3:
```
mockmaster generate csv name place age zip_code --limit 10 -o <output_path>
```

### To-dos
- Add support to other llms
- Change stratergy to store API keys
- Python SDK like faker

#### Authors
-  Deepu Krishnareddy
-  Harish Mohan








