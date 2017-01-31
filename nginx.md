# Installing nginx on a host machine

    # apt-get install nginx
	
# Configure when running on the host

Allow connections to the server on the http port:

    # iptables -I INPUT 1 -p tcp --dport 80 -s 157.181.0.0/16 -j ACCEPT

Test if you see the nginc welcome page, then make a backup of /etc/nginx/sites-available/default and edit it:

===============================================================
    server {
      listen compare.vo.elte.hu:80;
      server_name compare.vo.elte.hu;
      location /gitlab {
        proxy_pass http://172.18.0.3;
      }
    }
===============================================================

# Enable websockets etc for notebooks

    location ~* /notebook/[^/]+/[^/]+/(api/kernels/[^/]+/(channels|iopub|shell|stdin)|terminals/websocket)/? {
      proxy_pass            http://$PROXYIP:8000;
      proxy_http_version    1.1;
      proxy_set_header      Host \$http_host;
      proxy_set_header      Upgrade \$http_upgrade;
      proxy_set_header      Connection \"upgrade\";
      proxy_read_timeout    86400;
    }
    
# Customize error messages to include proxy server name (for debugging)

In any server section, add:

    error_page 502 /502.html;

    location = /502.html {
      root /var/www/nginx/;
    }
    
Put error page 502.html under /var/www/nginx/ with content:

```
<html>
<head><title>502 Bad Gateway</title></head>
<body bgcolor="white">
<center><h1>502 Bad Gateway: pollux-ubuntu</h1></center>
<hr><center>nginx/1.10.0 (Ubuntu)</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
```

# Installing nginx in a docker container

Create a directory for the customized nginx.conf file and copy an original nginx.conf to here from somewhere.

    # mkdir -p /data/data1/compare/srv/nginx/etc/

    # docker pull nginx
    #  docker run --name compare-nginx --net testnet -v /data/data1/compare/srv/nginx/etc/nginx.conf:/etc/nginx/nginx.conf:ro -v /data/data1/compare/srv/nginx/etc/sites-enabled/:/etc/nginx/sites-enabled/ -d nginx

A typical nginx.conf should look like this

===============================================================
	user www-data;
	worker_processes 4;
	pid /run/nginx.pid;

	events {
		worker_connections 768;
		# multi_accept on;
	}

	http {

		# ... lot of stuff ...

		server {
		  listen compare.vo.elte.hu:80;
		  server_name compare.vo.elte.hu;
		  location /gitlab {
			proxy_pass http://172.18.0.3;
		  }
		}
	}
===============================================================


Test with curl

    curl http://172.18.0.5
