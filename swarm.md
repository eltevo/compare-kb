

# Consul inditas kulon docker engine-n
### Ha kell hozza kulon virtualbox
```bash
docker-machine create -d virtualbox Swarm-consul
docker-machine stop Swarm-consul
VBoxManage modifyvm Swarm-consul --natpf1 "my_consul,tcp,,8500,,8500"
docker-machine start Swarm-consul
export ipconsul=`docker-machine env Swarm-consul | grep DOCKER_HOST | sed -e 's/\/\// /' | sed -e 's/:/ /g'  | awk '{print $3}'`
export portconsul=`docker-machine env Swarm-consul | grep DOCKER_HOST | sed -e 's/:/ /g' | sed -e 's/"/ /g' | awk '{print $5}'`
```

Mivel a virtualboxban futo consul portja ki van huzva a host gep 8500-es portjara ezert egyelore minden ip address ugyanaz (157.181.172.106)

### Consul inditas
```bash
#A virtualboxban levo docker engine alapertelmezese
eval $(docker-machine env Swarm-consul)
docker run -d -p 8500:8500 --name=consul progrium/consul -server -bootstrap
```

### Manager inditas
Masik docker-engine-n
```bash
service docker stop
vim /etc/default/docker
#Add the following
DOCKER_OPTS="--cluster-store=consul://157.181.172.106:8500 --cluster-advertise=157.181.172.106:2375 -H tcp://157.181.172.106:2375 -H unix:///var/run/docker.sock"
service docker start 

# Manager inditas
docker run -d -p 4000:4000 swarm manage -H :4000 --advertise 157.181.172.106:4000 consul://157.181.172.106:8500

# Elso node inditasa
docker run -d swarm join --advertise=157.181.172.106:2375 consul://157.181.172.106:8500

#Check
docker -H 157.181.172.106:4000 info
```

### Ujabb node hozzadasa (Gawain.elte.hu-n levo virtualbox)
```bash
#daemon le
/etc/init.d/docker stop

/var/lib/boot2docker/profile
DOCKER_OPTS="--cluster-store=consul://157.181.172.106:8500 --cluster-advertise=157.181.172.83:8850 -H tcp://0.0.0.0:8850 -H unix:///var/run/docker.sock"

#Itt meg a /etc/init.d/docker -bol ki kellett kommentelni par dolgot HA TLS nelkul akartuk inditani

#daemon fel
/etc/init.d/docker start

#node inditas
docker run -d swarm join --advertise=157.181.172.83:8850 consul://157.181.172.106:8500

```
