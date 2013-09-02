'''
Generate .msi from template via WiX tools.

A scripting of a process.
Where the process is 'generate an installer for Windows',
Which is a subprocess of 'publish', a subprocess of 'develop software'.

The scripting accomplishes:
- edit the WiX source (so you don't have to understand WiX XML.)
- automates calling of WiX tools
- FUTURE parameterize with the version, etc. for redo or repeat
It is a layer above the WiX layer.

Capability: VERY LIMITED.
This creates a very simple MSI, for a very simple case.
In other words, it is hardcoded and inflexible except for a few parameters (see below)
The same name is used ubuiquitously for the product, company, websites, certain directories, etc.
It also installs a fixed set of components (see below.)
In other words: specific to a company with a single product, where the product has its own mimetype.

Requires of the machine it runs on:
- Windows OS
- WiX toolset installed
- Python installed

Preconditions: you have, in some directory (? same as where the script resides ?)
- created a single binary for your app (say using PyInstaller)
- created a single app icon (.ico) for your app and its mimetype
- edit the template map so that it describes your app

Postcondition:
- a .msi file is created (or overwritten), named for the version

To use: 
- edit the template map (first time: all variables, subsequent times, just the version number?)
- copy any updated app.exe to the directory
- >python generateMSI.py
- copy the generated .msi file to your distribution chain

Variables:
- appName used to name the binary and the .ico and the install directory
- companyName must be used to name the company and its website e.g. company.org

Components installed:
- a single executable
- a single icon (for both the app and its mimetype)
- a single shortcut in the start menu
(Notably missing help files, copyright file.)

FUTURE
------
You MUST leave the generated source file (.wsc ) to serve as 'database' for subsequent uses.

User interface on the command line (query and response.)

Every use can be:
- initial run for this app (requires you to cut and paste a GUID, say from guid.com)
- redo of previous run (when initial generated MSI was found flawed in testing.)
- subsequent run for a another release of same app, generates another named .msi
(e.g. increments the bug fix version number)

'''
from string import Template
from subprocess import call

import templateWiX


def createFilename(templateString):
  # fab filename from template string and template map
  template = Template(templateString)
  return template.substitute(templateWiX.TEMPLATE_MAP)


def createWiXSourceFromTemplate():
  template = Template(templateWiX.WIX_TEMPLATE)
  return template.substitute(templateWiX.TEMPLATE_MAP)


def generateMSIFromWIX(source):
  
  
  outFilename = createFilename(templateWiX.OUT_FILENAME_TEMPLATE)
  sourceFileName = createFilename(templateWiX.SOURCE_FILENAME_TEMPLATE)
  intermediateFileName = createFilename(templateWiX.INTERMEDIATE_FILENAME_TEMPLATE)
  
  # Write source xml text to file
  with open(sourceFileName, 'w') as f:
    f.write(source)
    
  # invoke WiX tools in a chain through intermediate
  try:
    # WiX is two tools in sequence with an intermediate file
    call(["candle", sourceFileName])
    # ask light to rename its output file from the default
    call(["light", "-out " + outFilename + " " + intermediateFileName])
  except OSError:
    print "Is WiX toolset installed and in PATH?"
    raise
  print "Generated in current directory:", outFilename


def main():
  
  # FUTURE UI: dialog to figure out what kind of run, then futz with guid and version in template map
  
  WiXSource = createWiXSourceFromTemplate()
  print WiXSource
  generateMSIFromWIX(WiXSource)
  
  
  
if __name__ == '__main__':
    main()