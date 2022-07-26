# Generate Example/Mock Data for Dataview

**⚠ ATTENTION! Super early state of the script, very basic. Better usability and more test data generation (placeholder types & iterating several templates) is in the works**

This script helps you to generate Daily like notes for testing purposes. 

## Usage

**ATTENTION** Running the script will **overwrite** already existing files with the same name in the output path! **Never use in your real vault - always backup!**


Edit `template_daily_1.md` to your liking. To generate some random test data, you can use following syntax:

`%typeOfData;min;max;values%`

⚠ ATTENTION! You currently need to keep this format. A placeholder needs to consists of three `;`. You can leave properties empty; see examples below.

ATTENTION! "values" is not implemented yet.

See the documentation below for more details.

To run the script, download this repository, navigate into `example-data` and run `GenerateExampleData.py` on your command line. This will create a folder `example-data/dailys` containing 20  `.md` files containing the template as well as randomized values for the placeholders. You can edit count and output path of the files at the top of the script.

### typeOfData

Currently available are:

- **number**: Outputs a number between min and max (inclusive). `min` defaults to 0, `min` to 5
- **time**: Outputs a timestamp of format `HH:MM` between min and max (inclusive). `min` defaults to 08:00, `max` to 22:00
- **date**: to be implemented
- **boolean**: to be implemented

### min and max
Specifies optional minimal and maximum values for the type of data. See `typeOfData`

### values

**To be implemented**. Lets you specify a set of possible values of the field from which one will be randomly chosen. Setting values means `min/max` will be ignored.

## Examples

**number**

Outputs a value between (inclusive) 0 and 5
```
mood:: %number;;;%
```

Outputs a value between (inclusive) 0 and 3
```
mood:: %number;;3;%
```

Outputs a value between (inclusive) 2 and 7
```
steps:: %number;35;11183;%
```

**time**

Outputs a time stamp of format `HH:MM` between (inclusive) 08:00 and 22:00
```
meditation:: %time;;;%
```

Outputs a time stamp of format `HH:MM` between (inclusive) 15:00 and 22:00
```
dinner:: %time;15:00;;%
```


Outputs a time stamp of format `HH:MM` between (inclusive) 06:00 and 08:23
```
wake-up:: %time;06:00;08:23;%
```