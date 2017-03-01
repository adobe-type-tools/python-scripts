#!/usr/bin/python

import os
import sys
import time

############################################
# THE VALUES BELOW CAN BE EDITED AS NEEDED #
############################################

minKern = 3
# This value is inclusive; this means that pairs which EQUAL this ABSOLUTE
# value will NOT be ignored/trimmed. Anything kerning pair that falls below
# will be ignored.
writeTrimmed = False
# If 'False', trimmed pairs will not be processed and therefore will not be
# written to the kerning feature file.
# If 'True', trimmed pairs will be written, but commented out.
writeSubtables = False
# Sometimes the kerning feature file needs to have explicit subtable breaks,
# otherwise the OTF won't compile due to a subtable overflow.


############################################

__copyright__ = __license__ = """
Copyright (c) 2014 Adobe Systems Incorporated. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE."""

__doc__ = """ This script takes a path to a folder as input, finds all
the UFOs inside that folder and its subdirectories, and outputs each
font's kerning in feature file syntax. If a path is not provided, the
script uses the current path as the top-most directory. The name of
the resulting kerning FEA file is managed by the WriteFeaturesKernFDK
module. """

# ----------------------------------------------

libraryNotFound = False

try:
	from defcon import Font
except:
	print "ERROR: This script requires defcon. It can be downloaded from https://github.com/typesupply/defcon"
	libraryNotFound = True
try:
	import WriteFeaturesKernFDK
except:
	print "ERROR: This script requires WriteFeaturesKernFDK.py. It can be downloaded from https://github.com/adobe-type-tools/python-modules"
	libraryNotFound = True

if libraryNotFound:
	sys.exit()

fontsList = []


def getFontPaths(path, startpath):
	files = os.listdir(path)
	for file in files:
		if file[-4:].lower() in [".ufo"]:
			fontsList.append(os.path.join(path, file))
		else:
			if os.path.isdir(os.path.join(path, file)):
				getFontPaths(os.path.join(path, file), startpath)


def doTask(fonts, startpath):
	totalFonts = len(fonts)
	print "%d fonts found\n" % totalFonts
	i = 0

	for font in fonts:
		i += 1
		folderPath, fontFileName = os.path.split(font)
		# path to the folder where the font is contained and the font's file name
		styleName = os.path.basename(folderPath)
		folderPath = os.path.abspath(folderPath)
		# name of the folder where the font is contained

		# Change current directory to the folder where the font is contained
		os.chdir(folderPath)

		exportMessage = 'Exporting kern files for %s...(%d/%d)' % (
			styleName, i, totalFonts)
		print '*' * len(exportMessage)
		print exportMessage

		ufoFont = Font(fontFileName)
		WriteFeaturesKernFDK.KernDataClass(
			ufoFont, folderPath, minKern,
			writeTrimmed, writeSubtables
		)

		os.chdir(startpath)


def run():
	# if a path is provided
	if len(sys.argv[1:]):
		baseFolderPath = os.path.normpath(sys.argv[1])

		# make sure the path is valid
		if not os.path.isdir(baseFolderPath):
			print 'Invalid directory.'
			return

	# if a path is not provided, use the current directory
	else:
		baseFolderPath = os.getcwd()

	t1 = time.time()
	getFontPaths(baseFolderPath, baseFolderPath)
	startpath = os.path.abspath(os.path.curdir)
	if len(fontsList):
		doTask(fontsList, startpath)
	else:
		print "No fonts found"
		return

	t2 = time.time()
	elapsedSeconds = t2-t1

	if (elapsedSeconds/60) < 1:
		print 'Completed in %.1f seconds.' % elapsedSeconds
	else:
		print 'Completed in %.1f minutes.' % (elapsedSeconds/60)


if __name__=='__main__':
	run()
