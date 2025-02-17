# What is this Repository?

This repository is for the following exercise:
- Create a Python script for monitoring a website from a functional description.

# Documentation

## Main.py

Main script, takes in the param.xml with all the variable data necessary for the execution of the exercise and proceeds to execute all 6 steps described in the exercise.

## Param.xml

XML file with the variable data info, as of the current version(v1.0), the only variable data used is the information regarding which browser is to be used for the execution of the main script.
- Write "Chrome" or "Edge" on the file depending on which browser you which to execute the script with.

## logfile.txt

The logfile will be created upon the execution of the main script. This logfile will include every output from the usual python console aswell as debug messages created using the logging library.
Useful for debugging and diagnostics in case of errors during the execution of the exercise.

## Screenshots folder

Necessary folder for the execution of the main script since the exercise steps require the usage of image recognition of specific parts of the webpage.

# Requirements and how to install

- Microsoft Edge browser or Google Chrome browser

- Python 3
  + https://www.python.org

- Selenium 4 (web service automation)
  + pip install selenium

- Lackey (image recognition)
  + pip install lackey

# How to execute the script

Have Microsoft Edge or Google Chrome configured and specify which one should be used in the params.xml file;

The following files should all be in the same folder:
- Main.py
- param.xml
- Screenshots folder with screenshot images inside
  
Once the files are setup as described, simply running the main.py script using command line or using an IDE with an python interpreter/venv configured will execute the exercise.

# Known bugs / Future improvements

## To be fixed
- On Step 5, the script clicks on location 4 of the map but the info box is not shown

## To be implemented
- Video recording of the script's execution, for both logging purposes and for help debugging in situations in which an error occurs.
