## HoneyPress - WordPress honeypot container

This docker container will build a WordPress environment for you using the following:
* Nginx
* WP-CLI
* PHP5-FPM
* PHP 5.5
* Naxsi WAF

### To Do
- [ ] Continue writing out trigger.php for malicious entity tracking
- [ ] Add functionality to pull latest and greatest vulnerable WordPress code to be used in the honeypot
- [ ] Make code less ugly
- [ ] Decide on a license
- [ ] Add more options to be used via docker environment vars

### Clone and build docker image
Before we can build the container we need to pull down the doxi-rules repo.
```
$ git clone https://github.com/dustyfresh/HoneyPress.git
$ cd HoneyPress && git clone https://bitbucket.org/lazy_dogtown/doxi-rules.git
$ docker build --rm -t honeypress .
```

### Start container
Example:
```
$ docker run --name HoneyPress -d -p 80:80 -v $(pwd)/logs:/var/log/nginx -e WP_URL='http://YourHoneyPotDomain.tld' -e WP_TITLE='Please hack me' -e ADMIN_USER='admin' -e ADMIN_EMAIL='admin@nowhere.tld' -e ADMIN_PASSWORD='password123' honeypress
```

This will start your HoneyPress container sharing port 80 (HTTP) with the host. You can see we're specifying parameters for our WordPress installation by using docker environment variables.

### Container environment variables
Variable Name  | Description
-------------- | -------------
WP_URL | site_url parameter to set in the WordPress database
WP_TITLE  | Title of the blog to set in the database
ADMIN_USER | Username to use for the admin account
ADMIN_EMAIL | Admin email address for WordPress to use
ADMIN_PASSWORD | Secifies the password to assign to the administrator account.

### Installing vulnerable plugins and themes with bootstrap script
Currently the bootstrap.php script that is used to find the latest and greatest vulnerable WordPress code is not fully automated. This is on my to-do list and will be done soon. However, you can run bootstrap.php manually and it will give you a list of wp-cli commands to run in order to bootstrap vulnerable WordPress code:
```
root@c837bf806376:/# /bootstrap.php
Execute the following commands to install vulnerable themes and plugins:

wp --allow-root --path=/var/www/html plugin install cta --version=2.4.3
wp --allow-root --path=/var/www/html plugin install gwolle-gb --version=1.5.3
wp --allow-root --path=/var/www/html plugin install events-made-easy --version=1.5.49
wp --allow-root --path=/var/www/html plugin install wp-piwik --version=1.0.4
wp --allow-root --path=/var/www/html plugin install font --version=7.5
wp --allow-root --path=/var/www/html plugin install pie-register --version=2.0.18
wp --allow-root --path=/var/www/html theme install pagelines --version=1.4.6
wp --allow-root --path=/var/www/html theme install satoshi --version=2.0
wp --allow-root --path=/var/www/html plugin install wordpress-seo --version=1.7.3.3
```

You can see that this script knows the proper version number for the plugin/theme that we hope will get compromised or see scanner activity. Hoping to get more time to touch this once trigger.php gets more love. 

### Logs
Logging is handled via a docker volume mount so we may review the HoneyPress logs without entering the container. As specified in the docker run command:
```
-v $(pwd)/logs:/var/log
```

Naxsi Logs:
```
logs/error.log
```

Access Logs
```
logs/access.log
```

### WordPress admin credentials
These are specified as environment variables for the container at runtime. See the above example in the Start container section.

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

### WP-CLI
```
$ wp --allow-root --help
NAME

  wp

DESCRIPTION

  Manage WordPress through the command-line.

SYNOPSIS

  wp <command>

SUBCOMMANDS

  cache               Manage the object cache.
  cap                 Manage user capabilities.
  cli                 Get information about WP-CLI itself.
  comment             Manage comments.
  core                Download, install, update and otherwise manage WordPress proper.
  cron                Manage WP-Cron events and schedules.
  db                  Perform basic database operations.
  eval                Execute arbitrary PHP code after loading WordPress.
  eval-file           Load and execute a PHP file after loading WordPress.
  export              Export content to a WXR file.
  help                Get help on a certain command.
  import              Import content from a WXR file.
  media               Manage attachments.
  menu                List, create, assign, and delete menus
  network
  option              Manage options.
  plugin              Manage plugins.
  post                Manage posts.
  rewrite             Manage rewrite rules.
  role                Manage user roles.
  scaffold            Generate code for post types, taxonomies, etc.
  search-replace      Search/replace strings in the database.
  server              Launch PHP's built-in web server for this specific WordPress installation.
  shell               Interactive PHP console.
  sidebar             Manage sidebars.
  site                Perform site-wide operations.
  super-admin         List, add, and remove super admins from a network.
  term                Manage terms.
  theme               Manage themes.
  transient           Manage transients.
  user                Manage users.
  widget              Manage sidebar widgets.

GLOBAL PARAMETERS

  --path=<path>
      Path to the WordPress files

  --url=<url>
      Pretend request came from given URL. In multisite, this argument is how the target
  site is specified.

  --user=<id|login|email>
      Set the WordPress user

  --skip-plugins[=<plugin>]
      Skip loading all or some plugins

  --skip-themes[=<theme>]
      Skip loading all or some themes

  --require=<path>
      Load PHP file before running the command (may be used more than once)

  --[no-]color
      Whether to colorize the output

  --debug
      Show all PHP errors

  --prompt
      Prompt the user to enter values for all command arguments

  --quiet
      Suppress informational messages

  Run 'wp help <command>' to get more information on a specific command.
```

### Email
Email has been disabled because if the container is compromised we don't want the bad actors to start sending spam email
