# Installing gitlab in a docker image

    # docker pull gitlab/gitlab-ce

    # mkdir -p /data/data1/compare/etc/gitlab
    # mkdir -p /data/data1/compare/var/log/gitlab
    # mkdir -p /data/data1/compare/var/opt/gitlab

    # docker run -d --name gitlab -v /data/data1/compare/etc/gitlab:/etc/gitlab -v /data/data1/compare/var/log/gitlab:/var/log/gitlab -v /data/data1/compare/var/opt/gitlab:/var/opt/gitlab  gitlab/gitlab-ce:latest

The full command looks like this

    # docker run --detach \
      --hostname gitlab.example.com \
      --publish 443:443 --publish 80:80 --publish 22:22 \
      --name gitlab \
      --restart always \
      --volume /data/data1/compare/etc/gitlab:/etc/gitlab \
      --volume /data/data1/compare/var/log/gitlab:/var/log/gitlab \
      --volume /data/data1/compare/var/opt/gitlab:/var/opt/gitlab \
      gitlab/gitlab-ce:latest
	  
Reconfigure external URL to be used with reverse proxy (nginx)

Edit /data/data1/compare/etc/gitlab/gitlab.rb

===============================================================
external_url "http://compare.vo.elte.hu/gitlab"

gitlab_rails['gitlab_email_from'] = 'dobos@complex.elte.hu'
gitlab_rails['gitlab_email_display_name'] = 'Compare gitlab'
gitlab_rails['gitlab_email_reply_to'] = 'noreply@complex.elte.hu'

gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "mail.elte.hu"
===============================================================

At the beginning the server will report to be busy due to some initialization task. After about 30 sec it will become available, so don't worry about the 502 when you try to access it right after the docker container was launched. It you see the gitlab logo, you're fine.


# Configure OpenLDAP with gitlab