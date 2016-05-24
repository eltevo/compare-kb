# Installing nginx on a host machine

    # apt-get install nginx
	
# Configure

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
