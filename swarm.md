

### Consul inditas kulon docker engine-n
# Ha kell hozza kulon virtualbox
```bash
docker-machine create -d virtualbox Swarm-consul
docker-machine stop Swarm-consul
VBoxManage modifyvm Swarm-consul --natpf1 "my_consul,tcp,,8500,,8500"
docker-machine start Swarm-consul
```

# Consul inditas
```bash
#A virtualboxban levo docker engine alapertelmezese
eval $(docker-machine env Swarm-consul)
docker run -d -p 8500:8500 --name=consul progrium/consul -server -bootstrap
```
