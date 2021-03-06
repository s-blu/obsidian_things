import logging
from pathlib import Path
import datetime
import re
import random
import os

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


def createNewExampleFile(filename, templatefile, folderpath):
    Path(folderpath).mkdir(parents=True, exist_ok=True)

    example = open(templatefile, encoding='utf-8')
    content = example.read()
    content = replacePlaceholders(content, filename)

    f = open(os.path.join(folderpath, filename + ".md"), 'w+')
    f.write(content)
    f.close()


def replacePlaceholders(filecontent, filename):
    placeholderRegex = r'(%.[^%]+%)'
    placeholders = re.findall(placeholderRegex, filecontent)

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
                plhmin = filename if plhmin == "filename" else plhmin
                plhmax = filename if plhmax == "filename" else plhmax
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
    for i in range(1, count):
        templateNo = random.randrange(0, len(templates))
        createNewExampleFile(filennameSyntax + str(i),
                             templates[templateNo], path)


createExampleDailies()
createExampleResources()
