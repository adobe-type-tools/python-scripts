Python scripts
=========================
Assortment of scripts that run on the command line, i.e. **Terminal** on Mac OS X, and **Command Prompt** on Windows.

Installation
-----
**Mac OS X**: A version of Python is already installed.

**Windows**: You will need to install one of the 2.x versions available at [python.org](http://www.python.org/getit/).

Dependencies
-----
Some of the scripts may require additional Python packages or depend on certain tools being installed and appropriately configured to run on the command line.
Here is a list of the locations from which you may need to get the extra tools and packages:

* [Adobe Font Development Kit for OpenType (AFDKO)](http://www.adobe.com/devnet/opentype/afdko.html)
 * makeotf
 * autohint
 * tx
 * ttx
 * detype1
 * spot

* [FontTools](http://sourceforge.net/projects/fonttools/)

* [RoboFab](http://www.robofab.org/)

* [Type Supply](http://code.typesupply.com/)
 * defcon
 * ufo2fdk
 * woffTools

Using the scripts
-----
1. Download the [ZIP package](https://github.com/adobe-type-tools/python-scripts/archive/master.zip) and unzip it.
2. 
 * Most of the scripts will run by simply typing `python ` followed by the file name of the script, e.g. `python theScript.py`.
 * If the script is in a different directory from which you are trying to run it, you will need to provide the full path to the script's file, e.g. `python /Users/myself/foldername/theScript.py`.
 * Some scripts may allow you to use options, or require that you provide input files. To learn how to use those scripts, open them in a text editor app (e.g. TextEdit, Notepad) and read the documentation near the top of the file.
