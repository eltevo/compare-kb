# install, start
apt install openafs-krb5 openafs-client
service openafs-client start

# authenticate
kinit stegerjozsef@ELTE.HU
aklog

# use
screen
cd /afs/elte.hu/org/atomcsill
