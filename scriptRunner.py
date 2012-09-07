#!/usr/bin/python
# Scriptrunner will run all scripts within a folder that you specify.
# Useful for LaunchAgents and running multiple scripts at user login. 

import optparse 
import os
import subprocess
import plistlib
import datetime

def main():
    """Main"""

    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options]""")
    p.add_option('--once', '-o', dest='runOnce',
                    help="""Directory of scripts to run only once.""")
    p.add_option('--every', '-e', dest='runEvery',
                    help="""Directory of scripts to run every time.""")

    options, arguments = p.parse_args()
    runEveryPath = options.runEvery
    runOncePath = options.runOnce
    runOncePlist = os.path.expanduser("~/Library/Preferences/") + "com.company.scriptrunner.plist"

    try:
        runOncePlistValues=plistlib.readPlist(runOncePlist)
    except IOError:
        print "File does not exist"
        runOncePlistValues = {}

    if runEveryPath is not None: 
        for root, dirs, files in os.walk(runEveryPath):
            for file in files:
                subprocess.call(os.path.join(root,file), stdin=None, stdout=None, stderr=None)
                    
    # If runOnce is set, make sure script has not been run before and run it.
    if runOncePath is not None:
        for root, dirs, files in os.walk(runOncePath):
            for file in files:
                if file in runOncePlistValues:
                    print os.path.join(root, file) + " already run!"
                else:
                    subprocess.call(os.path.join(root,file), stdin=None, stdout=None, stderr=None)
                    runOncePlistValues[file] = datetime.datetime.now().isoformat()

    plistlib.writePlist(runOncePlistValues, runOncePlist) 

if __name__ == '__main__':
    main()
