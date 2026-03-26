# Welcome to Coffee Analysis
## Description

This code analyses a database of coffee suppliers, to create a few visual graphs and rank the coffee suppliers based on flavor, aroma, uniformity and a few other criteria. 

The code returns the top 5 suppliers based on these criteria.

## Project layout
    ...
    main.py    # The main file.
    data/
        simplified_coffee_ratings.csv  # The file being analysed.
        ...    

## Usage

After installation (see [Installation](/install/)), run the following command to process your coffee data and generate a PDF report:
```bash
python main.py [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|---|---|---|---|
| `--input` | string | `data/simplified_coffee_ratings.csv` | Path to the input CSV file |
| `--min_producers` | int | `3` | Minimum number of producers for a country to be included |
| `--min_production` | int | `500` | Minimum production volume (bags × weight in kg) for a producer to be included |
| `--weight_aroma` | float | `1.0` | Weight applied to aroma score |
| `--weight_flavor` | float | `1.0` | Weight applied to flavor score |
| `--weight_uniformity` | float | `1.0` | Weight applied to uniformity score |
| `--weight_species` | float | `1.0` | Weight applied to species score |
| `--weight_other` | float | `1.0` | Weight applied to all other scores |
| `--cwd` | string | `temp/` | Directory for saving output files |

### Examples

Run with defaults:
```bash
python main.py
```

Use a custom input file with stricter producer filtering:
```bash
python main.py --input data/my_coffee_data.csv --min_producers 5
```

Adjust scoring weights to prioritise aroma and flavor:
```bash
python main.py --weight_aroma 2.0 --weight_flavor 2.0
```
