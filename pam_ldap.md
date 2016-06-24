# PAM with LDAP

https://arthurdejong.org/nss-pam-ldapd/setup

Necessary packages:

    # apt-get install libnss-ldapd openldap-utils ldap-client libldap2-dev 

To get the config right, ubuntu has pam-auth-update that generates a working PAM config based on the installed packages.

    # sudo pam-auth-update --force
