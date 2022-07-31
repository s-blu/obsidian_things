# Generate Example/Mock Data for Dataview

**⚠ ATTENTION! This script overwrites files in the given output path - never ever use in your real vault!**

This script helps you to generate Daily like notes for testing purposes. 

## Usage

**ATTENTION** Running the script will **overwrite** already existing files with the same name in the output path! **⚠ Never use in your real vault! ⚠**

Edit the files under `templates/` to your liking. If you want more templates, create them and add them to the `templates` list in the script. To generate some random test data, you can use following syntax:

`%typeOfData;[min;max][;values]%`

ℹ Hint: The concrete syntax is dependent on your typeOfData. See below for more details.

To run the script, download this repository, navigate into `example-data` and run `GenerateExampleData.py` on your command line. This will create a folder `example-data` with `.md` files containing the template as well as randomized values for the placeholders. You can edit count and output path of the files at the top of the script. 
If you only want to generate `resources` or `dailys`, remove the appropiate function call at the bottom of the script. If you want to generate multiple `resources`, add function calls as needed and pass in the data (count, filenamesyntax, templates and paths) directly to the function.

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

Outputs a value between (inclusive) 35 and 11183
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

Outputs either "true" or nothing (empty string)
```
raining:: %text;true|%
```

## Example template

A template could look like this:

```
---
day: %filename%
wellbeing:
  mood: %number;;%
  health: %number;3;%
  notes: %text;discomfort|relaxed|sad|happy|neutral|euphoric|heartbroken|happy|sad|neutral|neutral|neutral|%
---
#daily

# Daily Note %filename%

- [ ] Task 1 of %filename%
- [x] Completed Task of %filename%
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe)

#### Appointments
My next appointment with [person:: %text;Lisa|Paul|Christa|Fernando|Elias%] is on [appointment:: %date;filename;%].
Also I have an appointment at [appointment:: %date;filename;% %time;;%] with [person:: %text;Bob|Alice|Karl|Jonathan|Barbara%]

#### Metadata

wake-up:: %time;06:00;08:23%
praying:: %text;yes|%
go-to-sleep:: %time;21:45;23:55%

training:: %text;15m|1h 5m|23m|1h 27m|36m|%
situps:: %number;0;25%
steps:: %number;35;11183%
```

This would result in - for example - this output:

```
---
day: 2022-01-09
wellbeing:
  mood: 3
  health: 3
  notes: 
---
#daily

# Daily Note 2022-01-09

- [ ] Task 1 of 2022-01-09
- [x] Completed Task of 2022-01-09
- [x] Task with state (maybe)

#### Appointments
My next appointment with [person:: Christa] is on [appointment:: 2022-04-19].
Also I have an appointment at [appointment:: 2022-08-27 09:47] with [person:: Barbara]

#### Metadata

wake-up:: 06:29
praying:: yes
go-to-sleep:: 22:31

training:: 36m
situps:: 6
steps:: 7347
```
