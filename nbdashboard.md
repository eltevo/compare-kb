Dashboard for notebooks

https://github.com/jupyter-incubator/dashboards

# Jupyter Dynamic Dashboards from Notebooks

1. Overview
---------------------
Extension for Jupyter Notebook that enables the layout and presentation of grid-based dashboards from notebooks.

There are 3 components that will build up and drive the dashboards created from jupyter notebooks. Since there is no prebuilt docker container for these, we have to make them ourselves. 

1. Dashboard Features for the Notebook
In order to use the **Dashboard Layout and Preview** for arranging notebook outputs in a grid-layout *jupyter-incubator/dashboards*

2. Bundling notebooks and associated assets for deployment as dashboards *jupyter-incubator/dashboards_bundlers*

3. Serving notebook-defined dashboards as standalone web apps *jupyter-incubator/dashboards_server*


# Environmental variables

```bash
DASHBOARD_SERVER_IP
HTTP_PORT=3000
HTTPS_PORT=3001
DASHBOARD_CONTAINER_NAME=dashserver_cont
DASHBOARD_IMAGE_NAME=dashserver
DASHBOARD_SERVER_LINK?=http://$dashboard_server_ip:$HTTP_PORT

KG_IP=157.181.172.106
KG_PORT=8888
KG_BASE_URL=/
KERNEL_GATEWAY_URL=http://$KG_IP:$KG_PORT
KG_IMAGE_NAME:=dashkernel
KG_CONTAINER_NAME:=kernel-gateway


```

## Install 1. and 2. into the notebook image
The appropriate docker file is *nbdashboard/Dockerfile-dashb-declwidgets-notebook* 
Run the jupyter notebook server:
```bash
docker run -it -p 8882:8888  --name dashnote notebook-wdashboard-image???? bash

#export DASHBOARD_REDIRECT_URL=http://$DASHBOARD_SERVER_IP:???/; \

export DASHBOARD_SERVER_URL=http://$DASHBOARD_SERVER_IP:$HTTP_PORT;\
export DASHBOARD_SERVER_AUTH_TOKEN=notebook_to_dashboard_secret; \
start-notebook.sh \
"--NotebookApp.base_url={base_path} \
--ip=0.0.0.0 \
--port=8888 \
--NotebookApp.trust_xheaders=True"
```

## Install 3.
This will build a kernel gateway and server image

Download the https://github.com/jupyter-incubator/dashboards_server

Create kernel image and run it
```bash
docker build -t dashkernel -f Dockerfile.kernel .

docker run -d \
       --name $KG_CONTAINER_NAME \
       -p 8888:8888 \
       -e KG_ALLOW_ORIGIN='*' \
       -e KG_AUTH_TOKEN=$KG_AUTH_TOKEN \
       -e KG_BASE_URL=$KG_BASE_URL \
       $KG_IMAGE_NAME;

```

Create Server image and run it
```bash
docker build -t dashserver -f Dockerfile.server .

docker run -d  --name $DASHBOARD_CONTAINER_NAME \
           -p $HTTP_PORT:$HTTP_PORT \
           -p $HTTPS_PORT:$HTTPS_PORT \
           -p 9711:8080 \
           -e USERNAME=testu \
           -e PASSWORD=testu \
           -e PORT=$HTTP_PORT \
           -e HTTPS_PORT=$HTTPS_PORT \
           -e HTTPS_KEY_FILE=$HTTPS_KEY_FILE \
           -e HTTPS_CERT_FILE=$HTTPS_CERT_FILE \
           -e SESSION_SECRET_TOKEN=$SESSION_SECRET_TOKEN \
           -e PUBLIC_LINK=$DASHBOARD_SERVER_LINK \
           -e KERNEL_GATEWAY_URL=$KERNEL_GATEWAY_URL \
           -e KG_AUTH_TOKEN=$KG_AUTH_TOKEN \
           -e KG_BASE_URL=$KG_BASE_URL \
           --link $KG_CONTAINER_NAME:$KG_CONTAINER_NAME \
           $DASHBOARD_IMAGE_NAME $CMD

```

I had to separate the apt-get update from the rest of the installation and add 'exit 0' so in case the update fails the docker script continues.
```
USER root
 
RUN echo "deb http://archive.ubuntu.com/ubuntu jessie main" > /etc/apt/sources.list
RUN echo "deb http://archive.ubuntu.com/ubuntu jessie-updates main" >> /etc/apt/sources.list
RUN echo "deb http://ftp.us.debian.org/debian stable main contrib non-free" >> /etc/apt/sources.list
 # Install Xvfb and its dependencies needed to run Electron (Nightmare tests)
RUN apt-get update; exit 0
RUN   apt-get install -y \
```


