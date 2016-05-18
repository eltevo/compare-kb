JupyterHub without docker and apache

1. Install JupyterHUB
---------------------

https://github.com/jupyterhub/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges
```
pip3 install jupyterhub
```
2. If running under privileged account
--------------------------------------

Create privileged user, add to sudoers, allow shadow file access
```
useradd jupyterhub
usermod -a -G shadow jupyterhub

visudo
```
===================================================
# the command(s) the Hub can run on behalf of the above users without needing a password
# the exact path may differ, depending on how sudospawner was installed
Cmnd_Alias JUPYTER_CMD = /usr/local/bin/sudospawner

# actually give the Hub user permission to run the above command on behalf
# of the above users without prompting for a password
rhea ALL=(%lxjupyter) NOPASSWD:JUPYTER_CMD
====================================================

Test it from an account member of lxjupyter without

$ sudo -u jupyter sudo -n -u $USER sudospawner --help

etc.

3. Create config files JupyterHub
-----------------------

Create dir for public conf and secrets

# mkdir -p /srv/jupyterhub
# chown jupyterhub /srv/jupyterhub		# only if using privileged account
# chmod 0700 /srv/jupyterhub

Create keys to be used with the web interface

http://www.akadia.com/services/ssh_test_certificate.html

Private key:

# openssl genrsa -des3 -out /srv/jupyterhub/jupyterhub.key 1024

Cert request:

# openssl req -new -key /srv/jupyterhub/jupyterhub.key -out /srv/jupyterhub/jupyterhub.csr

Remove Passphrase from Key:

# cp /srv/jupyterhub/jupyterhub.key /srv/jupyterhub/jupyterhub.key.orig
# openssl rsa -in /srv/jupyterhub/jupyterhub.key.orig -out /srv/jupyterhub/jupyterhub.key 

Make sure these are readable by the jupyterhub account only.

Generating a Self-Signed Certificate:

# openssl x509 -req -days 365 -in /srv/jupyterhub/jupyterhub.csr -signkey /srv/jupyterhub/jupyterhub.key -out /srv/jupyterhub/jupyterhub.crt

Generate a secret for session cookies:

# openssl rand -base64 2048 > /srv/jupyterhub/jupyterhub_cookie_secret

4. Configure
------------

https://jupyterhub.readthedocs.io/en/latest/getting-started.html

# mkdir -p /etc/jupyterhub
# cd /etc/jupyterhub
# chown jupyterhub .
# jupyterhub --generate-config

Edit the newly created config file, note the valid python syntax (indents)

===================================================================
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'
c.JupyterHub.hub_ip = '157.181.172.120'
c.JupyterHub.hub_port = 8081
c.JupyterHub.ip = '157.181.172.120'
c.JupyterHub.port = 8000
c.JupyterHub.ssl_cert = '/srv/jupyterhub/jupyterhub.crt'
c.JupyterHub.ssl_key = '/srv/jupyterhub/jupyterhub.key'

# allow full file system access
c.Spawner.default_url = '/tree/home/%U'
c.Spawner.notebook_dir = '/'
c.Spawner.env_keep = ['PATH', 'PYTHONPATH', 'CONDA_ROOT', 'CONDA_DEFAULT_ENV', 'VIRTUAL_ENV', 'LANG', 'LC_ALL']
c.Spawner.environment = {
"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda-7.5/bin:/usr/local/cuda-7.5/lib64:/usr/local/cuda-7.5/include",
"LD_LIBRARY_PATH": "/usr/local/cuda-7.5/lib64" }
===================================================================

Add public port to iptables (not hub port!)

# iptables -I INPUT 3 -p tcp --dport 8000 -j ACCEPT

5. Run as service under root

https://github.com/jupyterhub/jupyterhub/wiki/Run-jupyterhub-as-a-system-service

6. Jupyterhub with PAM

It should work out of the box but to initialize the environment a PAM hook similar
to sshd or login can be created.

In jupyterhub_configure.cfg:

c.PAMAuthenticator.open_sessions = True
c.PAMAuthenticator.service = 'jupyter'

Then cp /etc/pam.d/sshd /etc/pam.d/jupyter

7. Debugging

In the config, set c.JupyterHub.extra_log_file = '/var/log/jupyterhub.log'
