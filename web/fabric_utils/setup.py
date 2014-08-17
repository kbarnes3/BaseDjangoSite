from importlib import import_module
from fabric.api import cd, run, sudo
from deploy import deploy


def setup_server(setup_wins=''):
    base_packages = [
        'git',
        'python-virtualenv',
        'mercurial',
        'python-psycopg2',
        'postgresql',
        'nginx',
        'uwsgi',
        'uwsgi-plugin-python',
    ]

    _install_packages(base_packages)

    username = run('echo $USER')

    sudo('addgroup webadmin')
    sudo('adduser {0} webadmin'.format(username))

    sudo('mkdir /var/www')
    sudo('mkdir /var/www/python')
    sudo('chgrp -R webadmin /var/www')
    sudo('chmod -R ug+w /var/www')

    sudo('createuser -E -P -s {0}'.format(username), user='postgres')
    run('createuser -s root')

    sudo('mkdir /var/uwsgi')
    sudo('chmod 777 /var/uwsgi')
    sudo('rm /etc/nginx/sites-enabled/default')
    sudo('/etc/init.d/nginx start')

    if setup_wins:
        _setup_wins()


def _install_packages(packages):
    for package in packages:
        sudo('apt-get install --yes {0}'.format(package))


def _setup_wins():
    wins_packages = [
        'samba',
        'winbind',
    ]

    _install_packages(wins_packages)
    sudo('sed -i s/\'hosts:.*/hosts:          files dns wins/\' /etc/nsswitch.conf')


def setup_deployment(config, repo):
    settings = import_module('newdjangosite.settings_{0}'.format(config))
    db_settings = settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    PYTHON_DIR = '/var/www/python'
    repo_dir = '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)

    run('createdb --encoding=UTF8 --locale=en_US.UTF-8 --owner=postgres --template=template0 {0}'.format(db_name))
    run('createuser -d -R -S {0}'.format(db_user))
    run('psql -d postgres -c \"ALTER ROLE {0} WITH ENCRYPTED PASSWORD \'{1}\';\"'.format(db_user, db_password))

    with cd(PYTHON_DIR):
        run('git clone {0} newdjangosite-{1}'.format(repo, config))

    with cd(repo_dir):
        run('virtualenv --system-site-packages venv')

    deploy(config)

    with cd(repo_dir):
        run('venv/bin/python web/manage_{0}.py createsuperuser'.format(config))
