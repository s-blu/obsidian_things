import logging
from pathlib import Path
import datetime

folderpath_root = "example_data"
# TODO concatinate with the file somnething package to not cause OS dependencies
folderpath_dailys = folderpath_root + "/dailys" 

# see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for syntax
daily_filename_syntax = "%G-%m-%d"

class ExampleDataGenerator():
    def createNewExampleDaily(filename, templatefile):
        Path(folderpath_dailys).mkdir(parents=True, exist_ok=True)

        example = open(templatefile, encoding='utf-8')
        content = example.read()

        # TODO concatinate with the file somnething package to not cause OS dependencies
        f = open(folderpath_dailys + "/" + filename, 'w+')  # open file in append mode
        f.write(content)
        f.close()

for i in range(1, 10):
    # TODO start at first of january and be able to just add like 55 days and get a decent date out of this
    x = datetime.datetime(2018, 6, i)
    # TODO iterate through 3-4 different templates
    ExampleDataGenerator.createNewExampleDaily(x.strftime(daily_filename_syntax) + ".md", 'template_daily_1.md')
