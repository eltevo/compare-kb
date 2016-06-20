
# Install

You'll need node.js and npm from ubuntu repo:

    # apt-get install -y nodejs npm
  
Try nodejs

    $ nodejs
  
Add alias for node in ~/.bashrc

```~/.bashrc
alias node="nodejs"
```

Ubuntu doesn't create a link to nodejs with name no, so do it now:

    # ln -s /usr/bin/nodejs /usr/bin/node
  
## Install configurable-http-proxy

    # npm install -g configurable-http-proxy
  
Try it now

    $ configurable-http-proxy --default-target=http://localhost:8888
