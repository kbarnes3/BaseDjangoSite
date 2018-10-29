from importlib import import_module
from fabric.api import env
from fabric.api import cd, run, settings, sudo
from fabric.contrib.files import exists
from .deploy import AllowedException, deploy, get_repo_dir, WEBADMIN_GROUP

env.use_ssh_config = True

REPO_FULL_NAME = 'GitHubUser/GitHubRepo'


def setup_user(user, no_sudo_passwd='', public_key_file=''):
    from plush.fabric_commands import prepare_user

    messages = prepare_user(user, WEBADMIN_GROUP, add_sudo=True, no_sudo_passwd=bool(no_sudo_passwd))
    add_authorized_key(user, public_key_file)

    if not exists('/usr/bin/createuser'):
        _install_packages(['postgresql'])

    matching_user_count = sudo("psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='{0}'\"".format(user),
                               user='postgres')
    if '1' not in matching_user_count:
        sudo('createuser -s {0}'.format(user), user='postgres')

    if messages:
        print("========================================")
        print(messages)
        print("========================================")


def add_authorized_key(user, public_key_file):
    import plush.fabric_commands
    if public_key_file:
        with open(public_key_file, 'r') as public_key:
            public_key_contents = public_key.read()
        plush.fabric_commands.add_authorized_key(user, public_key_contents)


def setup_server(setup_wins=''):
    from plush.fabric_commands.permissions import make_directory

    base_packages = [
        'git',
        'python3-venv',
        'postgresql',
        'python3-psycopg2',
        'nginx',
        'uwsgi',
        'uwsgi-plugin-python3',
    ]

    _install_packages(base_packages)

    if setup_wins:
        _setup_wins()

    sudo('mkdir -p /etc/nginx/ssl')
    make_directory(WEBADMIN_GROUP, '/var/www')
    make_directory(WEBADMIN_GROUP, '/var/www/python')

    with settings(abort_exception=AllowedException):
        try:
            run('createuser -s root')
        except AllowedException:
            pass

    make_directory('root', '/var/uwsgi', '777')

    default_site = '/etc/nginx/sites-enabled/default'
    if exists(default_site):
        sudo('rm {0}'.format(default_site))
    sudo('/etc/init.d/nginx start')


def _install_packages(packages):
    for package in packages:
        sudo('apt-get install --yes {0}'.format(package))


def _setup_wins():
    wins_packages = [
        'samba',
        'smbclient',
        'winbind',
    ]

    _install_packages(wins_packages)
    sudo('sed -i s/\'hosts:.*/hosts:          files dns wins/\' /etc/nsswitch.conf')


def setup_deployment(config):
    django_settings = import_module('newdjangosite.settings_{0}'.format(config))
    db_settings = django_settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    repo_dir = get_repo_dir(config)

    database_created = False
    with settings(abort_exception=AllowedException):
        try:
            run('createdb --encoding=UTF8 --locale=en_US.UTF-8 --owner=postgres --template=template0 {0}'.format(db_name))
            database_created = True
        except AllowedException:
            pass

    with settings(abort_exception=AllowedException):
        try:
            run('createuser -d -R -S {0}'.format(db_user))
        except AllowedException:
            pass

    run('psql -d postgres -c \"ALTER ROLE {0} WITH ENCRYPTED PASSWORD \'{1}\';\"'.format(db_user, db_password))

    _setup_repo(repo_dir)

    with cd(repo_dir):
        if not exists('venv'):
            run('python3 -m venv --system-site-packages venv')

    global_dir = '{0}/config/ubuntu-16.04/global'.format(repo_dir)
    with cd(global_dir):
        uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
        uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

        if not exists(uwsgi_socket):
            from plush.fabric_commands.permissions import set_permissions_file
            sudo('cp uwsgi-app@.socket {0}'.format(uwsgi_socket))
            set_permissions_file(uwsgi_socket, 'root', 'root', '644')

        if not exists(uwsgi_service):
            sudo('cp uwsgi-app@.service {0}'.format(uwsgi_service))
            set_permissions_file(uwsgi_service, 'root', 'root', '644')

    deploy(config)

    if database_created:
        with cd(repo_dir):
            run('venv/bin/python web/manage_{0}.py createsuperuser'.format(config))


def _setup_repo(repo_dir):
    from plush.fabric_commands.permissions import make_directory

    make_directory(WEBADMIN_GROUP, repo_dir)

    if not exists('{0}/.git'.format(repo_dir)):
        from plush.fabric_commands.git import clone
        from plush.fabric_commands.ssh_key import create_key
        from plush.oauth_flow import verify_access_token
        from plush.repo_keys import add_repo_key

        if not verify_access_token():
            raise Exception('Unable to access GitHub account')
        create_key(REPO_FULL_NAME, WEBADMIN_GROUP)
        add_repo_key(REPO_FULL_NAME)
        clone(REPO_FULL_NAME, repo_dir)

