'''
template for a WiX input file

Note that $$ is string.Template's escape mechanism: yields a single $ (for use in WiX variables.)
'''

# Can't user 0.0.1-beta for version???

TEMPLATE_MAP = { \
'appName'  : 'pensool',
'companyName' : 'Pensool.org',
'guid' : '12345678-1234-1234-1234',
'version' : '0.0.1',
'mimetypeExtension' : 'pnl'
 }

SOURCE_FILENAME_TEMPLATE = r'''${appName}.wxs'''
INTERMEDIATE_FILENAME_TEMPLATE = r'''${appName}.wixobj'''
OUT_FILENAME_TEMPLATE = r'''${appName}_$version.msi'''



WIX_TEMPLATE = r'''<?xml version="1.0"?>
<?define ProductVersion = "$version"?>
<?define ProductUpgradeCode = "$guid-111111111111"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
   <Product Id="*" UpgradeCode="$$(var.ProductUpgradeCode)" 
            Name="appName" Version="$$(var.ProductVersion)" Manufacturer="$companyName" Language="1033">
      <Package InstallerVersion="200" Compressed="yes" Comments="Windows Installer Package"/>
      <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
      <Icon Id="ProductIcon" SourceFile="$appName.ico"/>
      <Property Id="ARPPRODUCTICON" Value="ProductIcon"/>
      <Property Id="ARPHELPLINK" Value="http://www.$companyName/help"/>
      <Property Id="ARPURLINFOABOUT" Value="http://www.$companyName/about"/>
      <Property Id="ARPNOREPAIR" Value="1"/>
      <Property Id="ARPNOMODIFY" Value="1"/>
      <Upgrade Id="$$(var.ProductUpgradeCode)">
         <UpgradeVersion Minimum="$$(var.ProductVersion)" OnlyDetect="yes" Property="NEWERVERSIONDETECTED"/>
         <UpgradeVersion Minimum="0.0.0" Maximum="$$(var.ProductVersion)" IncludeMinimum="yes" IncludeMaximum="no" 
                         Property="OLDERVERSIONBEINGUPGRADED"/>    
      </Upgrade>
      <Condition Message="A newer version of this software is already installed.">NOT NEWERVERSIONDETECTED</Condition>
 
      <!-- components copied/created on install machine -->
      <Directory Id="TARGETDIR" Name="SourceDir">
      
         <Directory Id="ProgramFilesFolder">
            <Directory Id="INSTALLDIR" Name="$appName">
               <Component Id="ApplicationFiles" Guid="$guid-222222222222">
                  <!-- Use executable from current working directory. -->
                  <File Id="ApplicationFile1" Source="./$appName.exe"/>
                  
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
               <Component Id="ApplicationShortcuts" Guid="$guid-333333333333">
                  <Shortcut Id="ApplicationShortcut1" Name="$appName" Description="$appName" 
                            Target="[INSTALLDIR]$appName.exe" WorkingDirectory="INSTALLDIR"/>
                  <RegistryValue Root="HKCU" Key="Software\$companyName\$appName" 
                            Name="installed" Type="integer" Value="1" KeyPath="yes"/>
                  <RemoveFolder Id="ProgramMenuSubfolder" On="uninstall"/>
               </Component>
            </Directory>
         </Directory>
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
