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

Setup global server environment
-------------------------------
These steps will install system wide packages and make other global changes that will impact all deployments on this server. These steps only need to be run once.

1. Run ```fab setup_server``` or ```fab "setup_server:setup_wins=True"```. This script will install a variety of packages with apt-get, make various directories, and properly secure these directories. Adding the ```setup_wins``` parameter will configure the server to broadcast its name via the WINS protocol. This lets you refer to the server by the value in ```/etc/hostname``` from a Windows computer on the same subnet. Consider adding ```setup_wins``` if this server is on the same subnet as Windows computers that will interact with it.

Setup deployment
----------------
These steps will get a specific deployment of NewDjangoSite running on a server that's been setup using the above directions. Any server can run one or more of the available deployments (prod, staging, daily, dev). See the ```web/newdjangosite/settings*.py``` files for the differences between the deployments. These steps can be repeated once for each desired deployments.

1. Consider updating the database username and password found in ```web/newdjangosite/settings_$deployment$.py``` file. If you update it, commit and push your changes before continuing. Note that the Fabric script won't work with passwords containing shell escape characters.
1. Run ```auth``` and follow the prompts in the browser, logging into GitHub with an account that can set deploy keys on this repo.
1. Run ```fab setup_deployment:$deployment$```
1. When prompted for a passphrase after seeing "Generating public/private rsa key pair", an empty passphrase is recommended
1. When prompted for a primary email and subsequent fields, enter the information for the Django superuser to create
1. The OAuth token stored by ```auth``` is no longer needed unless you intend to setup more deployments. It isn't used to updated a deployment in the steady state. Optionally, you can remove the token by running ```auth delete```.

Finishing up global server deployment
-------------------------------------
The files in config/ubuntu-18.04/global can impact all the Django sites running on the server, so they aren't routinely deployed. After your first deployment, or after updating these files, they need to be explictly deployed. They can be deployed with:  
```fab deploy_global_config:$deployment$```  
Note that no changes are made to ```$deployment$```, the files are just copied from that deployment at its current state. You may need to deploy to ```$deployment$``` to ensure recent updates to the global files are in the deployment's repo first. See the next section for details on deploying.

Deploying new changes
---------------------
Once a server deployment is set up, only one command is generally needed to update it with the latest changes pushed to GitHub:  
```fab deploy:$deployment$```  
This command replies on configuration parameters defined at the top ```web/newdjangosite/fabric_utils/deploy.py``` to define the behaviors that should be different on a per-deployment basis. Settings include the default branch and whether or not SSL related files are expected to exist.  
This command also takes an optional ```branch=``` parameter to override the default branch.
