# Tree command

## Configuration file

The file can specified the following fields to customize the tree :
|Field|Type|Description|Default value|
|-----|-----|-----|-----|
|`background_color`     | `str`               | Color of the background of the image. See [Color Names of Graphviz](https://graphviz.org/doc/info/colors.html)   | `""`  |
|`filename`             | `str`               | Name of the generated file                                                                                       | `"family_tree.png"` |
|`person_label_config`  | `PersonLabelConfig` | TODO | / |
|`title_config`         | `TitleConfig`       | TODO | / |
|`trim_config`          | `TrimConfig`        | TODO | / |
|`start_person`         | `str`               | ID of the person from where to start generating the tree                                                        | `None` |

### Edge config
TODO

### Node config
TODO

### Person label config
Config to customize how the text of a person is rendered (the label of a node). In the field `person_label_config` :

|Field|Type|Description|Default value|
|-----|-----|-----|-----|
|`bold_names`         | `bool`  | Bold the first and last names                         | `True`  |
|`show_nationalities` | `bool`  | Show the nationalities as flag                        | `True`  |
|`show_nickname`      | `bool`  | Show the nickname (in quotes)                         | `True`  |
|`show_middle_names`  | `bool`  | Show the list of middle names                         | `True`  |
|`show_years`         | `bool`  | Show the birth and death years                        | `True`  |
|`split_names`        | `bool`  | Add a return to line between the first and last names | `False` |
|`upper_last_name`    | `bool`  | Put the last name in uppercase                        | `False` |

### Title config
Config to customize how the title of tree is rendered. In the field `title_config` :

|Field|Type|Description|Default value|
|-----|-----|-----|-----|
|`enabled`  | `bool`   | Show the title of the tree                                                                                   | `True`  |
|`location` | `str`    | Location of the title in the image. See [`labelloc` of Graphviz](https://graphviz.org/docs/attrs/labelloc/)  | `"t"`   |
| `title`   | `str`    | Text of the title. Will use the title property of a Family object if no title is given                       | `None`  |

### Trim config
Config to select the persons to show in tree. In the field `trim_config` :

|Field|Type|Description|Default value|
|-----|-----|-----|-----|
|`ancestors_of`               | `AncestorsOfConfig`       | TODO  | `None`  |
|`descendants_of`               | `DescendantsOfConfig`       | TODO  | `None`  |
|`ignore`                       | `list[str]` | List of id of persons to ignore in the family tree                     | `[]`    |
|`ignore_incomplete_relations`  | `bool`      | Ignore the relations with a person who doesn't exist in tree           | `False` |
