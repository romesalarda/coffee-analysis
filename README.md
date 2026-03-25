# Coffee-analysis

## Description

This code analyses a database of coffee suppliers, to create a few visual graphs and rank the coffee suppliers based on flavor, aroma, uniformity and a few other criteria. 

The code returns the top 5 suppliers based on these criteria.

## Installation
1. Create a virtual environment
```bash
py -m venv venv
```

2. Ensure you activate the environment
For windows
```bash
venv\Scripts\Activate.ps1
```

For other
```bash
venv\Scripts\activate
```
or 
```bash
venv\Scripts\activate.bat
```

3. Install requirements
Either using
```bash
python3 -m pip install -r "requirements.txt"
```
or 
```bash
py -m pip install -r "requirements.txt"
```
whichever version of python you are using

## Usage

In the command line in the current directory where this README.md file is, run:
```bash
python3 main.py
```

A successfull output should provide you a PDF file with all the necessary data from the data provided

## Running Tests

To run tests run this command
```bash
pytest tests/graph_tests.py

pytest tests/demo_tests.py
```

## Maintainers
Hathem
Michael
Matthew
Rome

## Licence

## Authors
Hathem
Michael
Matthew
Rome

## Acknowledgements
