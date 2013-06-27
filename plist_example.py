#!/usr/bin/python

# The Following bits were borrowed from Greg Neagle's FoundationPlist:
# https://code.google.com/p/munki/source/browse/code/client/munkilib/FoundationPlist.py

from Foundation import NSData, \
                       NSPropertyListSerialization, \
                       NSPropertyListMutableContainers, \
                       NSPropertyListXMLFormat_v1_0

class FoundationPlistException(Exception):
    pass

class NSPropertyListSerializationException(FoundationPlistException):
    pass

class NSPropertyListWriteException(FoundationPlistException):
    pass

def readPlist(filepath):
    """
    Read a .plist file from filepath.  Return the unpacked root object
    (which is usually a dictionary).
    """
    plistData = NSData.dataWithContentsOfFile_(filepath)
    dataObject, plistFormat, error = \
        NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                     plistData, NSPropertyListMutableContainers, None, None)
    if error:
        error = error.encode('ascii', 'ignore')
        errmsg = "%s in file %s" % (error, filepath)
        raise NSPropertyListSerializationException(errmsg)
    else:
        return dataObject

def writePlist(dataObject, filepath):
    '''
    Write 'rootObject' as a plist to filepath.
    '''
    plistData, error = \
     NSPropertyListSerialization.dataFromPropertyList_format_errorDescription_(
                            dataObject, NSPropertyListXMLFormat_v1_0, None)
    if error:
        error = error.encode('ascii', 'ignore')
        raise NSPropertyListSerializationException(error)
    else:
        if plistData.writeToFile_atomically_(filepath, True):
            return
        else:
            raise NSPropertyListWriteException(
                                "Failed to write plist data to %s" % filepath)

# Set the plist_path object to the path of the plist you wish to edit
plist_path="/Users/nate/Library/Preferences/com.apple.Safari.plist"

# Get the contents of the plist specified in plist_path and assign them to plist_contents
plist_contents = readPlist(plist_path)

# Print out the contents of the 'DomainsToNeverSetUp' key found in plist_contents
print plist_contents["DomainsToNeverSetUp"]