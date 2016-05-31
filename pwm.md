git clone https://github.com/pwm-project/pwm.git
apt-get install openjdk-7-jdk
apt-get install tomcat7


Install fresh maven to build java web service:

	# wget http://ppa.launchpad.net/natecarlson/maven3/ubuntu/pool/main/m/maven3/maven3_3.2.1-0~ppa1_all.deb
	# dpkg -i maven3_3.2.1-0~ppa1_all.deb

then in pwm directory

mvn3 clean install

This should create a war file in target

Copy war file next to Dockerfile, rename to pwm.war then build the docker image:

docker build -t pwm .

Shoot up image in a container then test with SSL:

 docker run --net testnet --name compare-pwm -d -v /data/data1/compare/srv/pwm/config:/config pwm

 curl -v -k https://172.18.0.6:8443/pwm/
 
## Preconfigure LDAP to work with pwm

LDAP config files can only be modified by cn=admin,cn=config.

The LDAP config should be under /srv/ldap/etc/slapd.d, it's a tree of LDIF files. To find who's the admin user, grep for olcRootDN:

	grep -r olcRootDN .

Need to add schema from pwm/supplemental/ldif/openldap.ldif

	ldapadd -H ldap://compare-ldap:389 -D cn=admin,cn=config -W -f openldap.ldif

Now need to add an access entry to allow users modify their own properties. First create LDIF with the following content:

	dn: olcDatabase={1}hdb,cn=config
	changetype: modify
	add: olcAccess
	olcAccess: {1}to attrs=pwmResponseSet by self write

Then execute

	$ ldapmodify -H ldap://172.18.0.2:389 -D cn=admin,cn=config -W -f pwm-access.ldif
	
You should then see the change in /etc/slapd.d/cn=config/olcDatabase=\{1\}hdb.ldif

Actually, the "to attrs=pwmResponseSet by self write" entry must appear with the index {1}, so manually editing the config file might be necessary.
 
## Configure pwm LDAP

1. Browse to http://compare.vo.elte.hu/pwm
2. Start manual configuration.
3. Set an admin password, you can use this in config mode to access the system. Once config mode is turned off, only LDAP users will be able to access the system again.
4. Access configuration edito menu from the top right drop down menu (v sign)
5. Set config options

	LDAP vendor: OpenLDAP
	Storage Default: LDAP
	
	LDAP URL: ldap://compare-ldap:389
	LDAP proxy user: cn=admin,dc=compare,dc=vo,dc=elte,dc=hu  (use entryDN here for bind)
	LDAP Contextless Login Roots: ou=users,dc=compare,dc=vo,dc=elte,dc=hu (DN for Users)
	LDAP Test User: uid=test,ou=users,dc=compare,dc=vo,dc=elte,dc=hu
	Auto Add Object Classes:
		pwmUser 
		simpleSecurityObject 
		organizationalPerson 
		person 
		top 
		inetOrgPerson 
		shadowAccount  
		posixAccount 
	Username Search Filter: (&(objectClass=person)(uid=%USERNAME%))
	Attribute to use for Username: uid
	
6. Save config and try to login with LDAP user.
7. Configure LDAP admin

Now make sure one of the LDAP users is an admin so you can login after configuration mode is switched off. Under Modules/Administration:

	LDAP profile: default
	LDAP Search filer: (&(objectClass=person)(uid=dobos))

When logging on now with the LDAP account, an new icon will be displayed.

## Allow users update their own LDAP nodes



## Configure pwm site settings

In configuration editor, under Settings/Application/Application/A

	Site URL: http://compare.vo.elte.hu/pwm
	Forward URL: http://compare.vo.elte.hu/
	Logout URL: http://compare.vo.elte.hu/
	Home URL: http://compare.vo.elte.hu/

Email settings are necessery for user self-registration:

Configure recaptcha for human detection at https://www.google.com/recaptcha/admin#list