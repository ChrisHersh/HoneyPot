"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from HoneyPot import app
from HoneyPot.models import *

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""

    passwords = []
    usernames = []
    ips = []

    for un in Username.select().order_by(Username.count.desc()):
        usernames.append( (un.username, un.count) )

    for pw in Password.select().order_by(Password.count.desc()):
        passwords.append( (pw.password, pw.count) )

    for ip in IPAddr.select().order_by(IPAddr.count.desc()):
        ips.append( (ip.ip, ip.count) )

    ucount = Username.select().count()
    pcount = Password.select().count()
    icount = IPAddr.select().count()

    return render_template(
        'index.html',
        title='HoneyPot',
        year=datetime.now().year,
        usernames=usernames,
        passwords=passwords,
        ips=ips,
        ucount=ucount,
        pcount=pcount,
        icount=icount,
    )

#@app.route('/contact')
#def contact():
#    """Renders the contact page."""
#    return render_template(
#        'contact.html',
#        title='Contact',
#        year=datetime.now().year,
#        message='Your contact page.'
#    )

#@app.route('/about')
#def about():
#    """Renders the about page."""
#    return render_template(
#        'about.html',
#        title='About',
#        year=datetime.now().year,
#        message='Your application description page.'
#    )
