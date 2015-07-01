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
import os
import shutil
import subprocess

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
    if os.path.islink(fLoc):
        print "%s is a link and may already be encrypted." % fLoc
        return False
    if os.path.isdir(os.path.join(fLoc, "enc1.stat")):
        print "%s is being copied to enc folder." % fLoc
        return False
    if os.path.isdir(os.path.join(fLoc, "enc2.stat")):
        print "Renaming: %s to %s.bk" % (fLoc,fLoc)
        return False
    if os.path.isdir(os.path.join(fLoc, "enc3.stat")):
        print "Creating a Link for %s" % (fLoc)
        return False
    print "Working on %s" % fLoc
    with open(os.path.join(fLoc, "enc1.stat"), 'w') as file:
        file.write("1")
    rsyncSrc = fLoc
    rsyncDst = ENC_FOLDER + "/" + fLoc.split("/")[2]
    print "RSync: %s %s" % (rsyncSrc, rsyncDst)
    proc = subprocess.call(['rsync','-a',rsyncSrc,rsyncDst])
###
###
# Find next folder to work on
for item in os.listdir(ROOT_FOLDER):
    if os.path.isdir(os.path.join(ROOT_FOLDER, item)):
        if not 'enc' in item:
            folder = os.path.join(ROOT_FOLDER, item)
            print folder
            if processFolder(folder) == True:
                print "Completed."
            else:
                print "Skipping due to work already in progress"
        else:
            print "Skipping %s" % item

###