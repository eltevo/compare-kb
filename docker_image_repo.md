# Privat image ropository

On this [link](https://docs.docker.com/registry/) there is a detailed description about private repositorys. 

To get started, crate SSL key `my.key` and certificate `my.crt`and put them into `$DIRECTORY_OF_CERTIFICVATES_ON_HOST`.

Run the repository container available from docker
```bash
docker run -d                                                \ 
           -p 5000:5000                                      \
           --restart=always                                  \ 
           --name $NAME_OF_REGISTRY_CONTAINER                \
           -v ~$DIRECTORY_OF_CERTIFICVATES_ON_HOST:/certs:ro \
           -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/my.crt    \ 
           -e REGISTRY_HTTP_TLS_KEY=/certs/my.key            \
           registry:2
```
This exposes port `5000` on the host to be the repository port. 

Once the repository container runs it is accesible via usual docker commands as:

```bash
docker pull localhost:5000/imagename
```
