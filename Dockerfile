FROM ubuntu:14.04
MAINTAINER dustyfresh, https://github.com/dustyfresh

# Networking
EXPOSE 3306
EXPOSE 80

# Grab deps
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password password wordpress' | debconf-set-selections && echo 'mysql-server mysql-server/root_password_again password wordpress' | debconf-set-selections
RUN apt-get update  && apt-get -y install mysql-server mysql-client vim wget git build-essential
RUN apt-get -y install python-setuptools && echo "deb http://ppa.launchpad.net/nginx/stable/ubuntu $(lsb_release -cs) main" >> /etc/apt/sources.list && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C && apt-get update
RUN apt-get install -y nginx-naxsi=1.6.2-1+trusty0 nginx=1.6.2-1+trusty0 nginx-common=1.6.2-1+trusty0 && apt-get install -y php5-cli php5-common php5-mysql php5-gd php5-fpm php5-cgi php5-fpm php-pear php5-mcrypt
ADD ./nginx.conf /etc/nginx/nginx.conf
RUN /etc/init.d/nginx stop
RUN /etc/init.d/mysql stop
RUN /etc/init.d/php5-fpm stop

# php-fpm config
RUN sed -i 's/^;cgi.fix_pathinfo.*$/cgi.fix_pathinfo = 0/g' /etc/php5/fpm/php.ini
RUN sed -i 's/^;security.limit_extensions.*$/security.limit_extensions = .php .php3 .php4 .php5/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^;listen\s.*$/listen = \/var\/run\/php5-fpm.sock/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^listen.owner.*$/listen.owner = www-data/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^listen.group.*$/listen.group = www-data/g' /etc/php5/fpm/pool.d/www.conf
RUN sed -i 's/^;listen.mode.*$/listen.mode = 0660/g' /etc/php5/fpm/pool.d/www.conf

# Nginx vhost config
ADD ./naxsi-rules/wordpress.rules /etc/nginx/wordpress.rules
ADD ./default /etc/nginx/sites-enabled/default
RUN mkdir -p /var/www/html
RUN chown -R www-data. /var/www/html


# Supervisor
RUN /usr/bin/easy_install supervisor && /usr/bin/easy_install supervisor-stdout
ADD ./supervisord.conf /etc/supervisord.conf
RUN echo "export TERM=xterm" >> /root/.bashrc
ADD ./start /start
RUN chmod +x /start
CMD ["/bin/bash", "/start"]
