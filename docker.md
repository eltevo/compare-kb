# Docker install on ubuntu

https://docs.docker.com/engine/installation/linux/ubuntulinux/

    # apt-get update
    # apt-get install apt-transport-https ca-certificates
    # apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    # echo 'deb https://apt.dockerproject.org/repo ubuntu-xenial main' >> /etc/apt/sources.list.d/docker.list
    # apt-get update
    
Verify that APT is pulling the right images

    # apt-cache policy docker-engine
    
Install extra images

    # apt-get install linux-image-extra-$(uname -r)

Install, start and verify

    # apt-get install docker-engine
    # service docker start
    # docker run hello-world
    
## Run docker from the command line, listen on port

    # docker daemon -H 0.0.0.0:5555 &

## Move images to a custom directory

intro to docker images: http://blog.thoward37.me/articles/where-are-docker-images-stored/


Reconfigure docker to use another directory for images
- symlink, or:
- https://forums.docker.com/t/how-do-i-change-the-docker-image-installation-directory/1169


## Configure docker networking

    https://docs.docker.com/engine/userguide/networking/dockernetworks/

First of all, if iptables is used, a new chain for docker needs to be created:

    # iptables -N DOCKER
    # iptables -N DOCKER-ISOLATION

Create a bridge network that will connect dockers and the outside world.

    # docker network create --driver bridge testnet

Now the following command should list the newly created network

    # docker network ls

You can then inspect it by

    # docker network inspect testnet

The ip range is listed in the configuration.

## Installing and running an image

Pulling and starting an image; busybox is a perfect image to play with network config

    $ docker login
    $ docker pull busybox

List available images:

    $ docker images

Run a docker image interactively

    # docker run -i -t --net testnet busybox /bin/sh

It should give a prompt, quit with exit.

Test network connection by pinging the host at 172.18.0.1 and vice versa, from the host to 172.18.0.2. Also try nmap to see what's listening on the container.

List running containers

    $ docker ps

Stop a container

    $ docker stop e7c008a9b332

To run a docker process listening on some port first IPTABLES need to be configured to allow the connection

    # iptables -I INPUT 1 -p tcp --dport 389 -s 157.181.0.0/16 -j ACCEPT
    # docker run -d -p 389:389 --net testnet ...
