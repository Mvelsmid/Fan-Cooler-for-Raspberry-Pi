

# Fan-Cooler-for-Raspberry-Pi
PWM Fan Cooler - latest version 1.2 (21.7.2020)
1. Download and modifi fanpwm.py file  /default pin = GPIO4 (on Board Pin 7)  -  set your values in lines 12 to 18
2. Coppy files to Rpi Folder: /storage/.kodi/userdata
3. reboot Rpi

for LibreELEC 10.0.1 and up:

Since version 10.0.1, LibreElec canceled the automatic execution of the autoexec.py script from the userdata folder.
A script for controlling the fan was started via autoexec,py. So it won't work like that in the new LE versions.
The solution is to create an addon that will run this script.
Create a new folder service.autoexec in the addons folder

1. create a new addon.xml file with the content:

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="service.autoexec" name="Autoexec Service" version="1.0.0" provider-name="name">
    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
    </requires>
    <extension point="xbmc.service" library="autoexec.py">
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en_GB">Automatically run python code when Kodi starts.</summary>
        <description lang="en_GB">The Autoexec Service will automatically be run on Kodi startup.</description>
        <platform>all</platform>
        <license>GNU GENERAL PUBLIC LICENSE Version 2</license>
    </extension>
</addon>


2. create another autoexec.py file with the content:

import xbmc
xbmc.executebuiltin("RunScript(/storage/.kodi/userdata/fanpwm.py)")

3. In the userdata folder, put the script fanpwm.py

4. from the repository (Libreelec Add-ons) install Raspberry Tools (RPi.GPIO)
5. reboot the RPi
6. go to my add-ons and enable Autoexec Service




