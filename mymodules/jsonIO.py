#!/usr/bin/python

import logging
import sys
import json

logger = logging.getLogger(__name__)

def writeJson(dictToWrite=None, filename=None):
    if dictToWrite and filename:
        logger.info("\nDumping to jsonfile %s ..." %(str(filename)))

    # If the file name exists, write a JSON string into the file.
    if filename:
        try:
            f = open(filename, 'w') 
        except IOError:
            logger.error('Can\'t write to file %s' %(str(filename)))
            sys.exit(0)
        json.dump(dictToWrite, f)
        logger.info("Dumped %d entries to jsonfile %s" %(len(dictToWrite),filename))

def readJson(filename=None):
    if filename:
        logger.info("\nImporting from jsonfile %s ..." %(str(filename)))
        try:
            f = open(filename, 'r')
        except IOError:
            logger.error('Can\'t read from file %s' %(str(filename)))
            sys.exit(0)
        datastore = json.load(f)
        logger.info("Imported %d entries from jsonfile %s" %(len(datastore),filename))
        return datastore
    else:
        logger.error("Error: Filename to import is missing")
        return None

