from fabric.api import run, sudo


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
        pass
        sudo('apt-get install --yes {0}'.format(package))

    username = run('echo $USER')

    sudo('addgroup webadmin')
    sudo('adduser {0} webadmin'.format(username))

    sudo('mkdir /var/www')
    sudo('mkdir /var/www/python')
    sudo('chgrp -R webadmin /var/www')
    sudo('chmod -R ug+w /var/www')

    sudo('createuser -E -P -s {0}'.format(username), user='postgres')
    run('createuser -s root')

    sudo('mkdir /var/fastcgi')
    sudo('chmod 777 /var/fastcgi')
    sudo('rm /etc/nginx/sites-enabled/default')
    sudo('/etc/init.d/nginx start')
