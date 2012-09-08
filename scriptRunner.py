#!/usr/bin/python
# Scriptrunner will run all scripts within a folder that you specify.
# Useful for LaunchAgents and running multiple scripts at user login. 
# Thanks to Greg Neagle for an example of how to do this

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
 
    runOncePlist = os.path.expanduser("~/Library/Preferences/") + "com.company.scriptrunner.plist"

    try:
        runOncePlistValues=plistlib.readPlist(runOncePlist)
    except IOError:
        runOncePlistValues = {}

    for parameter, value in options.__dict__.items():
        if parameter == 'runEvery' and value is not None:
            for file in os.listdir(value):
                if os.access(os.path.join(value, file), os.X_OK) and (os.stat(os.path.join(value, file)).st_mode & 0777) == 0755:
                    subprocess.call(os.path.join(value ,file), stdin=None, stdout=None, stderr=None)
                else:
                    print file + " is not executable or has bad permissions"

        elif parameter == 'runOnce' and value is not None:

            for file in os.listdir(value):
                if file in runOncePlistValues:
                    print os.path.join(value, file) + " already run!"
                else:
                    if os.access(os.path.join(value, file), os.X_OK) and (os.stat(os.path.join(value, file)).st_mode & 0777) == 0755:
                        subprocess.call(os.path.join(value ,file), stdin=None, stdout=None, stderr=None)
                        runOncePlistValues[file] = datetime.datetime.now().isoformat()
                    else:
                        print file + " is not executable or has bad permissions"
            plistlib.writePlist(runOncePlistValues, runOncePlist)


     

if __name__ == '__main__':
    main()
