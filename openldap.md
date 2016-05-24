# Running OpenLDAP in a docker container

    https://hub.docker.com/r/dinkel/openldap/

Pull docker image from hub

    # docker pull dinkel/openldap

First of all, LDAP is very likely filtered on the network so it has to be configured on a non-stanard port. Also, volumes of the server needs to be mapped to local directories to allow data persistence between container restarts. Run the same image in the background, without the attached terminal:

    # mkdir /data/data1/compare/srv/ldap/etc
    # mkdir /data/data1/compare/srv/ldap/var
    # docker run -d --net testnet -p 666:389 --name compare-ldap -v /data/data1/compare/srv/ldap/etc:/etc/ldap -v /data/data1/compare/srv/ldap/var:/var/lib/ldap -e SLAPD_PASSWORD=alma -e SLAPD_DOMAIN=compare.vo.elte.hu dinkel/openldap

Test is the service is listening on the internal network. The port should be in the state 'open'

    # nmap -p 666 172.18.0.2

Test the port from a remote host:

    # nmap -p 666 dockerhostname

Install JXplorer on your desktop and try to connect with

    user DN: cn=admin,dc=compare,dc=vo,dc=elte,dc=hu
    password: alma
	
	
	
	
http://www.tldp.org/HOWTO/archived/LDAP-Implementation-HOWTO/pamnss.html

From the command-line, LDAP can be accessed with tools from the package 'ldap-utils'. On the dev machines install with

    # apt-get install ldap-utils
	
# Configuring users in LDAP

https://gitlab.com/gitlab-org/cookbook-gitlab/blob/master/doc/open_LDAP.md

It is not necessary to change database indexing, as described at the link above. To create a users, however, the following LDIF template is to be used. The first part creates a group for users, the second part creates a new user.

* The second file is different what's on the gitlab web site. You need to add objectClass: simpleSecurityObject in order to be able to save a password.
* LDIF files must be encoded in UTF-8

users.ldif

	dn: ou=Users,dc=compare,dc=vo,dc=elte,dc=hu
	objectClass: organizationalUnit
	ou: Users


	dn: uid=jsmith,ou=Users,dc=compare,dc=vo,dc=elte,dc=hu
	objectClass: simpleSecurityObject
	objectClass: organizationalPerson
	objectClass: person
	objectClass: top
	objectClass: inetOrgPerson
	objectClass: posixAccount
	objectClass: shadowAccount
	uid: jsmith
	sn: Smith
	givenName: John
	cn: John Smith
	displayName: John Smith
	uidNumber: 10000
	gidNumber: 10000
	userPassword: test
	gecos: John Smith
	loginShell: /bin/bash
	homeDirectory: /profiles/jsmith
	mail: john.smith@example.com
	telephoneNumber: 000-000-0000
	st: NY
	manager: uid=jsmith,ou=Users,dc=gitlab,dc=dev
	shadowExpire: -1
	shadowFlag: 0
	shadowWarning: 7
	shadowMin: 8
	shadowMax: 999999
	shadowLastChange: 10877
	title: System Administrator

Verify you can log in with the following user DN:

    uid=jsmith,ou=Users,dc=compare,dc=vo,dc=elte,dc=hu