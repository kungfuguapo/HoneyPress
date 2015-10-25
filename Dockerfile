FROM ubuntu:14.04
MAINTAINER dustyfresh, https://github.com/dustyfresh

# Networking
EXPOSE 3306
EXPOSE 80

# Grab deps
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password password wordpress' | debconf-set-selections && echo 'mysql-server mysql-server/root_password_again password wordpress' | debconf-set-selections
RUN apt-get update  && apt-get -y install mysql-server mysql-client vim wget git build-essential
RUN apt-get install -y nginx-naxsi && apt-get install -y php5-cli php5-common php5-mysql php5-gd php5-fpm php5-cgi php5-fpm php-pear php5-mcrypt
ADD ./nginx.conf /etc/nginx/nginx.conf
RUN /etc/init.d/nginx stop
RUN /etc/init.d/mysql stop

# php-fpm config
RUN sed -i 's/^;cgi.fix_pathinfo.*$/cgi.fix_pathinfo = 0/g' /etc/php5/fpm/php.ini
RUN sed -i 's/^;security.limit_extensions.*$/security.limit_extensions = .php .php3 .php4 .php5/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^;listen\s.*$/listen = \/var\/run\/php5-fpm.sock/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^listen.owner.*$/listen.owner = www-data/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^listen.group.*$/listen.group = www-data/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^;listen.mode.*$/listen.mode = 0660/g' /etc/php5/fpm/pool.d/www.conf

# Nginx vhost config
COPY ./doxi-rules/ /etc/nginx/doxi-rules
COPY ./default /etc/nginx/sites-enabled/default
COPY ./naxsi.rules /etc/nginx/naxsi/naxsi.rules
COPY ./trigger.php /var/www/html/trigger.php
RUN mkdir -p /var/www/html
RUN chown -R www-data. /var/www/html
COPY ./bootstrap.php /bootstrap.php
RUN chmod +x /bootstrap.php

# Supervisor
RUN apt-get -y install python-setuptools
RUN /usr/bin/easy_install supervisor && /usr/bin/easy_install supervisor-stdout
COPY ./supervisord.conf /etc/supervisord.conf
RUN echo "export TERM=xterm" >> /root/.bashrc
COPY ./start /start
RUN chmod +x /start
CMD ["/bin/bash", "/start"]
