# API Data fetching

## Prerequisites

* python installed

For scraping IDs from VVZ (only on linux, but can be adapted in the VVZ_bot.py file for other configurations):
* chrome installed 
* chrome webdriver for the same version of chrome installed (in /usr/bin/) (https://sites.google.com/a/chromium.org/chromedriver/downloads)

## How to use

* clone or download files
* open console in installation folder
* run ``` python VVZ_bot.py ``` to scrape the module IDs of the economics faculty from Vorlesungsverzeichnis
* run ``` python rating_grade_correlation.py ``` to scrape data for hypothesis 1
* run ``` python average_rating_and_grade_per_semester.py ``` to scrape data for hypothesis 2

## What it does

* VVZ_bot.py script creates module IDs list for the following scripts
* script reads all module ids from the input file (by default 'module_list.txt')
* fetches data of all modules
* writes output file (by default 'output.CSV') with all selected field
