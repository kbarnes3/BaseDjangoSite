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
```sudo apt-get remove unattended-upgrades```  
```sudo reboot```
1. After you log in again, make a note of your IP address. ```ifconfig``` will print the IP address if the welcome message does not.
1. At this point, Fabric should be able to connect with a hostname of the form ```username@a.b.c.d``` where ```username``` is the username for the user set up by the Ubuntu installer and ```a.b.c.d``` is the IP address noted previously. At this point, you'll need to log in with your password.

Setup user account for deploying
------------------------

These steps will prepare your user account to be used to successfully deploy and update a NewDjangoSite deployment to your server. These steps can be used to create a new user or modify an existing user.