#!/usr/bin/env python

"""
This script takes a path to a folder as input, finds all
UFOs inside that folder and its subdirectories, and outputs each
font's kerning in OT feature file syntax.
If a path is not provided, the script uses the current path as the topmost
directory. The name of the resulting kerning FEA file is managed by the
kernFeatureWriter module.
"""

import os
import sys
import time

module_not_found = False

try:
    from defcon import Font
except ImportError:
    print(
        "ERROR: This script requires defcon. It can be downloaded from "
        "https://github.com/typesupply/defcon"
    )
    module_not_found = True
try:
    import kernFeatureWriter
except ImportError:
    print(
        "ERROR: This script requires kernFeatureWriter.py. It can be "
        "downloaded from https://github.com/adobe-type-tools/python-modules"
    )
    module_not_found = True


def get_ufo_paths(startpath):
    ufo_paths = []
    for dir_path, _, _ in os.walk(startpath):
        if dir_path.lower().endswith('.ufo'):
            ufo_paths.append(dir_path)
    return sorted(ufo_paths)


def write_kern_features(ufo_list):
    total_ufos = len(ufo_list)
    print("%d fonts found\n" % total_ufos)

    for i, ufo in enumerate(ufo_list, 1):
        styleName = os.path.basename(os.path.dirname(os.path.normpath(ufo)))
        exportMessage = 'Exporting kern files for %s...(%d/%d)' % (
            styleName, i, total_ufos)
        print('*' * len(exportMessage))
        print(exportMessage)

        d_font = Font(ufo)
        kfw_args = kernFeatureWriter.Defaults()
        kfw_args.input_file = ufo
        kfw_args.write_subtables = True
        # can set more options here, e.g.
        # kfw_args.min_value = 5  # instead of 3
        kernFeatureWriter.run(d_font, kfw_args)


def run():
    # if a path is provided
    if len(sys.argv[1:]):
        base_path = os.path.normpath(sys.argv[1])

        # make sure the path is valid
        if not os.path.isdir(base_path):
            print('Invalid directory.')
            return 1

    # if a path is not provided, use the current directory
    else:
        base_path = os.getcwd()

    t1 = time.time()
    ufo_list = get_ufo_paths(base_path)
    if len(ufo_list):
        write_kern_features(ufo_list)
    else:
        print("No fonts found")
        return 1

    t2 = time.time()
    elapsedSeconds = t2 - t1
    elapsedMinutes = elapsedSeconds / 60

    if elapsedMinutes < 1:
        print(('Completed in %.1f seconds.' % elapsedSeconds))
    else:
        print(('Completed in %.1f minutes.' % elapsedMinutes))


if __name__ == '__main__':
    if module_not_found:
        sys.exit(1)
    run()
