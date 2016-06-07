#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = ''

def loginattempt(ip,user,passwd,useragent):
    with open("/opt/honeypress/logs/auth.log", "a") as log:
        log.write('[{}] - {} - user: {} pass: {} - {}\n\n\n'.format(str(datetime.now()),ip,user,passwd, useragent))

def logmobiledetector(ip, payload, useragent):
    with open("/opt/honeypress/logs/mobiledetector.log", "a") as log:
        log.write('[{}] - {} - {} - Payload:src={}\n'.format(str(datetime.now()), ip, useragent, payload))

@app.route('/')
def index():
    return render_template('index.php'), 200

@app.route('/searchreplacedb2.php')
def searchreplacedb2():
    return '', 200

# Detecting dirlisting for uploads
@app.route('/wp-content/uploads/')
def uploadsdirlisting():
    return 'index of /', 200

@app.route('/wp-content/debug.log')
def debuglog():
    return 'aaa', 200

@app.route('/wp-admin/admin-ajax.php')
def adminajaxphp():
    return '0', 200

@app.route('/xmlrpc.php', methods=['GET', 'POST'])
def xmlrpc():
    if request.method == 'GET':
        return 'XML-RPC server accepts POST requests only.', 405
    elif request.method == 'POST':
        return '', 403

@app.route('/readme.html')
def readme():
    return render_template('readme.html'), 200

@app.route('/wp-config.php')
def wpconfig():
    return '', 200

@app.route('/wp-content')
def wpcontent():
    return '', 200

@app.route('/wp-content/themes')
def wpcontentthemes():
    return '', 200

@app.route('/wp-content/plugins')
def wpcontentplugins():
    return '', 200

@app.route('/wp-content/uploads')
def uploads():
    return '', 200

@app.route('/wp-admin')
def wpadmin():
    return redirect("/wp-login.php", code=302)

@app.route('/wp-admin/')
def wpadminslash():
    return redirect("/wp-login.php", code=302)

@app.route('/wp-login.php', methods=['GET', 'POST'])
def wplogin():
    if request.method == 'POST':
        username = request.form['log']
        password = request.form['pwd']
        loginattempt(request.remote_addr,username,password,request.headers.get('User-Agent'))
        if username == 'admin' and password == 'admin':
            return 'username and password are both admin. Likely a bot trying to use default login details or brute force.', 200
        elif username == 'admin' and password == 'password':
            return 'username and password are admin:password. Likely a bot trying to use default login details or brute force.', 200
        return render_template('wp-login.php'), 200
    return render_template('wp-login.php'), 200

# Reference: https://blog.sucuri.net/2016/06/wp-mobile-detector-vulnerability-being-exploited-in-the-wild.html
@app.route('/wp-content/plugins/wp-mobile-detector/', methods=['GET', 'POST'])
def wpmobiledetectorslash():
    return '', 200

@app.route('/wp-content/plugins/wp-mobile-detector/resize.php', methods=['GET', 'POST'])
def wpmobiledetector():
    if request.method == 'POST':
        if request.form['src']:
            logmobiledetector(request.remote_addr, request.form['src'], request.headers.get('User-Agent'))
    return '', 200

@app.route('/wp-content/plugins/wp-mobile-detector/readme.txt', methods=['GET', 'POST'])
def wpmobiledetectorreadme():
    return '', 200


@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
''', 200

@app.after_request
def apply_caching(response):
    response.headers["Server"] = "nginx"
    response.headers["Content-Type"] = "text/html; charset=UTF-8"
    response.headers["Connection"] = "keep-alive"
    response.headers["Keep-Alive"] = "timeout=20"
    response.headers["Link"] = '<http://wordpress.com/wp-json/>; rel="https://api.w.org/"'
    response.headers["Set-Cookie"] = 'wordpress_test_cookie=WP+Cookie+check; path=/'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
