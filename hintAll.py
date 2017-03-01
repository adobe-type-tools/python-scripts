#!/usr/bin/python

import os
import sys
import time
from subprocess import Popen, PIPE


__doc__ = """
hintAll v1.1 - Aug 04 2013

This script takes a path to a folder as input, finds all the Type 1 fonts
(.pfa files) or UFO fonts inside that folder and its subdirectories, and
hints them using the FDK's autohint tool. If a path is not provided, the
script will use the current path as the top-most directory.
The script ignores Multiple Master PFA fonts, usually named 'mmfont.pfa'.
The Type 1 fonts can also be in plain text format (.txt) where the Private
and CharStrings dictionaries are not encrypted. These files can be obtained
by using the FDK's detype1 tool.

==================================================
Versions:
v1.0 - Feb 22 2013 - Initial release
v1.1 - Aug 04 2013 - Added support for UFO files
"""

kFontTXT = "font.txt"
kTempPFA = "font_TEMP_.pfa"


def getFontPaths(path):
	fontsList = []
	for r, folders, files in os.walk(path):
		fileAndFolderList = folders[:]
		fileAndFolderList.extend(files)

		for item in fileAndFolderList:
			fileName, extension = os.path.splitext(item)
			extension = extension.lower()
			if extension == ".pfa" and not fileName == "mmfont":
				fontsList.append(os.path.join(r, item))
			elif extension == ".txt" and fileName == "font":
				fontsList.append(os.path.join(r, item))
			elif extension == ".ufo":
				fontsList.append(os.path.join(r, item))
			else:
				continue

	return fontsList


def doTask(fonts):
	totalFonts = len(fonts)
	print "%d fonts found\n" % totalFonts
	i = 1

	for font in fonts:
		folderPath, fontFileName = os.path.split(font)
		styleName = os.path.basename(folderPath)

		# Change current directory to the folder where the font is contained
		os.chdir(folderPath)

		# If it's a txt font, convert it to pfa temporarily
		fontIsTXT = False
		if fontFileName == kFontTXT:
			fontIsTXT = True
			fontFileName = kTempPFA
			cmd = 'type1 %s > %s' % (kFontTXT, kTempPFA)
			popen = Popen(cmd, shell=True, stdout=PIPE)
			popenout, popenerr = popen.communicate()
			if popenout:
				print popenout
			if popenerr:
				print popenerr

		print '*******************************'
		print 'Hinting %s...(%d/%d)' % (styleName, i, totalFonts)
		i += 1
		cmd = 'autohint -q "%s"' % fontFileName
		popen = Popen(cmd, shell=True, stdout=PIPE)
		popenout, popenerr = popen.communicate()
		if popenout:
			print popenout
		if popenerr:
			print popenerr

		# Revert font back to pfa, and delete temporary file
		if fontIsTXT:
			cmd = 'detype1 %s > %s' % (kTempPFA, kFontTXT)
			popen = Popen(cmd, shell=True, stdout=PIPE)
			popenout, popenerr = popen.communicate()
			if popenout:
				print popenout
			if popenerr:
				print popenerr

			if os.path.exists(kTempPFA):
				os.remove(kTempPFA)


def run():
	# if a path is provided
	if len(sys.argv[1:]):
		baseFolderPath = sys.argv[1]

		if baseFolderPath[-1] == '/':  # remove last slash if present
			baseFolderPath = baseFolderPath[:-1]

		# make sure the path is valid
		if not os.path.isdir(baseFolderPath):
			print 'Invalid directory.'
			return

	# if a path is not provided, use the current directory
	else:
		baseFolderPath = os.getcwd()

	t1 = time.time()
	fontsList = getFontPaths(baseFolderPath)

	if len(fontsList):
		doTask(fontsList)
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
