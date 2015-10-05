## HoneyPress - WordPress honeypot container

This docker container will build a WordPress environment for you using the following:
* Nginx
* WP-CLI
* PHP5-FPM
* PHP 5.5
* Naxsi WAF

### Clone and build docker image
```
$ git clone https://github.com/dustyfresh/HoneyPress.git
$ cd HoneyPress
$ docker build --rm -t honeypress .
```

### Start container
Example:
```
$ ./container-start.sh
```

### Logs
Naxsi Logs:
```
logs/error.log
```

Access Logs
```
logs/access.log
```

### WordPress admin credentials
User: **admin**  
pass: **password**

### MySQL authentication
```
$ mysql -u root -p’wordpress’
```

```
$ egrep 'DB_USER|DB_PASS' /var/www/html/wp-config.php
define('DB_USER', 'wordpress');
define('DB_PASSWORD', 'wordpress');
```

### Install vulnerable plugins
Install vulnerable plugins & themes so we will be attacked by bots. Naxsi will log attack so we can look into them further. You can see a list of WordPress vulnerabilities [here](https://wpvulndb.com/).
