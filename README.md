# HoneyPress - WordPress honeypot
WordPress honeypot in a docker container


## Update:
I have began a complete re-write / re-implementation of this idea. Decided it would be best to go with good ol' Flask and python for creating a "WordPress" install. Because of Flask's flexibility and Python's modularity there are all kinds of fun to be had.


## Clone and build Docker image
```
$ git clone https://github.com/dustyfresh/HoneyPress.git
$ cd HoneyPress && docker build --rm -t honeypress .
```


## Start HoneyPress
```
$ docker run -d --name HoneyPress -p 80:80
```


## Logs
You can view access logs easily:
```
$ docker exec honeypress bash -c 'tail /opt/honeypress/logs/access.log'

192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=jquery.js HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=console.png HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=ubuntu.ttf HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:41] "GET /wp-login.php?__debugger__=yes&cmd=resource&f=console.png HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:44] "GET /wp-login.php HTTP/1.1" 200 -
192.168.99.1 - - [06/Jun/2016 03:21:46] "POST /wp-login.php HTTP/1.1" 200 -
```


### Password logging
If you wanted to extract a list of passwords used in testing:
```
$ docker exec honeypress bash -c 'tail /opt/honeypress/logs/auth.log'

[2016-06-06 03:21:41.061363] - 192.168.99.1 - user: admin pass: admin - Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/
46.0
```


## ToDo
- Log shipping (prolly will just use rsyslog / S3)
- Access log monitoring (look for things like sql injections, LFI/RFI, XSS, etc)
- Modular vulnerabilities. Need to make it easier to fake a new vulnerability so scanners think they're exploiting a live target
- Tor detection
- Database of some sort.. haven't decided if I should go with MongoDB or just use sqlite
- Do some benchmarking.. is nginx needed?
