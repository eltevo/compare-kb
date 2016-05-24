# Configure file systems for samba sharing
-------------------------------------------

* https://help.ubuntu.com/community/ActiveDirectoryWinbindHowto 
* https://wiki.samba.org/index.php/Idmap_config_rid
* https://www.samba.org/samba/docs/man/Samba-HOWTO-Collection/idmapper.html#id2606596
* https://technet.microsoft.com/en-us/magazine/2008.12.linux.aspx
 
Install packages acl, attr

## Create partitions on large disks, then mount:

    # mkdir -p /mnt/data0
    # mkdir -p /mnt/data1

edit fstab

==============================================================
    /dev/sdc1 /mnt/data0 ext4 defaults,acl,user_xattr,errors=remount-ro 0 0
    /dev/sdd1 /mnt/data1 ext4 defaults,acl,user_xattr,errors=remount-ro 0 0
==============================================================

It is important to disable fsck on the large volumes because checking them
can take days and prevent booting the system. (last 0 on the lines)

    # mount /mnt/data0
    # mount /mnt/data1

about ACLs, see https://help.ubuntu.com/community/UbuntuLTSP/ACLSupport

## Create samba shares
----------------------

Open additional ports in iptables

    # iptables -I INPUT 4 -s 157.181.0.0/16 -p udp --dport 137 -j ACCEPT
    # iptables -I INPUT 5 -s 157.181.0.0/16 -p udp --dport 138 -j ACCEPT
    # iptables -I INPUT 6 -s 157.181.0.0/16 -p tcp --dport 139 -j ACCEPT
    # iptables -I INPUT 7 -s 157.181.0.0/16 -p tcp --dport 445 -j ACCEPT

    # service iptables-persistent save

Create /data

Change group to domain users so everyone can access the share

    # chgrp -R "lxuser"

Add new block to /etc/samba/smb.conf

=======================================================================
    [data]
      path=/data
      valid users= @lxadm @lxuser
      writable=yes
      read only=no
      browseable = yes
    
      wide links=yes
      follow symlinks = yes
      unix extensions = no
=======================================================================

For some reason, symlinks under a samba share don't work, so mount fs directly
under /data.

Windows user primary group is "Domain users" so the following is required to
set group flag of files created on a samba share from windows:

    # setfacl -x g:"domain users" /data/data0
    # chgrp lxuser /data/data0
    # chmod g+s

This will turn on sticky groups.

## Permanently mount windows share
----------------------------------

Install cifs-utils

    # apt-get install cifs-utils

This is necessary to mount any windows shares. Test it first from command-line. Use the machine
account for authentication. Option multiuser will allow per-user access control.

Some distributions may have slightly broken packages of cifs-utils for which 
the symlink of idmap is missing:

    # Ubuntu 14, cifs-utils 2:6.0-1ubuntu2
    mkdir /etc/cifs-utils
    ln -s /usr/lib/x86_64-linux-gnu/cifs-utils/idmapwb.so /etc/cifs-utils/idmap-plugin


    # mount -t cifs //blackhole/users /home -osec=krb5,username=RETDB02$,multiuser,cifsacl,...

This should succeed if you have a valid krb5 ticket to the domain.
See cifs.mount man page for details on options.

This is how it looks like as an fstab entry. Not that a local krb5 keytab file with the
machine account secret is necessary for this to work because the system must have
a TGT to the kerberos server to mount the share.

//blackhole/users /home cifs sec=krb5,username=TESLA$,multiuser,nosetuids,noperm,nobrl,uid=cifsuser,gid=lxuser,file_mode=0666,dir_mode=0777 0 0

It is important to use the server name in DNS and it be the same as the host name of the
server. Aliases won't work.

nosetuids,noperm,nobrl are important for many linux programs to work
server will set file permissions on the windows side

Try getting original Windows ACL for a file

    $ getcifsacl test.txt

To debug problems, check out /var/log/auth.log

To enable setting the right owner and group permissions, a kernel upcall to
/etc/request-key.conf has to be added, according to
http://manpages.ubuntu.com/manpages/xenial/en/man8/cifs.idmap.8.html

=======================================================================
    #OPERATION  TYPE           D C PROGRAM ARG1 ARG2...
    #=========  =============  = = ================================
    create      cifs.idmap     * * /usr/sbin/cifs.idmap %k
=======================================================================

Now we set up automatic mounting of the share.

An alternative way to mount user directories is pam_mount:

Install libpam_mount package

    # apt-get install libpam-mount

Edit /etc/security/pam_mount.conf.xml 
