#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = ''

def loginattempt(ip,user,passwd,useragent):
    with open("/opt/honeypress/logs/auth.log", "a") as log:
        log.write('[{}] - {} - user: {} pass: {} - {}\n\n\n'.format(str(datetime.now()),ip,user,passwd, useragent))

@app.route('/')
def index():
    return ''

@app.route('/xmlrpc.php', methods=['GET', 'POST'])
def xmlrpc():
    if request.method == 'GET':
        return '', 405
    elif request.method == 'POST':
        return '', 403

@app.route('/readme.html')
def readme():
    return render_template('readme.html')

@app.route('/wp-config.php')
def wpconfig():
    return ''

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

@app.route('/wp-login.php', methods=['GET', 'POST'])
def wplogin():
    if request.method == 'POST':
        username = request.form['log']
        password = request.form['pwd']
        loginattempt(request.remote_addr,username,password,request.headers.get('User-Agent'))
        if username == 'admin' and password == 'admin':
            return 'username and password are both admin. Likely a bot trying to brute force.'
        return render_template('wp-login.php')
    return render_template('wp-login.php')

@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
'''

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
    app.run(debug=True, host='0.0.0.0', port=80)
