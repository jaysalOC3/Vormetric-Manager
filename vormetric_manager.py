#!/opt/Python-2.7.9/python
__author__ = 'jesse.salmon'
###
# Ensure that the correct python Version is installed.
import sys
pyVer = sys.version_info
if pyVer[0] == 2 and pyVer[1] == 7:
    print "Correct Python Version in Use."
else:
    print "Please install python 2.7 to use this script."
    exit(1)
###
import shutil, os

ROOT_FOLDER = '/pmdms_sec_test'
ENC_FOLDER = ROOT_FOLDER + '/enc'
###
# Check the root folder to encrypt
if os.path.exists(ENC_FOLDER):
    print "Found Folder: enc"
else:
    print "Could not find enc folder: Exit"
    exit(1)


###