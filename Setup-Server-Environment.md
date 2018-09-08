Setup Your Server Environment
=============================

These directions will set up a new server.
They are the same directions for setting up a test server stack or a full production environment.
For consistency, the only OS supported for a server is Ubuntu Server 18.04.
Most server operations should be done through Fabric, which is already installed if you followed the steps in Setup-Dev-Environment.md.
Fabric can be run by running ```fab``` in a virtualenv while in the \web directory.
To simplify this, \scripts\Invoke-Fabric.ps1 or the ```Invoke-Fabric``` function can be used from PowerShell.

Prep for Fabric
---------------

Some steps need to be performed manually before Fabric can be used.

1. Set up a new Ubuntu Server 18.04 install, following the official documentation
1. Once you can log in, do an initial update:  
```sudo apt-get update```  
```sudo apt-get dist-upgrade```  
```sudo reboot```
