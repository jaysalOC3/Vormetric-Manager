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

###
# Process Folder if not already worked on.
def processFolder(fLoc):
    print (os.path.join(fLoc, "enc1.stat"))
###
###
# Find next folder to work on
for item in os.listdir(ROOT_FOLDER):
    if os.path.isdir(os.path.join(ROOT_FOLDER, item)):
        if not 'enc' in item:
            folder = os.path.join(ROOT_FOLDER, item)
            print folder
            processFolder(folder)
        else:
            print "Skipping %s" % item

###