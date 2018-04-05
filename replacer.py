from argparse import ArgumentParser
from os import rename, walk
from os.path import join, splitext

PLACEHOLDER_VARIABLE = 'newdjangosite'
PLACEHOLDER_TITLE = 'NewDjangoSite'
PLACEHOLDER_DOMAIN = 'yourdomain.tld'
PLACEHOLDER_GITHUB_REPO = 'GitHubUser/GitHubRepo'

EXCLUDED_DIRECTORIES = ['.git', '.idea', 'venv']
EXCLUDED_FILES = ['replacer.py']
EXCLUDED_EXTENSIONS = ['.pyc']


def replace(file_path, site_variable, site_title, site_domain, github_repo):
    modified = False

    with open(file_path, 'rb') as file_handle:
        contents = file_handle.read()

    if bytearray(PLACEHOLDER_VARIABLE, 'utf-8') in contents:
        contents = contents.replace(bytearray(PLACEHOLDER_VARIABLE, 'utf-8'), bytearray(site_variable, 'utf-8'))
        modified = True

    if bytearray(PLACEHOLDER_TITLE, 'utf-8') in contents:
        contents = contents.replace(bytearray(PLACEHOLDER_TITLE, 'utf-8'), bytearray(site_title, 'utf-8'))
        modified = True

    if bytearray(PLACEHOLDER_DOMAIN, 'utf-8') in contents:
        contents = contents.replace(bytearray(PLACEHOLDER_DOMAIN, 'utf-8'), bytearray(site_domain, 'utf-8'))
        modified = True

    if bytearray(PLACEHOLDER_GITHUB_REPO, 'utf-8') in contents:
        contents = contents.replace(bytearray(PLACEHOLDER_GITHUB_REPO, 'utf-8'), bytearray(github_repo, 'utf-8'))
        modified = True

    if modified:
        with open(file_path, 'wb') as file_handle:
            file_handle.write(contents)
        print('Updated {0}'.format(file_path))
    else:
        print('No changes to {0}'.format(file_path))


def replace_in_files(site_variable, site_title, site_domain, github_repo):
    for root, dirs, files in walk('.'):

        # First, make sure we don't touch anything in excluded directories
        for excluded in EXCLUDED_DIRECTORIES:
            if excluded in dirs:
                dirs.remove(excluded)
                print('Skipping {0}'.format(join(root, excluded)))

        for name in files:
            # Make sure we don't want to skip this file because of its name or extension
            if name in EXCLUDED_FILES:
                print('Skipping {0}'.format(join(root, name)))
                continue
            if splitext(name)[1] in EXCLUDED_EXTENSIONS:
                print('Skipping {0}'.format(join(root, name)))
                continue

            # Rename the file if PLACEHOLDER_VARIABLE or PLACEHOLDER_DOMAIN is in the file name
            if PLACEHOLDER_VARIABLE in name:
                old_path = join(root, name)
                new_name = name.replace(PLACEHOLDER_VARIABLE, site_variable)
                full_path = join(root, new_name)
                rename(old_path, full_path)
                print('Renaming {0} to {1}'.format(old_path, full_path))
            elif PLACEHOLDER_DOMAIN in name:
                old_path = join(root, name)
                new_name = name.replace(PLACEHOLDER_DOMAIN, site_domain)
                full_path = join(root, new_name)
                rename(old_path, full_path)
                print('Renaming {0} to {1}'.format(old_path, full_path))
            else:
                full_path = join(root, name)

            # Find and replace anything in the contents of the file
            replace(full_path, site_variable, site_title, site_domain, github_repo)


if __name__ == "__main__":
    print('Enter the name of the site in a form suitable for a variable. This should consist of only lowercase characters (e.g., mydjangosite)')
    site_variable = input('Site Variable: ')

    print('\nEnter the name of the site in your preferred human-readable form. This can contain mixed case, spaces, symbols, etc. (e.g., My Django Site)')
    site_title = input('Site Title: ')
    
    print('\nEnter the domain for your site. This should omit "www." (e.g., example.com)')
    site_domain = input('Site Domain: ')

    print('\nEnter the GitHub repo this site will be deployed from. It should be of the form GitHubUser/GitHubRepo')
    github_repo = input('GitHub repo: ')

    print('\nEnter the name of the owner of this site. This name will appear in the copyright information for this site')
    owner = input('Owner: ')

    print('\nEnter the email address for the owner. Django will email failures to this address, but it won''t be visible on the site)')
    email = input('Email: ')

    print('\nRenaming web/{0} to web/{1}'.format(PLACEHOLDER_VARIABLE, site_variable))
    rename('web/{0}'.format(PLACEHOLDER_VARIABLE), 'web/{0}'.format(site_variable))
    replace_in_files(site_variable, site_title, site_domain, github_repo)

