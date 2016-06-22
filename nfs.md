# Cofiguring and NFS server using docker image

Since the nfs server is a kernel module, the *host* must have the necessary packages for any docker to run an nfs server:

    # apt-get install nfs-server

Then simply

    #  docker run -d --name compare-nfs --net testnet --privileged -v /data/data1/compare/srv/nfs/home:/home cpuguy83/nfs-server /home

Once it is listening on the network, try to access it by mounting on the host

* https://help.ubuntu.com/community/SettingUpNFSHowTo

Install the NFS client

    # apt-get install nfs-common 
    # mkdir -p /data/data1/compare/tmp/mnt/home
    # mount -t nfs -o proto=tcp,port=2049 172.18.0.4:/home /data/data1/compare/tmp/mnt/home

