# Oak

Group of tools to work with genealogical data.

## Installation

Install dependencies with `pip install -r requirements.txt`.

## Commands

### oak_inspect

Inspect for available data at a path and show a summary of the files, persons and warnings.

```
usage: oak_inspect.py [-h] --input_path INPUT_PATH

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH
                        Path to the family data.
```

### oak_tree

Visualize a family tree based on the [Graphviz](https://graphviz.org) software :

```
usage: oak_tree.py [-h] --input_file_path INPUT_FILE_PATH [--config_file_path CONFIG_FILE_PATH] [--output_dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --input_file_path INPUT_FILE_PATH
                        Path to the file containing the family data.
  --config_file_path CONFIG_FILE_PATH
                        Path to the YAML file containing configuration of the family tree. This file is optionnal.
  --output_dir OUTPUT_DIR
                        Path to the output directory. Take current folder as default.
```

### oak_stats

Generate stats from the infos of the members of a family :

```
usage: oak_stats.py [-h] --input_file_path INPUT_FILE_PATH [--output_dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --input_file_path INPUT_FILE_PATH
                        Path to the file containing the family data.
  --output_dir OUTPUT_DIR
                        Path to the output directory. Take current folder as default.
```

