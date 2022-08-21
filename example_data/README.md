# Generate Example/Mock Data for Dataview

**⚠ ATTENTION! This script overwrites files in the given output path - never ever use in your real vault!**

This script helps you to generate example notes for testing purposes. 

## Usage

**ATTENTION** Running the script will **overwrite** already existing files with the same name in the output path! **⚠ Never use in your real vault! ⚠**

Edit the files under `templates/` to your liking. If you want more templates, create them and add them to the `templates` list in the script (or call the function with an appropiate argument). To insert some random test data, you can use following syntax inside your templates:

`%typeOfData;[min;max][;values]%`

ℹ Hint: The concrete syntax is dependent on your typeOfData. See below for more details.

To run the script, download this repository, navigate into `example-data` and run `GenerateExampleData.py` on your command line. This will create a folder `example-data` with `.md` files containing the template as well as randomized values for the placeholders. You can edit count and output path of the files at the top of the script or give them individually when calling the executing functions at the bottom. 
If you only want to generate `resources` or `dailys`, remove the appropiate function call at the bottom of the script. If you want to generate multiple `resources`, add function calls as needed and pass in the data (count, filenamesyntax, templates and paths) directly to the function.

## typeOfData for randomized values

Currently available are:

- **filename**: Outputs the filename, in case of the daily notes thats `YYYY-MM-DD`. Syntax: `%filename%`
- **number**: Outputs a number between min and max (inclusive). `min` defaults to 0, `min` to 5. Syntax: `%number;min;max%`
- **time**: Outputs a timestamp of format `HH:MM` between min and max (inclusive). `min` defaults to 08:00, `max` to 22:00. Syntax: `%time;min;max%`
- **date**: Outputs a date of format `YYYY-MM-DD` between min and max (inclusive). `min` defaults to 2022-02-02, `max` to 2022-12-12. Syntax: `%date;min;max%`
- **text**: Outputs one of the given values. Syntax: `%text;value1|value2|value3%` Values are seperated by a | and therefore cannot contain a | or a ;

### Examples

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

Outputs a date of format `YYYY-MM-DD` between (inclusive) the filename of the file (when in format `YYYY-MM-DD`, otherwise uses today's date) and 2022-12-12
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

## Available Functions

By calling one (or multiple) of the following functions at the end of the script you'll generate your data. Choose the function to call based on what you want to achieve.

### createExampleDailies

When you want to create files with dates as filenames.

Example call:

`createExampleDailies()`

#### Arguments

- `count`: (optional) total count of dailies you want to generate. Defaults to 35
- `filenameSyntax`: (optional) name syntax of your dailies. Need to be a date format string compatible to https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior. Defaults to `%G-%m-%d`

### createExampleResources

This is your function to generate arbitrary example data.

Example Calls:

`createExampleResources()`

`createExampleResources(5, 'projects_', ['templates/projects/1.md'], os.path.join(folderpath_root, "projects"))`

`createExampleResources(0, ['Ellen', 'Alice', 'Bob', 'Lu'], ['templates/persons/1.md', 'templates/persons/2.md'], os.path.join(folderpath_root, "people"))` _Hint: count will be ignored here and we'll generate 4 example files_

#### Arguments

- `count`: (optional) total count of recource files to generate. Defaults to 7
- `filenameSyntax`: (optional) filenames to use. You can either pass in a string, i.e. `books_`, which then get used as filename with a consecutive number as suffix (i.e. `books_1, books_2` etc) or a list of specific filenames (i.e. `["Paul", "Alice", "Bob"]`) which then get iterated. Defaults to `books_`. _Hint: When using a list of file names, count will be set to the length of the list_
- `templates`: (optional) List of template files to use. Defaults to `['templates/books/1.md', 'templates/books/2.md']`
- `path`: (optional) Path to write example data to. Defaults to `os.path.join(folderpath_root, "books")` (results in `example_data/books`)

### createExampleResourcesFromDataset

**Advanced usage, requires coding experience**.
If you want to fill in a template not with semi-randomized data but with a fixed set of data, that's possible when using `createExampleResourcesFromDataset`. Here, you need to give slightly different arguments:

#### Arguments

- `filenames`: List of filenames. In addition, these are the keys `dataFn` gets called with
- `templates`: List of template files to fill
- `path`: Path to write example data to
- `dataFn`: function to call to get back the set of fixed data to use. Will be called with `filename` as first argument and index as second argument. Needs to return a dict with data to use.

When using **createExampleResourcesFromDataset**, a new type of placeholder is available:

**data**

```
publisher:: %data;publisher%
```

This will replace the placeholder with the value of key `publisher` from the dict `dataFn` has returned.

#### Example

If you have a .json file with this content:

```
[
  {
    "name": "Stardew Valley",
    "developer": "ConcernedApe",
    "publisher": "ConcernedApe",
    "genre": "Indie, RPG, Simulation"
  },
  {
    "name": "New World",
    "developer": "Amazon Games",
    "publisher": "Amazon Games",
    "genre": "Action, Adventure, Massively Multiplayer, RPG"
  },
  {
    "name": "Team Fortress 2",
    "developer": "Valve",
    "publisher": "Valve",
    "genre": "Action, Free to Play" 
  }
]
```

and implement this function:

```
def findGameData(gameName):
    dataset = open("templates/data/games.json", encoding='utf-8')
    content = json.loads(dataset.read())
    data = None
    for game in content:
        if game["name"] == gameName:
            data = game
            break

    return data
```
calling 

```
createExampleResourcesFromDataset(
    ["Stardew Valley", "New World", "Team Fortress 2"],
    ['templates/games/1.md'],
    os.path.join(folderpath_root, "games"),
    findGameData)
```

You'll be able to use a template of this sort:

```
name: %filename%
publisher: %data;publisher%
developer: %data;developer%
genre: %data;genre%
---
#games

# %filename%

...
```

This allows you to generate data with a consistent, senseful data replacement. All other types of replacements are available for this function as well.
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
