# wrapping git

Gitlab-shell gives ssh access to git but it requires public key authentication 
which is tricky to get working from code. The gitpython documentation doesn't say
much about the problems.

From git 2.5 up, it is possible to set the GIT_SSH_COMMAND env variable to
provide the exact ssh command that git will use to connect to the server.
(Earlier versions could only use a custom executable from the GIT_SSH evn var.)
Git will automatically add the repo name to the end of the ssh command so it
should look something like (in case a non-standard ssh port is used):

    /usr/bin/git -i "keyfile" -p 23
    
From gitpython, typicall a 'with' environment is used to set env vars:

    g = Git()
    with g.custom_environment(GIT_SSH_COMMAND=cmd):
        # do git magic here
        
However, this doesn't work when cloning repose where the trick is to pass
the env vars to the function itself:

    repo = git.Repo.clone_from(url, dir, env=dict(GIT_SSH_COMMAND=cmd))
    
Older ubuntu provides git 1.9 so a new apt repo needs to be added to install
newer version:

    # sudo apt-get install software-properties-common python-software-properties
    # sudo add-apt-repository ppa:git-core/ppa
    # apt-get update
    # apt-get install git --upgrade