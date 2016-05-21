# Running OpenLDAP in a docker container

    https://hub.docker.com/r/dinkel/openldap/

Pull docker image from hub

    # docker pull dinkel/openldap

First of all, LDAP is very likely filtered on the network so it has to be configured on a non-stanard port. Also, volumes of the server needs to be mapped to local directories to allow data persistence between container restarts. Run the same image in the background, without the attached terminal:

    # mkdir /data/data1/compare/etc/ldap
    # mkdir /data/data1/compare/var/lib/ldap
    # docker run -d --net testnet -p 666:389 --name slapd -v /data/data1/compare/etc/ldap:/etc/ldap -v /data/data1/compare/var/lib/ldap:/var/lib/ldap -e SLAPD_PASSWORD=alma -e SLAPD_DOMAIN=compare.vo.elte.hu dinkel/openldap

Test is the service is listening on the internal network. The port should be in the state 'open'

    # nmap -p 666 172.18.0.2

Test the port from a remote host:

    # nmap -p 666 dockerhostname

Install JXplorer on your desktop and try to connect with

    user DN: cn=admin,dc=compare,dc=vo,dc=elte,dc=hu
    password: alma