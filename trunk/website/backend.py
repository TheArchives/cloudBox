# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import socket
import simplejson

class BackendSocket(object):
    
    def __init__(self, host, port, password):
        #print "Connecting to %s:%s" % (host,port)
        self.skt = socket.socket()
        self.skt.connect((host, port))
        self.password = password
    
    def query(self, command, data=None):
        payload = {
            "command": command,
            "password": self.password,
        }
        if data:
            payload.update(data)
        self.skt.send(simplejson.dumps(payload)+"\r\n")
        response = self.skt.recv(1024)
        while response and "\n" not in response:
            response += self.skt.recv(1024)
            # If there's no response, connection lost
            if response == "":
                break
        # We might have not got anything
        if "\n" in response:
            result, response = response.split("\n", 1)
            return simplejson.loads(result)
        else:
            raise IOError
    
    def __del__(self):
        self.skt.close()
