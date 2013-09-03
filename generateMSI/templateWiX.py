'''
template for a WiX input file

Note we don't use XML variables: use templating at this level.
(WiX and MS Installer also have variables, called properties?)

TODO fix guidPrefix:  if a component is replaced, generate new GUID.

In same directory, use this structure for the archive of source (in the sense: source of copy to target)
??? 

appName.exe
appName.ico

'''

# Can't user 0.0.1-beta for version???

TEMPLATE_MAP = { \
'appName'  : 'pensool',
'companyName' : 'Pensool.org',
'guidPrefix' : '12345678-1234-1234-1234',
'productGUID' : '12345678-1234-1234-1234-000000000000',
'upgradeGUID' : '12345678-1234-1234-1234-111111111111',
'version' : '0.0.1',
'mimetypeExtension' : 'pnl'
 }

SOURCE_FILENAME_TEMPLATE = r'''${appName}.wxs'''
INTERMEDIATE_FILENAME_TEMPLATE = r'''${appName}.wixobj'''
OUT_FILENAME_TEMPLATE = r'''${appName}_$version.msi'''


WIX_TEMPLATE = r'''<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" 
        UpgradeCode="$upgradeGUID" 
        Version="$version" 
        Language="1033" 
        Name="$appName" 
        Manufacturer="$companyName">
        
        <Package InstallerVersion="300" 
          Compressed="yes"/>
        <Media Id="1" 
          Cabinet="$appName.cab" 
          EmbedCab="yes" />
        <!-- FUTURE icon 
        <Icon Id="ProductIcon" SourceFile="$appName.ico"/>
        -->

        <!-- Step 1: Define the directory structure -->
        <Directory Id="TARGETDIR" Name="SourceDir">
          
          <Directory Id="ProgramFilesFolder">
              <Directory Id="AppRootDir" Name="$appName"/>
          </Directory>
          
          <Directory Id="ProgramMenuFolder">
            <Directory Id="ProgramMenuSubfolder" Name="$appName">
          </Directory>
          
        </Directory>


        <!-- Step 2: Add files to your installer package
        Here, source for WiX is working directory at WiX time (where WiX invoked, where .wxs is located.)
        -->
        <DirectoryRef Id="AppRootDir">
            <Component Id="AppBinaries" Guid="$guidPrefix-222222222222">
                <File Id="myapplication.exe" 
                  Source="$appName.exe" 
                  KeyPath="yes" Checksum="yes"/>
                  
                <!-- register mimetype.  Probably not safe from conflict with existing mimetypes. -->
                <ProgId Id="$appName.$mimetypeExtension" Description="$appName file type">
                  <Extension Id="$mimetypeExtension" ContentType="application/$mimetypeExtension">
                     <Verb Id="open" Command="open" TargetFile="$appName.exe" Argument='"%1"'/>
                  </Extension>
                </ProgId>
            </Component>
            
            <!-- FUTURE
            <Component Id="documentation.html" Guid="PUT-GUID-HERE">
                <File Id="documentation.html" Source="MySourceFiles\documentation.html" KeyPath="yes"/>
            </Component>
            -->
        </DirectoryRef>
        
        <DirectoryRef Id="ProgramMenuSubfolder">
          <Component Id="AppStartMenuItem" Guid="$guidPrefix-333333333333">
             <Shortcut Id="AppMenuShortcut" Name="$appName" Description="$appName" 
                       Target="[AppRootDir]$appName.exe" WorkingDirectory="AppRootDir"/>
             <RegistryValue Root="HKCU" Key="Software\$companyName\$appName" 
                       Name="installed" Type="integer" Value="1" KeyPath="yes"/>
             <RemoveFolder Id="ProgramMenuSubfolder" On="uninstall"/>
           </Component>
        </DirectoryRef>
        
        <!-- FUTURE DesktopShortcut -->

        <!-- Step 3: Tell WiX what components a featureSet comprises -->
        <Feature Id="AppAndShortcuts" Title="App and shortcuts" Level="1">
            <ComponentRef Id="AppBinaries" />
            <ComponentRef Id="AppStartMenuItem"/>
            <!-- FUTURE DesktopShortcut -->
        </Feature>
    </Product>
</Wix>
'''


WIX_TEMPLATE_OLD = r'''<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="$productGUID" UpgradeCode="$upgradeGUID" 
           Name="appName" Version="$version" Manufacturer="$companyName" Language="1033">
     <Package Id='*' Keywords='Installer' Description="Installs $appName"
       InstallerVersion="200" Compressed="yes" 
       Comments="Package created by $companyName"/>
     <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
     <Icon Id="ProductIcon" SourceFile="$appName.ico"/>
     <Property Id="ARPPRODUCTICON" Value="ProductIcon"/>
     <Property Id="ARPHELPLINK" Value="http://www.$companyName/help"/>
     <Property Id="ARPURLINFOABOUT" Value="http://www.$companyName/about"/>
     <Property Id="ARPNOREPAIR" Value="1"/>
     <Property Id="ARPNOMODIFY" Value="1"/>
     <Upgrade Id="$upgradeGUID">
        <UpgradeVersion Minimum="$version" OnlyDetect="yes" Property="NEWERVERSIONDETECTED"/>
        <UpgradeVersion Minimum="0.0.0" Maximum="$version" IncludeMinimum="yes" IncludeMaximum="no" 
                        Property="OLDERVERSIONBEINGUPGRADED"/>    
     </Upgrade>
     <Condition Message="A newer version of this software is already installed.">NOT NEWERVERSIONDETECTED</Condition>
  
     <!-- See numerous posts for explanation of next line.  Basically, source is same directory where .msi is located. -->
     <Directory Id="TARGETDIR" Name="SourceDir">
       
       <!-- components copied/created on install machine -->
       
        <Directory Id="ProgramFilesFolder">
           <!-- INSTALLDIR is a property (variable).  Here named by appName, not appName_version? -->
           <Directory Id="INSTALLDIR" Name="$appName">
              <Component Id="ApplicationFiles" Guid="$guidPrefix-222222222222">
                 <!-- Use executable from current working directory. -->
                 <File Id="ApplicationFile1" Source="$appName.exe"/>
                 
                 <!-- register mimetype.  Probably not safe from conflict with existing mimetypes. -->
                 <ProgId Id="$appName.$mimetypeExtension" Description="$appName file type">
                    <Extension Id="$mimetypeExtension" ContentType="application/$mimetypeExtension">
                       <Verb Id="open" Command="open" TargetFile="$appName.exe" Argument='"%1"'/>
                    </Extension>
                 </ProgId>
                 
              </Component>
           </Directory>
        </Directory>
  
        <Directory Id="ProgramMenuFolder">
           <Directory Id="ProgramMenuSubfolder" Name="$appName">
              <Component Id="ApplicationShortcuts" Guid="$guidPrefix-333333333333">
                 <Shortcut Id="ApplicationShortcut1" Name="$appName" Description="$appName" 
                           Target="[INSTALLDIR]$appName.exe" WorkingDirectory="INSTALLDIR"/>
                 <RegistryValue Root="HKCU" Key="Software\$companyName\$appName" 
                           Name="installed" Type="integer" Value="1" KeyPath="yes"/>
                 <RemoveFolder Id="ProgramMenuSubfolder" On="uninstall"/>
              </Component>
           </Directory>
        </Directory>
        
        <!-- Desktop TODO -->
        
     </Directory>
  
     <InstallExecuteSequence>
        <RemoveExistingProducts After="InstallValidate"/>
     </InstallExecuteSequence>
  
     <Feature Id="DefaultFeature" Level="1">
        <ComponentRef Id="ApplicationFiles"/>
        <ComponentRef Id="ApplicationShortcuts"/>     
     </Feature>
  </Product>
</Wix>

'''
