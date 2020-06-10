import os, sys
import logging

from lib.processor import Processor



"""
Entry point to the program
Usage: processor DIRECTORY

This "main" function will just init the logger and set the current working
directory the the DIRECTORY, so the directory where the user put his data,
config file and assets.

The sequence of traitments is handled by the Processor class
"""
if __name__ == '__main__' :
    logging.getLogger().setLevel(logging.INFO)
    base_directory = sys.argv[1];
    os.chdir(base_directory)
    if len(sys.argv) < 2 :
        logging.error("Usage : processor YOUR_DIRECTORY\nwith YOUT_DIRECTORY: the directory that contains the config file, your data file, your STATIC, etc.")
        sys.exit(1)
    Processor()
    
