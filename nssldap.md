# LDAP authentication with PAM

This doesn't cover Kerberos, just simple LDAP authentication.

## Install necessary package

    # apt-get install libnss-ldapd

This will configure the scripts under /etc/pam.d/ automatically, but need to set up ldap server in /etc/nslcd.conf:

=======================================
    uid nslcd
    gid nslcd

    uri ldap://compare-ldap/
    base dc=compare,dc=vo,dc=elte,dc=hu
    binddn cn=admin,dc=compare,dc=vo,dc=elte,dc=hu
    bindpw almafa137
=======================================

And add ldap to nsswitch.conf, but it should be added automatically when the libnss-ldapd package is installed.

=======================================
    passwd:         ldap compat
    group:          ldap compat
    shadow:         ldap compat
    gshadow:        files

    hosts:          files dns
    networks:       files

    protocols:      db files
    services:       db files
    ethers:         db files
    rpc:            db files

    netgroup:       nis
=======================================