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

import sys, os, time
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

fontsList = []

def getFontPaths(path, startpath):
#	print "Searching in path...", path
	files = os.listdir(path)
	for file in files:
		if file[-4:].lower() in [".ufo"]:
			fontsList.append(os.path.join(path, file))	#[len(startpath)+1:])
		else:
			if os.path.isdir(os.path.join(path, file)):
				getFontPaths(os.path.join(path, file), startpath)


def doTask(fonts):
	totalFonts = len(fonts)
	print "%d fonts found\n" % totalFonts
	i = 0

	for font in fonts:
		i += 1
		folderPath, fontFileName = os.path.split(font)  # path to the folder where the font is contained and the font's file name
		styleName = os.path.basename(folderPath) # name of the folder where the font is contained

		# Change current directory to the folder where the font is contained
		os.chdir(folderPath)

		print '*******************************'
		print 'Exporting mark files for %s...(%d/%d)' % (styleName, i, totalFonts)
		
		ufoFont = Font(fontFileName)
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

	getFontPaths(baseFolderPath, baseFolderPath)
		
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
