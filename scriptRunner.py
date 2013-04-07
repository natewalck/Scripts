#!/usr/bin/python
# scriptRunner will run all scripts within a folder that you specify.
# Useful for LaunchAgents and running multiple scripts at user login.
# Thanks to Greg Neagle for an example of how to do this

import optparse
import os
import subprocess
import plistlib
import datetime
import sys
import stat


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
    for path in (options.runOnce, options.runEvery):
        if path is not None:
            if not os.path.isdir(path):
                sys.exit(path + " is not a directory")

    runOncePlist = os.path.expanduser("~/Library/Preferences/") + "com.company.scriptrunner.plist"

    try:
        runOncePlistValues = plistlib.readPlist(runOncePlist)
    except IOError:
        runOncePlistValues = {}

    if options.runEvery:
        for script in os.listdir(options.runEvery):
            st = os.stat(os.path.join(options.runEvery, script))
            mode = st.st_mode
            if not mode & stat.S_IWOTH:
                try:
                    subprocess.call(os.path.join(options.runEvery, script), stdin=None)
                except OSError:
                    print "Something went wrong!"
            else:
                print script + " is not executable or has bad permissions"

    if options.runOnce:
        for script in os.listdir(options.runOnce):
            if script in runOncePlistValues:
                print os.path.join(options.runOnce, script) + " already run!"
            else:
                st = os.stat(os.path.join(options.runOnce, script))
                mode = st.st_mode
                if not mode & stat.S_IWOTH:
                    try:
                        subprocess.call(os.path.join(options.runOnce, script), stdin=None)
                        runOncePlistValues[script] = datetime.datetime.now()
                    except OSError:
                        print "Uh oh"
                else:
                    print script + " is not executable or has bad permissions"
        plistlib.writePlist(runOncePlistValues, runOncePlist)


if __name__ == '__main__':
    main()
