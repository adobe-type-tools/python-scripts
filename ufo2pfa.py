#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import time
from subprocess import Popen, PIPE


__doc__ = """
ufo2pfa v2.0 - Feb 03 2016

This script takes a path to a folder as input, finds all the UFO fonts
inside that folder and its subdirectories, and converts them to Type 1
fonts (.pfa files). If a path is not provided, the script will use the
current path as the top-most directory.

==================================================
Versions:
v1.0 - Feb 23 2013 - Initial release
v2.0 - Feb 03 2016 - Modernized and removed defcon and ufo2fdk dependencies.
"""


def getFontPaths(path):
    fontsList = []
    for r, folders, files in os.walk(path):
        for folder in folders:
            fileName, extension = os.path.splitext(folder)
            extension = extension.lower()
            if extension == ".ufo":
                fontsList.append(os.path.join(r, folder))

    return fontsList


def doTask(fonts):
    totalFonts = len(fonts)
    print("%d fonts found" % totalFonts)
    i = 1

    for font in fonts:
        folderPath, fontFileName = os.path.split(font)
        styleName = os.path.basename(folderPath)

        # Change current directory to the folder where the font is contained
        os.chdir(folderPath)

        print('\n*******************************')
        print('Processing %s...(%d/%d)' % (styleName, i, totalFonts))

        # Assemble PFA file name
        fileNameNoExtension, fileExtension = os.path.splitext(fontFileName)
        pfaPath = fileNameNoExtension + '.pfa'

        # Convert UFO to PFA using tx
        cmd = 'tx -t1 "%s" "%s"' % (fontFileName, pfaPath)
        popen = Popen(cmd, shell=True, stdout=PIPE)
        popenout, popenerr = popen.communicate()
        if popenout:
            print(popenout)
        if popenerr:
            print(popenerr)

        i += 1


def run():
    # if a path is provided
    if len(sys.argv[1:]):
        baseFolderPath = os.path.normpath(sys.argv[1])

        # make sure the path is valid
        if not os.path.isdir(baseFolderPath):
            print('Invalid directory.')
            return

    # if a path is not provided, use the current directory
    else:
        baseFolderPath = os.getcwd()

    t1 = time.time()
    fontsList = getFontPaths(os.path.abspath(baseFolderPath))

    if len(fontsList):
        doTask(fontsList)
    else:
        print("No fonts found.")
        return

    t2 = time.time()
    elapsedSeconds = t2 - t1
    elapsedMinutes = elapsedSeconds / 60

    if elapsedMinutes < 1:
        print('Completed in %.1f seconds.' % elapsedSeconds)
    else:
        print('Completed in %.1f minutes.' % elapsedMinutes)


if __name__ == '__main__':
    run()
