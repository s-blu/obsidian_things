# TODO parse template and replace %var% placeholders with given values
# TODO randomize placeholder values in a given range
# TODO create 2-3 more template files

import logging
from pathlib import Path
import datetime
import re
import random

folderpath_root = "example_data"
# TODO concatinate with the file somnething package to not cause OS dependencies
folderpath_dailys = folderpath_root + "/dailys"
totalCountOfDailies = 123
templates = ['templates/template_daily_1.md','templates/template_daily_2.md']

# see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for syntax
daily_filename_syntax = "%G-%m-%d"

def createNewExampleFile(filename, templatefile):
    Path(folderpath_dailys).mkdir(parents=True, exist_ok=True)

    example = open(templatefile, encoding='utf-8')
    content = example.read()
    content = replacePlaceholders(content, filename)

    # TODO concatinate with the file somnething package to not cause OS dependencies
    f = open(folderpath_dailys + "/" + filename + ".md", 'w+')
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


for i in range(1, totalCountOfDailies):
    templateNo = random.randrange(0, len(templates))
    dailydate = datetime.datetime(2022, 1, 1) + datetime.timedelta(days=i)

    # TODO iterate through 3-4 different templates
    createNewExampleFile(dailydate.strftime(
        daily_filename_syntax), templates[templateNo])
