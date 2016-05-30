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


## Install 1. and 2.
The appropriate docker file is *nbdashboard/Dockerfile-dashb-declwidgets-notebook* 

## Install 3.

Download the https://github.com/jupyter-incubator/dashboards_server
```

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


