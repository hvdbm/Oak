# Oak

Tree generated with [Graphviz](https://graphviz.org).

## Command

The code can be called with :
```
python oak.py [-h] --input_file_path INPUT_FILE_PATH [--config_file_path CONFIG_FILE_PATH] [--output_dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  --input_file_path INPUT_FILE_PATH
                        Path to the JSON file containing the family data
  --config_file_path CONFIG_FILE_PATH
                        Path to the JSON file containing configuration of the family tree
  --output_dir OUTPUT_DIR
                        Path to the output directory
```


## Configuration file

A configuration `JSON` file can be used to customize the tree. The file is optionnal and by default the following values will be used :

```json
{
  "filename": "family_tree.png",
  "graph_title": "",
  "node_shape": "box",
  "show_nickname": false
}
```

| Parameter   | Definition | Default |
| -----       | -----      | -----  |
| filename    | Name of the image containing the tree   | Current dir |
| graph_title | The label of the graph                  | ""          |
| node_shape  | Shape of the persons nodes              | box         |
| show_nickname | Show a nickname in the label of a person | false    |
