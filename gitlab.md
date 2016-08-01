# Installing gitlab in a docker image

    # docker pull gitlab/gitlab-ce

    # mkdir -p /data/data1/compare/srv/gitlab/etc
    # mkdir -p /data/data1/compare/srv/gitlab/log
    # mkdir -p /data/data1/compare/srv/gitlab/opt

    # docker run -d --name compare-gitlab -v /data/data1/compare/srv/gitlab/etc:/etc/gitlab -v /data/data1/compare/srv/gitlab/log:/var/log/gitlab -v /data/data1/compare/srv/gitlab/opt:/var/opt/gitlab  gitlab/gitlab-ce:latest

The full command looks like this

    # docker run --detach \
      --hostname gitlab.example.com \
      --publish 443:443 --publish 80:80 --publish 22:22 \
      --name gitlab \
      --restart always \
      --volume /data/data1/compare/etc/gitlab:/etc/gitlab \
      --volume /data/data1/compare/var/log/gitlab:/var/log/gitlab \
      --volume /data/data1/compare/var/opt/gitlab:/var/opt/gitlab \
      gitlab/gitlab-ce:latest
	  
Reconfigure external URL to be used with reverse proxy (nginx)

Edit /data/data1/compare/gitlab/etc/gitlab.rb

===============================================================
    external_url "http://compare.vo.elte.hu/gitlab"
    
    gitlab_rails['gitlab_email_from'] = 'dobos@complex.elte.hu'
    gitlab_rails['gitlab_email_display_name'] = 'Compare gitlab'
    gitlab_rails['gitlab_email_reply_to'] = 'noreply@complex.elte.hu'
    
    gitlab_rails['smtp_enable'] = true
    gitlab_rails['smtp_address'] = "mail.elte.hu"
===============================================================

At the beginning the server will report to be busy due to some initialization task. After about 30 sec it will become available, so don't worry about the 502 when you try to access it right after the docker container was launched. It you see the gitlab logo, you're fine.

When connection for the very first time, gitlab will ask for a root password.

# Configure OpenLDAP with gitlab

    https://gitlab.com/gitlab-org/cookbook-gitlab/blob/master/doc/open_LDAP.md
    https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/README.md#setting-up-ldap-sign-in

Users are authenticated from LDAP, however:

* when users register on the gitlab page, they don't get into LDAP
* when a gitlab user is deleted by an admin, it doesn't get deleted from LDAP
* users can't change password on the gitlab site
* LDAP groups are supported in the Enterprise Edition only

    https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/administration/auth/ldap.md
	
# Gitlab API

Authenticate user and get a session token:

    $ curl -X POST "http://172.20.0.4/gitlab/api/v3/session?login=root&password=Almafa137"


# Administering Gitlab via its consoles

## Gitlab dbconsole

    # docker exec -it compare-gitlab bash
	# gitlab-rails dbconsole
	> SELECT username FROM users;

## Gitlab ruby console

    # docker exec -it compare-gitlab bash
	# gitlab-rails console
	> User.find("test")

Adding a new user with ldap identity

	u = User.new
	u.name = "Test Testing"
	u.username = "test"
	u.password = "almafa137"
	u.email = "dobos@complex.elte.hu"
	u.confirmed_at = Time.now
	u.confirmation_token = nil
	u.save!

	i = Identity.new
	i.provider = "ldapmain"
	i.extern_uid = "uid=test,ou=users,dc=compare,dc=vo,dc=elte,dc=hu"
	i.user = u
	i.user_id = u.id
	i.save!

# Accessing gitlab with SSH

Make sure that key permission are restrictive enough, otherwise sshd will not start inside the container:

    # chmod 600 /srv/kooplex/compare/gitlab/etc/ssh_host_*
    
Which corresponds to

    # chmod 600 /etc/gitlab/ssh_host_*
    
when executed from inside the container.

To run git non-interactively and authenticate with a key

* remove password from the keyfile

    $ ssk-keygen -p -f keyfile

* trust the server key - the easiest is to start an ssh session from a terminal and answer yes, but it's manual. Need to find an automatic way.

The gitlab-shell might not be configured correctly. Check these:

* /etc/passwd has /bin/sh as the default command for the user 'git'
* /etc/pam.d/sshd has the following entry:

    session    optional     pam_loginuid.so
    
This second option is required if git reports a protocol error. That means that the server is responding with a
generic welcome message instead of executing the requested program.

instead of the default

    session    required     pam_loginuid.so
    
* git needs to be called with a tricky env variable to use an SSH key to connect to the server:

    $ GIT_SSH_COMMAND="ssh -v -i '/srv/kooplex/compare/home/test/.ssh/gitlab.key' -p 23" git clone ssh://git@pollux-ubuntu:/test/alma.git test
    
the ssh command will be executed and git will add the user@server part (sometimes the port) and the commands executed. If you get a disallowed command or similar, always check the verbose output of ssh -v in a terminal, it will print the command that could not be executed.

# Rendnering notebooks on gitlab
This [link](https://gist.github.com/martijnvermaat/6926070) contains some configurtion options enabling gitlab to rendner jupyter notebook.

