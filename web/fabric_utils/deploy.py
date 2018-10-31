from fabric.api import cd, run, sudo
from plush.fabric_commands.permissions import set_permissions_directory

configurations = {
    'daily': {
        'branch': 'master',
        'ssl': False,
    },
    'dev': {
        'branch': 'master',
        'ssl': False,
    },
    'prod': {
        'branch': 'prod',
        'ssl': False,
    },
    'staging': {
        'branch': 'prod',
        'ssl': False,
    },
}

PYTHON_DIR = '/var/www/python'
WEBADMIN_GROUP = 'webadmin'


class AllowedException(Exception):
    pass


def get_repo_dir(config):
    return '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)


def deploy(config, branch=''):
    configuration = configurations[config]
    if not branch:
        branch = configuration['branch']
    use_ssl = configuration['ssl']

    repo_dir = get_repo_dir(config)
    web_dir = '{0}/web'.format(repo_dir)
    config_dir = '{0}/config/ubuntu-18.04'.format(repo_dir)
    daily_scripts_dir = '{0}/cron.daily'.format(config_dir)
    uwsgi_dir = '{0}/uwsgi'.format(config_dir)
    nginx_dir = '{0}/nginx'.format(config_dir)
    virtualenv_python = '{0}/venv/bin/python'.format(repo_dir)

    _update_source(repo_dir, branch)
    _compile_source(config, repo_dir, web_dir, virtualenv_python)
    _update_scripts(config, daily_scripts_dir)
    _update_database(config, web_dir, virtualenv_python)
    _reload_code(config, uwsgi_dir)
    _reload_web(config, nginx_dir, use_ssl)
    _run_tests(config, web_dir, virtualenv_python)


def _update_source(repo_dir, branch):
    with cd(repo_dir):
        set_permissions_directory(repo_dir, WEBADMIN_GROUP, mod='ug+w')
        sudo('git fetch origin')
        sudo('git reset --hard origin/{0}'.format(branch))


def _compile_source(config, repo_dir, web_dir, virtualenv_python):
    with cd(repo_dir):
        run('venv/bin/pip install --quiet --requirement=requirements.txt')

    with cd(web_dir):
        sudo('find . -iname "*.pyc" -exec rm {} \;')
        sudo('{0} -m compileall .'.format(virtualenv_python))
        sudo('{0} manage_{1}.py collectstatic --noinput'.format(virtualenv_python, config))


def _update_scripts(config, daily_scripts_dir):
    cron_daily_dir = '/etc/cron.daily'
    with cd(daily_scripts_dir):
        sudo('cp newdjangosite-{0}-* {1}'.format(config, cron_daily_dir))

    with cd(cron_daily_dir):
        sudo('chmod 755 newdjangosite-{0}-*'.format(config))


def _update_database(config, web_dir, virtualenv_python):
    with cd(web_dir):
        sudo('{0} manage_{1}.py migrate'.format(virtualenv_python, config))


def _reload_code(config, uwsgi_dir):
    with cd(uwsgi_dir):
        sudo('cp newdjangosite-{0}.ini /etc/uwsgi/apps-available'.format(config))
        sudo('chmod 644 /etc/uwsgi/apps-available/newdjangosite-{0}.ini'.format(config))
        sudo('systemctl enable uwsgi-app@newdjangosite-{0}.socket'.format(config))
        sudo('systemctl enable uwsgi-app@newdjangosite-{0}.service'.format(config))
        sudo('systemctl start uwsgi-app@newdjangosite-{0}.socket'.format(config))
        sudo('touch /var/run/uwsgi/newdjangosite-{0}.reload'.format(config))


def _reload_web(config, nginx_dir, ssl):
    with cd(nginx_dir):
        sudo('cp {0}.yourdomain.tld /etc/nginx/sites-enabled/'.format(config))
        if ssl:
            sudo('cp ssl/{0}.yourdomain.tld.* /etc/nginx/ssl'.format(config))
            sudo('chown root /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))
            sudo('chgrp root /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))
            sudo('chmod 644 /etc/nginx/ssl/{0}.yourdomain.tld.*'.format(config))

        sudo('/etc/init.d/nginx reload')


def _run_tests(config, web_dir, virtualenv_python):
    with cd(web_dir):
        run('{0} manage_{1}.py test'.format(virtualenv_python, config))


def deploy_global_config(config):
    from plush.fabric_commands.permissions import set_permissions_file
    repo_dir = get_repo_dir(config)
    global_dir = '{0}/config/ubuntu-18.04/global'.format(repo_dir)
    nginx_conf = '/etc/nginx/nginx.conf'
    uwsgi_socket = '/etc/systemd/system/uwsgi-app@.socket'
    uwsgi_service = '/etc/systemd/system/uwsgi-app@.service'

    with cd(global_dir):
        sudo('git fetch origin')
        sudo('git reset --hard origin/master')

        sudo('cp nginx.conf {0}'.format(nginx_conf))
        set_permissions_file(nginx_conf, 'root', 'root', '644')

        sudo('cp uwsgi-app@.socket {0}'.format(uwsgi_socket))
        set_permissions_file(uwsgi_socket, 'root', 'root', '644')

        sudo('cp uwsgi-app@.service {0}'.format(uwsgi_service))
        set_permissions_file(uwsgi_service, 'root', 'root', '644')

    sudo('/etc/init.d/nginx restart')


def shutdown(config, branch=''):
    configuration = configurations[config]
    if not branch:
        branch = configuration['branch']
    use_ssl = configuration['ssl']

    repo_dir = get_repo_dir(config)
    nginx_dir = '{0}/config/ubuntu-18.04/nginx/shutdown'.format(repo_dir)

    _update_source(repo_dir, branch)
    _reload_web(config, nginx_dir, use_ssl)
