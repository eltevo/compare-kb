# Join server to windows domain
--------------------------------

Configure NTP

    # apt-get install ntp

edit /etc/ntp.conf if necessary

Setup samba

https://help.ubuntu.com/community/ActiveDirectoryWinbindHowto
https://raymii.org/s/tutorials/SAMBA_Share_with_Active_Directory_Login_on_Ubuntu_12.04.html

    # apt-get install samba winbind libnss-winbind libpam-winbind

/etc/samba/smb.conf should look like:

==============================================================
  # /etc/samba/smb.conf
  [global]
  
  # machine name and domain settings
  security=ADS
  realm=VO.ELTE.HU
  workgroup = VO
  netbios name=RETDB02
  auth methods=winbind
  
  # uid - sid mapping
  idmap config * : backend = rid
  idmap config * : range = 100000-500000
  
  # winbind config
  winbind enum users = yes
  winbind enum groups = yes
  winbind nested groups = no
  winbind expand groups = 4
  winbind use default domain = Yes
  winbind refresh tickets = Yes
  
  # user home directories
  template homedir = /home/%U
  template shell = /bin/bash
  ;  template primary group = @lxuser
  
  # authentication settings
  client use spnego = yes
  client ntlmv2 auth = no
  encrypt passwords = yes
  restrict anonymous = 2
  users = @lxadm @lxuser
  
  # kerberos settings
  kerberos method = secrets and keytab
  dedicated keytab file = /etc/krb5.keytab
  
  # global share settings
  read only=no
  unix extensions = no
  
  [data]
  path=/data
  valid users= @lxadm @lxuser
  writable=yes
  read only=no
  browseable = yes
  
  wide links=yes
  follow symlinks = yes
  unix extensions = no
==============================================================

winbind refresh tickets = yes will automatically refresh kerberos tickets
for long user sessions

template primary group will use lxuser instead of windows default "Domain Users" 
-- this is problematic... instead set g+s mode on directories, so that
the default group will be lxusers
users = ... will restrict samba access to the given groups

kerberos method = secret and keytab is necessary to have the machine account
password stored in a keytab file under /etc/krb5.keytab
  
This is how uid and gid mapping is done by winbind:
https://www.samba.org/samba/docs/man/manpages-3/idmap_rid.8.html

ID = RID - BASE_RID + LOW_RANGE_ID.
RID = ID + BASE_RID - LOW_RANGE_ID

# service winbind restart
# service samba restart

Install kerberos

# apt-get install krb5-user

Edit /etc/krb5.conf, setup VO.ELTE.HU domain with BLACKHOLE.VO.ELTE.HU


==================================================================
[libdefaults]
        default_realm = VO.ELTE.HU
[realms]
        VO.ELTE.HU = {
                kdc = blackhole.vo.elte.hu
                admin_server = blackhole.vo.elte.hu
                default_domain = vo.elte.hu
        }
        ELTE.HU = {
                kdc = kdc1.elte.hu
                kdc = kdc2.elte.hu
                admin_server = kdc1.elte.hu
        }
        krft = {
                kdc = complex.elte.hu
                admin_server = complex.elte.hu
        }
[domain_realm]
        vo.elte.hu = VO.ELTE.HU

==================================================================

Test kerberos

# kinit dobos

This should ask for a password for dobos@VO.ELTE.HU

# klist

Test your server status

# testparm -s

Server role should be ROLE_DOMAIN_MEMBER

Join the domain

# net ads join -U dobos

At this point you can navigate to \\RETDB02 from a windows machine and get prompted for a password

Try get user entry using getent

# getent passwd dobos

If you get the wrong UID, just flush

# net cache flush

Make sure the machine account exists and keytab is present

# klist -ke

The following should authenticate using the keytab

# kinit -k RETDB02$

To get a TGT for the machine account

# net ads kerberos kinit -P

5. Configure PAM to authenticate from domain
--------------------------------------------

Configure NSS, this is how passwd, hosts etc. are resolved. Winbind should be on
the list for passwd etc. to provide user data based on ADS.

==============================================================
# /etc/nsswitch.conf
#
# Example configuration of GNU Name Service Switch functionality.
# If you have the `glibc-doc-reference' and `info' packages installed, try:
# `info libc "Name Service Switch"' for information about this file.

passwd:         compat winbind
group:          compat winbind
shadow:         compat

hosts:          files wins dns
networks:       files

protocols:      db files
services:       db files
ethers:         db files
rpc:            db files

netgroup:       nis
==============================================================

Configure PAM, see
https://www.samba.org/samba/docs/man/Samba-HOWTO-Collection/winbind.html

Basically, just running pam-auth-update end enabling winbind will do.

# pam-auth-update

See if /lib/x86_64-linux-gnu/security/pam_winbind.so exists

Check /etc/pam.d/samba and its includes:

@include common-auth
@include common-account
@include common-session-noninteractive

make sure pam_winbind.so is in the lists

At this point you should be able to logon to linux using the windows account
but the home directory won't get mounted.

You can try to login with full domain account name: VO\dobos

Restrict login to users of the lxuser group

edit /etc/security/access.conf

==============================================================
+ : @adm : ALL
+ : @user : ALL
+ : @lxadm : ALL
+ : #lxuser : ALL

- : ALL : ALL
==============================================================

We need a kerberos ticket during login to be able to mount the home directory.

https://www.samba.org/samba/docs/man/manpages/pam_winbind.conf.5.html

Create /etc/security/pam_winbind.conf
You can copy /usr/share/doc/libpam-winbind/examples/pam_winbind/pam_winbind.conf

Important options:
- krb5_auth = yes
- krb5_ccache_type=FILE

To restrict users to a given group that can login using an active directory account,
add: require_membership_of = VO\lxuser

=======================================================================
# /etc/security/pam_winbind.conf

[global]

;debug = no
;debug_state = no
;cached_login = no
krb5_auth = yes
krb5_ccache_type = FILE
require_membership_of = VO\lxuser
warn_pwd_expire = 14
;silent = no
;mkhomedir = no

=======================================================================
