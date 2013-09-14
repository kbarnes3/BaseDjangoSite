from fabric.api import sudo


def setup_server():
    packages = [
        'git',
        'python-virtualenv',
        'mercurial',
        'python-psycopg2',
        'postgresql',
        'python-flup',
        'nginx'
    ]

    for package in packages:
        sudo('apt-get install --yes {0}'.format(package))
