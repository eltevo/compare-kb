# Creating a Virtual Filesystem where acl and quota are switched on

This description is based on the following links:
https://thelinuxexperiment.com/create-a-virtual-hard-drive-volume-within-a-file-in-linux/
http://linuxgazette.net/109/chirico.html
http://stackoverflow.com/a/8148831
http://www.tecmint.com/set-access-control-lists-acls-and-disk-quotas-for-users-groups/

## Step 0 - Preparing
    # sudo apt install quota
    # mkdir -p /var/diskimg
## Step 1 - Creating an 100GB regular file (as a disk image) with all zeros:
    # dd if=/dev/zero of=/var/diskimg/virtfs.img bs=1M count=100000
Comment: dd uses a block size of 512 bytes by default and we can change to 1M.
## Step 2 - Formating the previous file as an ext4 filesystem:
    # mkfs -t ext4 /var/diskimg/virtfs.img
## Step 3 - Mounting this filesystem to /srv via loop device, setting up acl and quota:
    # mount /var/diskimg/virtfs.img /srv -t auto -o usrquota,grpquota,acl,loop=/dev/loop3
## Step 4 - Switching on quota for users and groups:
    # quotacheck -mcuvgf /srv
    # quotaon -vu /srv
    # quotaon -vg /srv
Comment: the quotacheck scans a filesystem for disk usage, create, check and repair quota files.
(The switch -f forces checking and writing of new quota files on filesystems with quotas enabled.)
## Step 5 - Setting quota to 10G for a user (with $uid)
    # setquota -u $uid 10G 10G 0 0 /dev/loop3
Comment: the format (after $uid) is block-softlimit block-hardlimit inode-softlimit inode-hardlimit.
To disable a quota, set the corresponding parameter to 0.
