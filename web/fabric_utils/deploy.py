from fabric.api import cd, run, settings, sudo

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


def deploy(config):
    configuration = configurations[config]
    branch = configuration['branch']
    use_ssl = configuration['ssl']

    PYTHON_DIR = '/var/www/python'
    repo_dir = '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)
    web_dir = '{0}/web'.format(repo_dir)
    config_dir = '{0}/config/ubuntu-14.04'.format(repo_dir)
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
        sudo('chgrp -R webadmin .')
        sudo('chmod -R ug+w .')
        run('git fetch origin')
        # Attempt to checkout the target branch. This might fail if we've
        # never deployed from this branch before in this deployment. In that case,
        # just create the branch then try again.
        with settings(warn_only=True):
            result = sudo('git checkout {0}'.format(branch))
        if result.failed:
            sudo('git branch {0}'.format(branch))
            sudo('git checkout {0}'.format(branch))

        sudo('git reset --hard origin/{0}'.format(branch))


def _compile_source(config, repo_dir, web_dir, virtualenv_python):
    with cd(repo_dir):
        sudo('venv/bin/pip install --requirement=requirements.txt')

    with cd(web_dir):
        sudo('find . -iname "*.pyc" -exec rm {} \;')
        sudo('{0} -m compileall .'.format(virtualenv_python))
        sudo('{0} manage_{1}.py collectstatic --noinput'.format(virtualenv_python, config))


def _update_scripts(config, daily_scripts_dir):
    CRON_DAILY_DIR = '/etc/cron.daily'
    with cd(daily_scripts_dir):
        sudo('cp newdjangosite-{0}-* {1}'.format(config, CRON_DAILY_DIR))

    with cd(CRON_DAILY_DIR):
        sudo('chmod 755 newdjangosite-{0}-*'.format(config))


def _update_database(config, web_dir, virtualenv_python):
    with cd(web_dir):
        sudo('{0} manage_{1}.py migrate'.format(virtualenv_python, config))


def _reload_code(config, uwsgi_dir):
    with cd(uwsgi_dir):
        sudo('cp newdjangosite-{0}.ini /etc/uwsgi/apps-enabled'.format(config))
        sudo('chmod 755 /etc/uwsgi/apps-enabled/newdjangosite-{0}.ini'.format(config))
        sudo('/etc/init.d/uwsgi start newdjangosite-{0}'.format(config))
        sudo('/etc/init.d/uwsgi reload newdjangosite-{0}'.format(config))

def _reload_web(config, nginx_dir, ssl):
    with cd(nginx_dir):
        sudo('cp {0}-newdjangosite-com /etc/nginx/sites-enabled/'.format(config))
        if ssl:
            sudo('cp ssl/{0}.newdjangosite.com.* /etc/nginx/ssl'.format(config))
            sudo('chown root /etc/nginx/ssl/{0}.newdjangosite.com.*'.format(config))
            sudo('chgrp root /etc/nginx/ssl/{0}.newdjangosite.com.*'.format(config))
            sudo('chmod 644 /etc/nginx/ssl/{0}.newdjangosite.com.*'.format(config))

        sudo('/etc/init.d/nginx reload')


def _run_tests(config, web_dir, virtualenv_python):
    with cd(web_dir):
        run('{0} manage_{1}.py test'.format(virtualenv_python, config))


def deploy_global_config(config):
    global_dir = '/var/www/python/newdjangosite-{0}/config/ubuntu-14.04/global'.format(config)
    SHARED_MEM = '/etc/sysctl.d/30-postgresql-shm.conf'
    NGINX_CONF = '/etc/nginx/nginx.conf'
    POSTGRES_HBA = '/etc/postgresql/9.3/main/pg_hba.conf'
    POSTGRES_CONF = '/etc/postgresql/9.3/main/postgresql.conf'

    with cd(global_dir):
        sudo('cp 30-postgresql-shm.conf {0}'.format(SHARED_MEM))
        _update_permissions(SHARED_MEM, 'root', 'root', '644')

        sudo('cp nginx.conf {0}'.format(NGINX_CONF))
        _update_permissions(NGINX_CONF, 'root', 'root', '644')

        sudo('cp pg_hba.conf {0}'.format(POSTGRES_HBA))
        _update_permissions(POSTGRES_HBA, 'postgres', 'postgres', '640')

        sudo('cp postgresql.conf {0}'.format(POSTGRES_CONF))
        _update_permissions(POSTGRES_HBA, 'postgres', 'postgres', '644')

    sudo('/etc/init.d/nginx restart')
    sudo('/etc/init.d/postgresql restart')


def _update_permissions(path, owner, group, mode):
    sudo('chown {0}:{1} {2}'.format(owner, group, path))
    sudo('chmod {0} {1}'.format(mode, path))


def shutdown(config):
    configuration = configurations[config]
    branch = configuration['branch']
    use_ssl = configuration['ssl']

    PYTHON_DIR = '/var/www/python'
    repo_dir = '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)
    nginx_dir = '{0}/config/ubuntu-14.04/nginx/shutdown'.format(repo_dir)

    _update_source(repo_dir, branch)
    _reload_web(config, nginx_dir, use_ssl)
