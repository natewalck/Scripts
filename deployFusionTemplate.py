#!/usr/bin/python

import optparse
import os
import shutil
import string
import re

p = optparse.OptionParser()
p.set_usage("""Usage: %prog [options]""")
p.add_option('--template', '-t', dest='template',
             help="""Path to template you wish to deploy.""")
p.add_option('--output', '-o', dest='output',
             help="""Path and name you would like to deploy the template to.""")

options, arguments = p.parse_args()

if not options.template:
    p.error('You must supply a VM to use as a template')

if not options.output:
    p.error('You must supply an output location and name')


templateName = os.path.splitext(os.path.basename(options.template))[0]

if options.output.endswith('.vmwarevm'):
    outputName = os.path.basename(options.output)
else:
    outputName = os.path.basename(options.output + '.vmwarevm')

outputPath = os.path.dirname(options.output)

print outputName
print outputPath

print "Copying %s to %s" % (options.template, os.path.join(outputPath, outputName))

shutil.copytree(options.template, os.path.join(outputPath, outputName))

for file in os.listdir(os.path.join(outputPath, outputName)):
    file = os.path.join(outputPath, outputName, file)
    if templateName in file:
        fileHandler = open(file, 'r')
        fileContents = fileHandler.read()
        fileHandler.close()
        modifiedFileContents = re.sub(templateName, os.path.splitext(outputName)[0], fileContents)
        fileHandler = open(file, 'w')
        fileHandler.write(modifiedFileContents)
        fileHandler.close()

        os.rename(file, string.replace(file, templateName, os.path.splitext(outputName)[0]))

print "Template Deployed to %s" % os.path.join(outputPath, outputName)
