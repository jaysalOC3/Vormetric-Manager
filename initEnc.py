## Vormetric Inital Encryption
## Sync to Server: scp Documents/File\ Encryption/scripts/initEnc.py jesse.salmon@devintx-dom05.kareo.ent:/home/jesse.salmon/initEnc.py
import os, time
from time import gmtime, strftime

# Setup Logging Facility
import logging
LOG_FILENAME = 'VormetricScript.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

import shutil
import subprocess
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
MAILFROM = 'DMSEncryption@kareo.com'
MAILTO = ['jesse.salmon@kareo.com']

fake = False

FILEFOLDERLIST = r'/home/jesse.salmon/FILELIST.txt'
FOLDERLIST = []
HOST = 'devintx-dom05.kareo.ent'

def status(message):
    message = message + "\n"
    message = message + "Time: %s" % strftime("%Y-%m-%d %H:%M:%S", gmtime())
    message = message + "\n"
    message = message + "This is a Test. Please disreguard."
    msg = MIMEText(message)
    msg['Subject'] = 'POC Encryption Status: %s' % HOST
    msg['From'] = MAILFROM
    msg['To'] = 'jesse.salmon@kareo.com'
    s = smtplib.SMTP('relay.kareo.com')
    s.sendmail(MAILFROM, MAILTO, msg.as_string())
    s.quit()
    
def getFolders(FF):
    FILENAME = FF
    with open(FILENAME) as tFile:
        for line in tFile.readlines():
            line = line.strip()
            if os.path.exists(line):
                print "Adding %s to list" % line
                FOLDERLIST.append(line)

def createEFolder(FOLDER):
    newFolder = FOLDER + '.enc'
    if not os.path.exists(newFolder):
        print "Making %s" % newFolder
        os.mkdir(newFolder)
    else:
        print "%s already exists" % FOLDER

def isGP(FOLDER,HOST):
    HOST = HOST
    proc = subprocess.Popen(['./vmssc','host','show',HOST],stdout=subprocess.PIPE)
    print "Checking for configured GP: %s" % FOLDER
    while True:
        line = proc.stdout.readline()
        if line != '':
            #print "GP Check:", line.rstrip()
            if FOLDER in line:
                print "WARNING: %s is already a Guard Point!" % FOLDER
                return True
        else: break
    return False
        
def createGP(FOLDER,POLICY,HOST):
'''
Function: Create GuardPoint for pretected folder.
'''
    FOLDER = FOLDER
    POLICY = POLICY
    HOST = HOST
    print "Creating Guard Point: %s" % FOLDER
    #	./vmssc host addgp -d <FOLDER> -p <POLICY> -e -t dir <HOST>
    subprocess.Popen(['./vmssc', 'host', 'addgp', '-d', FOLDER, '-p', POLICY,
                     '-e', '-t', 'dir', HOST])
def removeGP(FOLDER,POLICY,HOST):
'''
Function: Remove GuardPoint for pretected folder.
'''
    FOLDER = FOLDER
    POLICY = POLICY
    HOST = HOST
    print "Removing Guard Point: %s" % FOLDER
    #	./vmssc host delgp -d <FOLDER> -p <POLICY> -e -t dir <HOST>
    subprocess.Popen(['./vmssc', 'host', 'delgp', '-d', FOLDER, '-p', POLICY,
                     '-e', '-t', 'dir', HOST])

def cpData(FOLDER):
'''
Function: Use rsync to move files into protected folder.
'''
    while True:
        print "Checking on GP health..."
        if isGP(FOLDER+'.enc',HOST):
            break
        time.sleep(5)
    print "Moving Data - Source: %s Destination: %s" % (FOLDER,FOLDER+'.enc')
    tmessage = "Moving Data - Source: %s Destination: %s" % (FOLDER,FOLDER+'.enc')
    status(tmessage)
    if fake:
        time.sleep(5)
    else:
        proc = subprocess.call(['rsync','-a',FOLDER+r'/',FOLDER+r'.enc/'])
    print "Completed: %s" % FOLDER

def rename(FOLDER):
    while True:
        print "Renaming %s to %s" % (FOLDER,FOLDER+'.bk')
        try:
            shutil.move(FOLDER,FOLDER+'.bk')
            break
        except:
            time.sleep(10)
    while True:
        print "Renaming %s to %s" % (FOLDER+'.enc',FOLDER)
        try:
            shutil.move(FOLDER+'.enc',FOLDER)
            break
        except:
            time.sleep(10)

def cleanup(FOLDER):
    print "Just incase I'll cleanup any junk on %s" % FOLDER
    if isGP(FOLDER+'.enc',HOST):
        print "Removing Guard Point for temp folder: %s" % FOLDER
        removeGP(FOLDER+'.enc','Operational_POC_Policy', HOST)
    if os.path.exists(FOLDER+'.enc'):
        while True:
            try:
                shutil.rmtree(FOLDER+'.enc')
                break
            except:
                print "Waiting for Vormetric to receive the update..."
                time.sleep(5)
    if isGP(FOLDER,HOST):
        print "Removing Guard Point for folder: %s" % FOLDER
        removeGP(FOLDER,'Operational_POC_Policy', HOST)
    if os.path.exists(FOLDER+'.bk'):
        print "Restoring Backup folder: %s" % FOLDER
        shutil.rmtree(FOLDER)
        shutil.move(FOLDER+'.bk',FOLDER)
        
if __name__ == "__main__":
	getFolders(FILEFOLDERLIST)
	print "Starting..."
	for item in FOLDERLIST:
		cleanup(item)
		createEFolder(item)
		if not isGP(item+'.enc',HOST):
			createGP(item+'.enc','Operational_POC_Policy', HOST)
		cpData(item)
		removeGP(item+'.enc','Operational_POC_Policy', HOST)
		rename(item)
		if not isGP(item,HOST):
			createGP(item,'Operational_POC_Policy', HOST)
		status("Completed Encryption of: %s" % item)