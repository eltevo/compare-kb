Configuring quotas on Ubuntu

    # apt-get install quota quotatool
    
Mount disk image on loopback

    # mount img.fs /mnt/img -t auto -o usrquota,grpquota,acl,loop=3
    
Create quota files

    # touch /mnt/img/quota.user /mnt/img/quota.group
    # chmod 600 /quota.*
    # mount -o remount /mnt/img
    # quotacheck -avugm
    # quotaon -avug