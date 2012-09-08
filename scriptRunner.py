#!/usr/bin/python
# Scriptrunner will run all scripts within a folder that you specify.
# Useful for LaunchAgents and running multiple scripts at user login. 
# Thanks to Greg Neagle for an example of how to do this

# Todo: Add permissions checking so dubious scripts do not run
# Todo: Add check to make sure that scripts directory exists

import optparse 
import os
import subprocess
import plistlib
import datetime
import sys

def main():
    """Main"""

    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options]""")
    p.add_option('--once', '-o', dest='runOnce',
                    help="""Directory of scripts to run only once.""")
    p.add_option('--every', '-e', dest='runEvery',
                    help="""Directory of scripts to run every time.""")

    options, arguments = p.parse_args()

    # Check to see if passed options are a directory or not
    for parameter, value in options.__dict__.items():
        if value is not None:
            if not os.path.isdir(value): 
                sys.exit(value + "is not a directory")

    runEveryPath = options.runEvery
    runOncePath = options.runOnce
    runOncePlist = os.path.expanduser("~/Library/Preferences/") + "com.company.scriptrunner.plist"

    try:
        runOncePlistValues=plistlib.readPlist(runOncePlist)
    except IOError:
        print "File does not exist"
        runOncePlistValues = {}
    except:
        print "Something has gone terribly wrong."
        raise

    if runEveryPath is not None: 
        for file in os.listdir(runEveryPath):
            if os.access(os.path.join(runEveryPath, file), os.X_OK):
                subprocess.call(os.path.join(runEveryPath,file), stdin=None, stdout=None, stderr=None)
            else:
                print file + " is not executable"
                    
    # If runOnce is set, make sure script has not been run before and run it.
    if runOncePath is not None:
        for file in os.listdir(runOncePath):
            if file in runOncePlistValues:
                print os.path.join(runOncePath, file) + " already run!"
            else:
                if os.access(os.path.join(runOncePath, file), os.X_OK):
                    subprocess.call(os.path.join(runOncePath,file), stdin=None, stdout=None, stderr=None)
                    runOncePlistValues[file] = datetime.datetime.now().isoformat()
                else:
                    print file + " is not executable"

    plistlib.writePlist(runOncePlistValues, runOncePlist) 

if __name__ == '__main__':
    main()
