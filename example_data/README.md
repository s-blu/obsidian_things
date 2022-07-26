# Generate Example/Mock Data for Dataview

**⚠ ATTENTION! Super early state of the script, very basic. Better usability and more test data generation (placeholder types & iterating several templates) is in the works**

This script helps you to generate Daily like notes for testing purposes. 

## Usage

**ATTENTION** Running the script will **overwrite** already existing files with the same name in the output path! **Never use in your real vault - always backup!**


Edit `template_daily_1.md` to your liking. To generate some random test data, you can use following syntax:

`%typeOfData;[min;max][;values]%`

ℹ Hint: The concrete syntax is dependent on your typeOfData. See below for more details.

To run the script, download this repository, navigate into `example-data` and run `GenerateExampleData.py` on your command line. This will create a folder `example-data/dailys` containing 20  `.md` files containing the template as well as randomized values for the placeholders. You can edit count and output path of the files at the top of the script.

### typeOfData

Currently available are:

- **filename**: Outputs the filename, in case of the daily notes thats `YYYY-MM-DD`. Syntax: `%filename%`
- **number**: Outputs a number between min and max (inclusive). `min` defaults to 0, `min` to 5. Syntax: `%number;min;max%`
- **time**: Outputs a timestamp of format `HH:MM` between min and max (inclusive). `min` defaults to 08:00, `max` to 22:00. Syntax: `%time;min;max%`
- **date**: Outputs a date of format `YYYY-MM-DD` between min and max (inclusive). `min` defaults to 2022-02-02, `max` to 2022-12-12. Syntax: `%date;min;max%`
- **text**: Outputs one of the given values. Syntax: `%text;value1|value2|value3%` Values are seperated by a | and therefore cannot contain a | or a ;

## Examples

**number**

Outputs a value between (inclusive) 0 and 5
```
mood:: %number;;%
```

Outputs a value between (inclusive) 0 and 3
```
mood:: %number;;3%
```

Outputs a value between (inclusive) 2 and 7
```
steps:: %number;35;11183%
```

**time**

Outputs a time stamp of format `HH:MM` between (inclusive) 08:00 and 22:00
```
meditation:: %time;;%
```

Outputs a time stamp of format `HH:MM` between (inclusive) 15:00 and 22:00
```
dinner:: %time;15:00;%
```


Outputs a time stamp of format `HH:MM` between (inclusive) 06:00 and 08:23
```
wake-up:: %time;06:00;08:23%
```

**date**
Outputs a date of format `YYYY-MM-DD` between (inclusive) 2022-02-02 and 2022-12-12
```
appointment:: %date;;%
```

Outputs a date of format `YYYY-MM-DD` between (inclusive) the filename of the file (that needs to be in format `YYYY-MM-DD`) and 2022-12-12
```
appointment:: %date;filename;%
```

Outputs a date of format `YYYY-MM-DD` between (inclusive) 2022-01-01 and 2022-02-02
```
appointment:: %date;2022-01-01;2022-02-02%
```


**text**

Outputs either "yes" or "no"
```
raining:: %text;yes|no%
```

Outputs either x, o, z, t, rgb or l
```
character:: %text;x|o|z|t|rgb|l%
```

Outputs either "true" or an empty string (nothing)
```
raining:: %text;true|%
```
