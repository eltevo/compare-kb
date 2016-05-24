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