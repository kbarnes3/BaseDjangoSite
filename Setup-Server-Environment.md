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
```sudo apt-get autoremove```  
```sudo reboot```
1. After you log in again, make a note of your IP address. ```ifconfig``` will print the IP address if the welcome message does not.
1. At this point, Fabric should be able to connect with a hostname of the form ```username@a.b.c.d``` where ```username``` is the username for the user set up by the Ubuntu installer and ```a.b.c.d``` is the IP address noted previously. If a DNS record exists that points to ```a.b.c.d```, that can be used as well. At this point, you'll need to log in with your password. After the initial setup, it's recommended that you only connect using SSH public-key authentication, which can be setup below.

Setup user account for deploying
------------------------

These steps will prepare your user account to be used to successfully deploy and update a NewDjangoSite deployment to your server. These steps can be used to create a new user or modify an existing user.

1. Make sure you run all the following commands in a PowerShell prompt set up by following Setup-Dev-Environment.md
1. The Fabric command ```setup_user``` is used to configure a new or existing user account. It takes a series of required and optional parameters. Run one of the below commands to setup a user account.  
    1. The first parameter is ```$linux_user$```. ```$linux_user$``` is either an existing user account or the name of the user you want to create. This account will be prepped to deploy and update NewDjangoSite sites, which includes being granted sudo access. The simplest form of the ```setup_user``` command is ```fab setup_user:$linux_user$```.  
    1. The second parameter is ```no_sudo_passwd``` which indicates you don't want to be challenged with a password when running sudo logged in as ```$linux_user$```. This is recommended if you plan on logging in using a public/private key pair. If this parameter is provided, any value other than an empty string will be interpretted as true. This parameter defaults to '' if not provided. Specifying this parameter will resemble this:  
    ```fab "setup_user:$linux_user$,no_sudo_passwd=true"```  
    Note that PowerShell requires everything from "setup_user" onward to be in quotes due to the comma.
    1. The third parameter is ```public_key_file```. This parameter specifies a file on disk that contains a public key that should be used for authentication of SSH instead of the user password. This parameter should probably be used in conjunction with ```no_sudo_passwd``` if you don't want to have to specify a password as soon as Fabric runs a command with sudo. Specifying this parameter will resemble this:  
    ```fab "setup_user:$linux_user$,no_sudo_passwd=true,public_key_file=C:\Users\You\.ssh\id_rsa.pub"```  
    Note that PowerShell requires everything from "setup_user" onward to be in quotes due to the commas.
1. When prompted by Fabric to enter a hostname, the username you provide must already exist and have sudo access. This may or may not be the same as the ```$linux_user$``` provided above.
1. More public keys can be added with the command:  
```fab "add_authorized_key:$linux_user,C:\Users\You\.ssh\id_rsa.pub"```
1. Repeat these steps for any additional users. Note that if ```$linux_user$``` does not exist, it will be created with a password disabled. If public key authentication is not going to be used for this account, you'll need to log in and set a password manually.
1. If public key authentication is going to be used exclusively for remote access, you can disable password based authentication by running:  
```fab disable_ssh_passwords```  
and following the directions printed.
