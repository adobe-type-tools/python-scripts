#!/usr/bin/python

###################################################
### THE VALUES BELOW CAN BE EDITED AS NEEDED ######
###################################################

writeClassesFile = True     # TRUE: Writes mark classes to external file. FALSE: Writes mark classes as part of mark.fea file.
genMkmkFeature = True       # TRUE: Writes mkmk.fea file. FALSE: Ignores mark-to-mark placement.
indianScriptsFormat = True  # TRUE: Writes abvm.fea and blwm.fea files. FALSE: Writes simple mark.fea file.
trimCasingTags = True       # TRUE: Trims casing tags so that all marks can be applied to UC/LC. FALSE: Leaves casing tags as is.

# ----------------------------------------------

libraryNotFound = False

import os, sys, re, copy, math, time
try:
	from defcon import Font
except:
	print "ERROR: This script requires defcon. It can be downloaded from https://github.com/typesupply/defcon"
	libraryNotFound = True
try:
	import WriteFeaturesMarkFDK
except:
	print "ERROR: This script requires WriteFeaturesMarkFDK.py. It can be downloaded from https://github.com/adobe-type-tools/python-modules"
	libraryNotFound = True

if libraryNotFound:
	sys.exit()


def generateMarkFiles(font):

	folderPath, fontFileName = os.path.split(font)  
	# path to the folder where the font is contained and the font's file name
	os.chdir(folderPath)

	ufoFont = Font(fontFileName)
	ufoBaseName = os.path.splitext(fontFileName)[0]
#	markFileName = 'mark_%s.fea' % ufoBaseName
	styleName = ufoFont.info.styleName

	print '*******************************'
	print 'Exporting mark files for %s...' % (styleName)
	
	WriteFeaturesMarkFDK.MarkDataClass(ufoFont, folderPath, trimCasingTags, genMkmkFeature, writeClassesFile, indianScriptsFormat)


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

	fontPath = os.path.abspath(sys.argv[-1])

	print fontPath
	fontsList = []

	if os.path.exists(fontPath) and fontPath.lower().endswith('.ufo'):
		generateMarkFiles(fontPath)

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
