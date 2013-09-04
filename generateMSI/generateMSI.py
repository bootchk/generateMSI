'''
Generate .msi from template via WiX tools.

A scripting of a process.
Where the process is 'generate an installer for Windows',
Which is a subprocess of 'publish', a subprocess of 'develop software'.

The scripting accomplishes:
- generates GUIDs into pipe
- edit the WiX source (so you don't have to understand WiX XML.)
- automates calling of WiX tools
- FUTURE parameterize with the version, etc. for redo or repeat
It is a layer above the WiX layer.

Capability: VERY LIMITED.
This creates a very simple MSI, for a very simple case.
In other words, it is hardcoded and inflexible except for a few parameters (see below)
The same name is used ubuiquitously for the product, company, websites, certain directories, etc.
It also installs a fixed set of components (see below.)
In other words: use case specific to a company with a single product, where the product
- is a single executable,
- has its own mimetype.
But you could change template for a different use case.

Requires of the machine it runs on:
- Windows OS
- WiX toolset installed
- Python installed

Preconditions: you have, in some directory (? same as where the script resides ?)
- created a single binary for your app (say using PyInstaller)
- created a single app icon (.ico) for your app and its mimetype
- edit the template map so that it describes your app

Postcondition:
- a .msi file is created (or overwritten).  FUTURE named for the version

To use: 
- edit the template map (first time: all variables, subsequent times, just the version number?)
- copy any updated app.exe to the directory
- >python generateMSI.py
- double click on generated .msi to test
- copy the generated .msi file to your distribution chain

Variables:
- appName used to name the binary and the .ico and the install directory
- companyName must be used to name the company and its website e.g. company.org

Components installed:
- a single executable
- an association of the app to its new mimetype
- a single icon (for both the app and its mimetype)
- a single shortcut in the start menu
(Notably missing: help files, copyright file, desktop shortcut)

TODO
test what happens if already installed

FUTURE
======

args for whether to include mimetype
------------------------------------

Upgrades
--------

Repeat runs
-----------
You MUST leave the generated source file (.wsc ) to serve as 'database of GUID' for subsequent uses.

User interface on the command line (query and response) or args

Every use can be:
- initial run for this app (requires you to cut and paste a GUID, say from guid.com)
- redo of previous run (when initial generated MSI was found flawed in testing.)
- subsequent run for a another release of same app, generates another named .msi
(e.g. increments the bug fix version number)

'''
from string import Template
from uuid import uuid4
from subprocess import call

import templateWiX


def createFilename(templateString):
  # fab filename from template string and template map
  template = Template(templateString)
  return template.substitute(templateWiX.TEMPLATE_MAP)


def createWiXSourceFromTemplate():
  generateGUIDToTemplate()
  return Template(templateWiX.WIX_TEMPLATE).substitute(templateWiX.TEMPLATE_MAP)


def generateGUIDToTemplate():
  '''
  We're profligate with UUIDs.  Read up, there's no point in conserving.
  But we should conserve the upgradeGUID for use in upgrades (FUTURE.)
  '''
  templateWiX.TEMPLATE_MAP['upgradeGUID'] = getGUIDUpperCase()
  templateWiX.TEMPLATE_MAP['appExecutableGUID'] = getGUIDUpperCase()
  templateWiX.TEMPLATE_MAP['appStartMenuItemGUID'] = getGUIDUpperCase()


def getGUIDUpperCase():
  ''' Upper case UUID.  WTF it's MS innovation. '''
  return str(uuid4()).upper()


def generateMSIFromWIX(source):
  
  outFilename = createFilename(templateWiX.OUT_FILENAME_TEMPLATE)
  sourceFileName = createFilename(templateWiX.SOURCE_FILENAME_TEMPLATE)
  intermediateFileName = createFilename(templateWiX.INTERMEDIATE_FILENAME_TEMPLATE)
  
  # Write source xml text to file for WiX input
  with open(sourceFileName, 'w') as f:
    f.write(source)
    
  # invoke WiX tools in a chain through intermediate
  WiXBinPath = "c:/Program Files/WiX Toolset v3.7/bin/"
  candlePath = WiXBinPath + "candle"
  lightPath = WiXBinPath + "light"
  try:
    # WiX is two tools in sequence with an intermediate file
    # '-out filename' is optional: will create files in current directory (not to standard out)
    result = call([candlePath, sourceFileName])
    if result:  # non-zero is error
      # assert candle printed error to console
      print "candle failed"
      return
    '''
    ask light to rename outfile from the default to name with version appended.
    Can't get this to work, so just rename it in Python, or do it manually
    result = call([lightPath, " -out " + outFilename + " " + intermediateFileName])
    '''
    result = call([lightPath, intermediateFileName])
    # TODO rename

    if result:
      print "light failed"
      return
  except OSError:
    print "Is WiX toolset installed and in PATH?"
    raise
  # TODO clean source and intermediate? but no harm, they will be overwritten on future runs
  # TODO but capture version number?
  print "Generated  'appName'.msi in current directory.  You might rename it to: ", outFilename


def main():
  
  # FUTURE UI: dialog to figure out what kind of run, then futz with guid and version in template map
  
  WiXSource = createWiXSourceFromTemplate()
  # print WiXSource
  generateMSIFromWIX(WiXSource)
  
  
  
if __name__ == '__main__':
    main()
    