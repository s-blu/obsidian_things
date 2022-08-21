from gettext import find
import logging
from pathlib import Path
import datetime
import re
import random
import os
import json

folderpath_root = "example_data"

# resources
folderpath_resources = os.path.join(folderpath_root, "books")
totalCountOfResources = 7
resource_templates = ['templates/books/1.md', 'templates/books/2.md', ]
resource_filename_syntax = "books_"


# dailies
folderpath_dailys = os.path.join(folderpath_root, "dailys")
totalCountOfDailies = 35
daily_templates = ['templates/dailys/template_daily_1.md',
                   'templates/dailys/template_daily_2.md', 'templates/dailys/template_daily_3.md']
# see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for syntax
daily_filename_syntax = "%G-%m-%d"


def createNewExampleFile(filename, templatefile, folderpath, data=None):
    Path(folderpath).mkdir(parents=True, exist_ok=True)

    example = open(templatefile, encoding='utf-8')
    content = example.read()
    content = replacePlaceholders(content, filename, data)

    f = open(os.path.join(folderpath, filename + ".md"), 'w+')
    f.write(content)
    f.close()


def replacePlaceholders(filecontent, filename, data):
    placeholderRegex = r'(%.[^%]+%)'
    placeholders = re.findall(placeholderRegex, filecontent)

    datefilename = filename
    try:
        datetime.datetime.fromisoformat(datefilename)
    except ValueError:
        datefilename = datetime.datetime.now().strftime(daily_filename_syntax)

    for i, plh in enumerate(placeholders):
        replacement = ""
        plh = plh.replace("%", "").split(";")
        plhtype = plh[0]
        if (plhtype == "filename"):
            replacement = filename
        elif (plhtype == "text"):
            # TODO paste warning if values cannot be found
            values = plh[1].split("|")
            pick = random.randrange(0, len(values), 1)
            replacement = values[pick]
        elif (plhtype == "data"):
            try:
                replacement = data[plh[1]]
            except:
                logging.warning(
                    f'Could not replace data placeholder "{plh[1]}" with dataset {data}')
        else:
            if (len(plh) != 3):
                logging.warning(
                    f' Could not split up placeholder "{plh}" into type, min, max. Make sure it has the syntax "type;min;max" even if one of these is empty!')
            plhmin = plh[1]
            plhmax = plh[2]
            if (plhtype == 'number'):
                replacement = random.randrange(
                    int(plhmin) if plhmin else 0, int(plhmax) if plhmax else 5, 1)
            elif (plhtype == 'time'):
                plhmin = convertTimeToTimestamp(
                    plhmin if plhmin else "08:00")
                plhmax = convertTimeToTimestamp(
                    plhmax if plhmax else "22:00")

                replacement = datetime.datetime.fromtimestamp(
                    random.randrange(round(plhmin), round(plhmax))).strftime("%H:%M")
            elif (plhtype == 'date'):
                plhmin = datefilename if plhmin == "filename" else plhmin
                plhmax = datefilename if plhmax == "filename" else plhmax
                plhmin = datetime.datetime.fromisoformat(
                    plhmin if plhmin else "2022-02-02").timestamp()
                plhmax = datetime.datetime.fromisoformat(
                    plhmax if plhmax else "2022-12-12").timestamp()

                replacement = datetime.datetime.fromtimestamp(
                    random.randrange(round(plhmin), round(plhmax))).strftime("%G-%m-%d")
        filecontent = re.sub(placeholderRegex, str(
            replacement), filecontent, 1)

    return filecontent


def convertTimeToTimestamp(timestr):
    timestr = timestr.split(":")
    dttime = datetime.datetime.now()
    dttime = dttime.replace(hour=int(timestr[0]), minute=int(timestr[1]))
    return dttime.timestamp()


def createExampleDailies(count=totalCountOfDailies, filennameSyntax=daily_filename_syntax):
    for i in range(1, count):
        templateNo = random.randrange(0, len(daily_templates))
        # starting on the third to get full weeks
        dailydate = datetime.datetime(2022, 1, 3) + datetime.timedelta(days=i)

        createNewExampleFile(dailydate.strftime(
            filennameSyntax), daily_templates[templateNo], folderpath_dailys)


def createExampleResources(count=totalCountOfResources, filennameSyntax=resource_filename_syntax, templates=resource_templates, path=folderpath_resources):
    if isinstance(filennameSyntax, list):
        count = len(filennameSyntax)

    for i in range(1, count):
        templateNo = random.randrange(0, len(templates))
        if isinstance(filennameSyntax, list):
            filename = filennameSyntax[i]
        else:
            filename = filennameSyntax + str(i)

        createNewExampleFile(filename, templates[templateNo], path)


def createExampleResourcesFromDataset(filenames, templates, path, dataFn):
    for i in range(0, len(filenames)):
        templateNo = random.randrange(0, len(templates))
        data = dataFn(filenames[i], i)

        createNewExampleFile(filenames[i], templates[templateNo], path, data)



# === CALLS OF DATA GENERATING FUNCTIONS BELOW ==
# ￬￬￬ Adjust this to your needs ￬￬￬

createExampleDailies(7)
createExampleResources()

def findGameData(gameName, index):
    dataset = open("templates/data/games.json", encoding='utf-8')
    content = json.loads(dataset.read())
    data = None
    for game in content:
        if game["name"] == gameName:
            data = game
            break

    return data

createExampleResourcesFromDataset(
    ["Stardew Valley", "New World", "Team Fortress 2"],
    ['templates/games/1.md'],
    os.path.join(folderpath_root, "games"),
    findGameData)
