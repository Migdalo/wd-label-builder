# WDLabelBuilder
[![Build Status](https://travis-ci.org/Migdalo/wd-label-builder.svg?branch=master)](https://travis-ci.org/Migdalo/wd-label-builder)
[![Coverage Status](https://coveralls.io/repos/github/Migdalo/wd-label-builder/badge.svg?branch=master)](https://coveralls.io/github/Migdalo/wd-label-builder?branch=master)

Command-line tool for generating Wikidata labels, descriptions and aliases, and outputing them in QuickStatements compatible form. Written in Python 2.

## Usage
WDLabelBuilder takes a json file that contains Wikidata qnumbers and labels in one language, and creates labels on other language. User may choose to copy the labels from the input file as labels in another language. 

By default the results are saved to a file as QuickStatements compatible statements.

```
usage: wdlabelbuilder.py [-h] [-l | -a | -d] [-t] [-p PREFIX] [-s SUFFIX]
                         [-q QTITLE] [-n LTITLE] [-j | -u]
                         language filename

Create labels, descriptions and aliases for Wikidata items based on existing
labels for those items.

positional arguments:
  language              Language of the label/alias/description you are
                        adding. Use Wikimedia abbreviations (e.g. "en", "fr").
  filename              Input json filepath.

optional arguments:
  -h, --help            show this help message and exit
  -l, --label           Generate labels
  -a, --alias           Generate aliases
  -d, --description     Generate descriptions
  -t, --timeseries      Use numbers, such as years from labels in the input
                        json to create labels in another language.
  -p PREFIX, --prefix PREFIX
                        Prefix of the label/alias/description
  -s SUFFIX, --suffix SUFFIX
                        Suffix of the label/alias/description
  -q QTITLE, --qtitle QTITLE
                        Title of the qnumber field in the json file. Default
                        is "item".
  -n LTITLE, --ltitle LTITLE
                        Title of the label field in the json file. Default is
                        "itemLabel".
  -j, --json            Export results as a json instead of QuickStatements
                        commands.
  -u, --url             Export results as a QuickStatements 2 url.
```

### Basic usage
The most basic use case is when you want to copy the labels/aliases in the input file as labels/aliases in another language. This is useful for proper nouns.

Creating Finnish labels from labels in the input file.
> python wdlabelbuilder.py -l fi query.json

Creating Finnish aliases from aliases in the input file.
> python wdlabelbuilder.py -a fi query.json

### Time series
Sometimes Wikidata items form time series. For example: "2014 in literature" (Q2814662), "2015 in literature" (Q16024623), "2016 in literature" (Q19606180) etc. In these cases WDLabelBuilder can use the year from a label in the input file to construct a label in another language.

For example the following commands would use the year in literature examples above to create Finnish labels: "kirjallisuusvuosi 2014" (Q2814662), "kirjallisuusvuosi 2015" (Q16024623), "kirjallisuusvuosi 2016" (Q19606180) etc.
> python wdlabelbuilder.py -l -t -p kirjallisuusvuosi fi query.json

### Output
By default the output will be produced as a file named 'output' which contains strings that can be imported to QuickStatements. It's also possible to export the results as a json file or as QuickStatements 2 link. 

## License
WDLabelBuilder is licensed under [MIT license](./LICENSE).
