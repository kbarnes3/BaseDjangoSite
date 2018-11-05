BaseDjangoSite
==============

A basic template for a Django site and the framework to deploy it.

This project is intended to be copied and pasted into an empty repo as the basis of a new Django site. From there, developers are encouraged to modify and delete code to suit their needs. This project is intended to be comfortable to use for someone familiar with Django (or at least someone who has completed a Django tutorial project). As such, it tries to stay as close to a vanilla Django project as possible.

To get an idea of the intended developer work flows for projects based on this template, read Setup-Dev-Environment.md and Setup-Server-Environment.md.

Using BaseDjangoSite as your project template
---------------------------------------------
To start a new Django site based on this project, do the following steps

1. Create an empty Git repo and copy the contents of this repo into it. Alternatively, clone this repo to a new directory and then delete the .git folder.
1. Remove or update the following files to reflect your project: README.md and LICENSE.TXT
1. Ensure the latest release of Python 3.6 is installed on your computer
1. Run the "replacer.py" script to personalize the BaseDjangoSite template files. The script should be run with: ```py -3.6 replacer.py```
1. The script will prompt you for values such as your project domain, URL, and email address. The script will then edit and rename files based on the provided values.
1. Delete the replace.py file
1. Commit all the remaining files to Git.
1. From PowerShell, run ```scripts\Bootstrap.ps1 -Verbose``` followed by ```scripts\Ensure-Venv.ps1```
1. Run ```python secret_key.py``` and copy the output into the SECRET_KEY property in ```web\newdjangosite\settings_base.py```. Be sure to uncomment the property.
1. Follow the instructions in Setup-Dev-Environment.md to set up a local development environment.
1. Follow the instructions in Setup-Server-Environment.md to set up a server deployment.
