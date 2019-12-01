#!/usr/bin/env python

import os
import sys
import time

############################################
# THE VALUES BELOW CAN BE EDITED AS NEEDED #
############################################

minKern = 3
# This value is inclusive; this means that pairs which EQUAL this ABSOLUTE
# value will NOT be ignored/trimmed. Any kerning pair that falls in the range
# from 0-minKern to 0+minKern will be ignored.
writeTrimmed = False
# If 'False', trimmed pairs will not be processed and therefore will not be
# written to the kerning feature file.
# If 'True', trimmed pairs will be written, but commented out.
writeSubtables = False
# Sometimes the kerning feature file needs to have explicit subtable breaks,
# otherwise the OTF won't compile due to a subtable overflow.


libraryNotFound = False

try:
    from defcon import Font
except ImportError:
    print(
        "ERROR: This script requires defcon. "
        "It can be downloaded from https://github.com/typesupply/defcon")
    libraryNotFound = True
try:
    import WriteFeaturesKernFDK
except ImportError:
    print(
        "ERROR: This script requires WriteFeaturesKernFDK.py. "
        "It can be downloaded from "
        "https://github.com/adobe-type-tools/python-modules")
    libraryNotFound = True

if libraryNotFound:
    sys.exit()


def generateKernFile(font):

    folderPath, fontFileName = os.path.split(font)
    # path to the folder where the font is contained and the font's file name
    os.chdir(folderPath)

    ufoFont = Font(fontFileName)
    ufoBaseName = os.path.splitext(fontFileName)[0]
    kernFileName = 'kern_%s.fea' % ufoBaseName
    styleName = ufoFont.info.styleName

    print('*******************************')
    print('Kerning for %s...' % (styleName))

    WriteFeaturesKernFDK.KernDataClass(
        ufoFont, folderPath, minKern,
        writeTrimmed, writeSubtables, kernFileName
    )


def run():
    # if a path is provided
    if len(sys.argv[1:]):
        baseFolderPath = sys.argv[1]

        if baseFolderPath[-1] == '/':  # remove last slash if present
            baseFolderPath = baseFolderPath[:-1]

        # make sure the path is valid
        if not os.path.isdir(baseFolderPath):
            print('Invalid directory.')
            return

    # if a path is not provided, use the current directory
    else:
        baseFolderPath = os.getcwd()

    t1 = time.time()

    fontPath = os.path.abspath(sys.argv[-1])
    print(fontPath)

    if os.path.exists(fontPath) and fontPath.lower().endswith('.ufo'):
        generateKernFile(fontPath)

    else:
        print("No fonts found")
        return

    t2 = time.time()
    elapsedSeconds = t2 - t1
    elapsedMinutes = elapsedSeconds / 60

    if elapsedMinutes < 1:
        print(('Completed in %.1f seconds.' % elapsedSeconds))
    else:
        print(('Completed in %.1f minutes.' % elapsedMinutes))


if __name__ == '__main__':
    run()
