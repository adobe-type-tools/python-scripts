# Copyright 2014 Adobe. All rights reserved.

"""
For a UFO font, check that the glyph hashes stored when checkOutlines or
autohint were last run still match the source glyph hashes.
If not, all outdated glyphs are deleted from the Adobe processed layer.
"""

__usage__ = """
   checkUFOProcessedLayer  v1.0 July 17 2013

   checkUFOProcessedLayer [-checkOnly] <ufo font path>

   Options:
    -checkOnly  When this option is specified, the tool will report
    which glyphs in the processed layer are outdated, but will not
    delete them.


"""

import sys
from afdko import ufoTools

kSrcGLIFHashMap = "com.adobe.type.autoHintHashMap"


def run():
    fontPath = sys.argv[1]
    doSync = True
    allMatch, msgList = ufoTools.checkHashMaps(fontPath, doSync)
    if allMatch:
        print("All processed glyphs match")
    else:
        for msg in msgList:
            print(msg)


if __name__ == "__main__":
    run()
