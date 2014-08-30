from argparse import ArgumentParser
from os import rename, walk
from os.path import join, splitext

PLACEHOLDER_VARIABLE = 'newdjangosite'
PLACEHOLDER_TITLE = 'NewDjangoSite'

EXCLUDED_DIRECTORIES = ['.git', '.idea', 'venv']
EXCLUDED_FILES = ['replacer.py']
EXCLUDED_EXTENSIONS = ['.pyc']


def replace(file_path, site_variable, site_title):
    modified = False

    with open(file_path, 'rb') as file_handle:
        contents = file_handle.read()

    if PLACEHOLDER_VARIABLE in contents:
        contents = contents.replace(PLACEHOLDER_VARIABLE, site_variable)
        modified = True

    if PLACEHOLDER_TITLE in contents:
        contents = contents.replace(PLACEHOLDER_TITLE, site_title)
        modified = True

    if modified:
        with open(file_path, 'wb') as file_handle:
            file_handle.write(contents)
        print('Updated {0}'.format(file_path))
    else:
        print('No changes to {0}'.format(file_path))


def replace_in_files(site_variable, site_title):
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

            # Rename the file if PLACEHOLDER_VARIABLE is in the file name
            if PLACEHOLDER_VARIABLE in name:
                old_path = join(root, name)
                new_name = name.replace(PLACEHOLDER_VARIABLE, site_variable)
                full_path = join(root, new_name)
                rename(old_path, full_path)
                print('Renaming {0} to {1}'.format(old_path, full_path))
            else:
                full_path = join(root, name)

            # Find and replace anything in the contents of the file
            replace(full_path, site_variable, site_title)


if __name__ == "__main__":
    parser = ArgumentParser(description='Injects your site''s name into the template to set up a new site')
    parser.add_argument('site_variable',
                        help='The name of the site in a form suitable for a variable. This should consist of only lowercase characters.')
    parser.add_argument('site_title',
                        help='The name of the site in your preferred human-readable form. This can contain mixed case, spaces, symbols, etc.')
    args = parser.parse_args()

    rename('web/{0}'.format(PLACEHOLDER_VARIABLE), 'web/{0}'.format(args.site_variable))
    print('Renaming web/{0} to web/{1}'.format(PLACEHOLDER_VARIABLE, args.site_variable))
    replace_in_files(args.site_variable, args.site_title)
