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

###
# Check the root folder to encrypt

###