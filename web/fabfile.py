from fabric.api import env
from fabric_utils.deploy import deploy, deploy_global_config, shutdown
from fabric_utils.setup import add_authorized_key, disable_ssh_passwords, setup_deployment, setup_server, setup_user
import newdjangosite

env.use_ssh_config = True  # This makes it easier to use key based authentication
