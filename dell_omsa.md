# Dell OpenManages Server Administrator (OMSA)

## Install from Docker image

    # docker run --privileged -d -p 1311:1311 --restart=always \
        --net=host -v /lib/modules/`uname -r`:/lib/modules/`uname -r` \
        --name=omsa82 jdelaros1/openmanage

# Install Dell Open Manage
---------------------------

http://linux.dell.com/repo/community/ubuntu/

    $ sudo echo 'deb http://linux.dell.com/repo/community/ubuntu precise openmanage' | sudo tee -a /etc/apt/sources.list.d/linux.dell.com.sources.list 

replace precise with trusty etc.

    $ sudo apt-get update
    $ sudo apt-get install srvadmin-all

Add users to /opt/dell/srvadmin/etc/omarolemap 

    john_doe     *     Administrator

IMPORTANT:

There's a bug in OMSA that logs you into the wrong role, even though you're and admin.
Fix this by 

    $ sudo chmod 0640 /opt/dell/srvadmin/etc/omarolemap

Without being admin you can't manage virtual disks etc.

Start services

    $ sudo service dsm_om_connsvc start
    $ sudo service dataeng start

Visit https://<ip_address>:1311/ for admin interface

Setup service to run at boot

    $ sudo update-rc.d dsm_om_connsvc defaults

Update iptable to grant access to OMSA from local subnet

    $ sudo iptable -I INPUT 1 -s 157.181.172.0/8 -p tcp --dport 1311 -j ACCEPT
