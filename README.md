> [!IMPORTANT]
> **⚠️ This is a work in progress. ⚠️**

# Oak

Group of tools to work with genealogical data.

## Installation

The project needs an installation of [Graphviz](https://graphviz.org) for the `pygraphviz` package (instructions available [here](https://pygraphviz.github.io/documentation/stable/install.html)).

A [devcontainer](https://code.visualstudio.com/docs/devcontainers/create-dev-container) with a default environnement is also available. 

### Python dependencies

The Python dependencies for our different tools can be installed with : 

```
pip install .
```

The Python dev dependencies to review the code can be installed with : 

```
pip install .[dev]
```

## Data

The data is expected to follow the [`Family`](https://github.com/hvdbm/Oak/blob/main/src/family.py) and [`Person`](https://github.com/hvdbm/Oak/blob/main/src/person.py) classes. Current accepted files extensions are `JSON` and `YAML`.

## Commands

### Utils

#### 🔍 oak_inspect

Search for available data at a path and show a summary of the files, persons, errors and warnings.

```
usage: oak_inspect.py [-h] --input_path INPUT_PATH

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        Path to the family data (a file or a folder).
```

#### 📊 oak_stats

Generate stats from the infos of the members of a family :

```
usage: oak_stats.py [-h] --input_path INPUT_PATH [--output_dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        Path to the family data.
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Path to the output directory. Take current folder as default.
```

### Family visualization

#### 🌳 oak_tree

Generate a family as a tree graph with Graphviz :

```
usage: oak_tree.py [-h] --input_path INPUT_PATH [--config_file_path CONFIG_FILE_PATH] [--output_dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        Path to the family data (a file or a folder).
  --config_file_path CONFIG_FILE_PATH, -c CONFIG_FILE_PATH
                        Path to the YAML file containing configuration of the family tree. This file is optionnal.
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Path to the output directory. Take current folder as default.
```

See [Tree README](src/tree/README.md) for more infos on the config file.

#### ☀️ oak_sunburst

Generate a family as a sunburst with Plotly :

```
usage: oak_sunburst.py [-h] --input_path INPUT_PATH --person_id PERSON_ID [--output_dir OUTPUT_DIR]
                       [--output_filename OUTPUT_FILENAME] [--output_format OUTPUT_FORMAT] [--max_depth MAX_DEPTH]
                       [--no_interactive] [--equally_weighted] [--type {ancestors,descendants}]

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH, -i INPUT_PATH
                        Path to the family data (a file or a folder).
  --person_id PERSON_ID, -p PERSON_ID
                        ID of the person to center the sunburst on.
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Path to the output directory. Default to None, no file is saved.
  --output_filename OUTPUT_FILENAME, -fi OUTPUT_FILENAME
                        Name of the file. Default to 'suburst'.
  --output_format OUTPUT_FORMAT, -fo OUTPUT_FORMAT
                        Extension of the output file. Accepted format : 'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf',
                        'html'. Default to 'html'.
  --max_depth MAX_DEPTH, -d MAX_DEPTH
                        Maximum number of layer to renderer. Default to -1 to show the complete hiearchy.
  --no_interactive, -ni
                        Don't show the interactive sunburst window with Plotly.
  --equally_weighted, -ew
                        Weight all sectors at the same depth equally.
  --type {ancestors,descendants}, -t {ancestors,descendants}
                        Type of sunburst to draw: 'ancestors' or 'descendants'. Default to 'ancestors'.
```

You may have to install additionnal packages to save the sunburst as an image.