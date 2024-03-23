## Welcome to MockMaster

A CLI tool to generate dummy data in various formats using GPT ,designed to meet diverse needs of software engineers .
It can be used to bootstrap your database , serve dummy data to test out your frontend etc..

## Features
- :books:	Generate data in json or csv format ( more will be added)
- :toolbox:	 Generate data for dynamic fields with no fixed vocabulary.
- :mirror:	Generate json that follows json schema data fromat.
- :lock:	Store output in specified path.

## Basic Usage

### Step 1: Installation

#### Installing from source

```
git clone https://github.com/deepukr007/mockmaster.git
cd mockmaster
```

### Step 2:
```
pip install .
```

### Step 3:
Set or edit openAI API key and store it in .env file 
```
mockmaster init
```

### Step 4:

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








