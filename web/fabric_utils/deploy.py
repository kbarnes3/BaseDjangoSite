from fabric.api import cd, run, settings, sudo

configurations = {
    'daily': {
        'branch': 'master',
    },
    'dev': {
        'branch': 'master',
    },
    'prod': {
        'branch': 'prod',
    },
    'staging': {
        'branch': 'prod',
    },
}


def deploy(config):
    configuration = configurations[config]
    branch = configuration['branch']

    PYTHON_DIR = '/var/www/python'
    repo_dir = '{0}/newdjangosite-{1}'.format(PYTHON_DIR, config)
    web_dir = '{0}/web'.format(repo_dir)
    config_dir = '{0}/config/ubuntu-12.04'.format(repo_dir)
    daily_scripts_dir = '{0}/cron.daily'.format(config_dir)
    init_dir = '{0}/init.d'.format(config_dir)
    nginx_dir = '{0}/nginx'.format(config_dir)
    virtualenv_python = '{0}/venv/bin/python'.format(repo_dir)

    _update_source(config, repo_dir, web_dir, virtualenv_python, branch)
    _update_scripts(config, daily_scripts_dir)
    _update_database(config, web_dir, virtualenv_python)
    _reload_code(config, init_dir, nginx_dir)
    _run_tests(config, web_dir, virtualenv_python)


def _update_source(config, repo_dir, web_dir, virtualenv_python, branch):
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
        sudo('{0} manage_{1}.py syncdb'.format(virtualenv_python, config))
        sudo('{0} manage_{1}.py migrate'.format(virtualenv_python, config))


def _reload_code(config, init_dir, nginx_dir):
    with cd(init_dir):
        sudo('cp newdjangosite-{0} /etc/init.d'.format(config))
        sudo('chmod 755 /etc/init.d/newdjangosite-{0}'.format(config))
        sudo('update-rc.d newdjangosite-{0} defaults'.format(config))
        sudo('update-rc.d newdjangosite-{0} enable'.format(config))
        sudo('/etc/init.d/newdjangosite-{0} restart'.format(config))

    with cd(nginx_dir):
        sudo('cp {0}-newdjangosite-com /etc/nginx/sites-enabled/'.format(config))
        sudo('/etc/init.d/nginx reload')


def _run_tests(config, web_dir, virtualenv_python):
    with cd(web_dir):
        run('{0} manage_{1}.py test'.format(virtualenv_python, config))
