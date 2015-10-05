## HoneyPress - WordPress honeypot container

This docker container will build a WordPress environment for you using the following:
* Nginx
* WP-CLI
* PHP5-FPM
* PHP 5.5
* Naxsi WAF

### Update Naxsi Web App Firewall signatures
```
$ git clone https://github.com/nbs-system/naxsi-rules.git
```

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
