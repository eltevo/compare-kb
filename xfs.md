# XFS with project quota

Install and create xfs on image file:

    # apt-get install xfsprogs
    # mkfs -t xfs -f home.img
    
Mount with quota enabled (acl is turned on by default)
    
    # mount home.img home -t xfs -o prjquota,loop=/dev/loop3
    

    
    
