#!/usr/bin/env python

import sys

 
from twisted.conch.unix import UnixSSHRealm
from twisted.cred import portal
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred.error import UnauthorizedLogin
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.internet import reactor, defer
from zope.interface import implements
from twisted.python import log

from HoneyPot.models import *
 
# Logging was disabled
# log.startLogging(sys.stderr)
 
# Server-side public and private keys. These are the keys found in
# sshsimpleserver.py. Make sure you generate your own using ssh-keygen!
 
publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV'
 
privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""
 
class NullDatabase:
    """Authentication/authorization backend using nothing """
    credentialInterfaces = IUsernamePassword,
    implements(ICredentialsChecker)

    def __init__(self):

        pass
 
    def requestAvatarId(self, credentials):
        password = credentials.password
        username = credentials.username

        try:
            dbun = Username.get(Username.username == username)
            dbun.count += 1

            dbun.save()
            
        except:
            Username.create(username=username, count=1)
        finally:
            pass

        try:
            dbpw = Password.get(Password.password == password)
            dbpw.count += 1

            dbpw.save()
            
        except:
            Password.create(password=password, count=1)
        finally:
            pass

        return defer.fail(UnauthorizedLogin("invalid password"))
 


class AuthServer(userauth.SSHUserAuthServer):
    def _ebBadAuth(self, reason):
        addr = self.transport.getPeer().address.host
        print("addr {} failed to log in as {} using {}"
              .format(addr, self.user, self.method))

        print(repr(addr))
        addr = unicode(addr)
        print(repr(addr))
        if self.method == "password":
            try:
                dbip = IPAddr.get(IPAddr.ip == addr)
                dbip.count += 1
                print("IP Count " + str(dbip.count))
                dbip.save()
            
            except:
                IPAddr.create(ip=addr, count=1)
            finally:
                pass

        userauth.SSHUserAuthServer._ebBadAuth(self, reason)


class UnixSSHdFactory(factory.SSHFactory):
    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=publicKey)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privateKey)
    }
    services = {
        'ssh-userauth': AuthServer,
        'ssh-connection': connection.SSHConnection
    }
 
# Components have already been registered in twisted.conch.unix
 
portal = portal.Portal(UnixSSHRealm())
portal.registerChecker(NullDatabase())
UnixSSHdFactory.portal = portal
 
if __name__ == '__main__':
    reactor.listenTCP(5022, UnixSSHdFactory())
    print "Running"
    reactor.run()
