import os
import socket
from time import *
import _thread

class WebServer:
    def __init__(self,methods,port=80,folder="",defaultPage="index.html"):
        self.port = port
        self.methods = methods
        self.folder = folder
        self.home = defaultPage

    def start(self):
        print('Web Server starting on port: %d...' % (self.port))

        servSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            servSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

            servSocket.bind(('0.0.0.0',self.port))

            servSocket.listen(1)

            while True:
                connSocket,sourceAddr = servSocket.accept()
                if(connSocket):
                    print("%s connected" %(sourceAddr[0]))
                    _thread.start_new_thread(self.handleRequest,(connSocket))

        except Exception as e:
            servSocket.close()
            print(e)

    def handleRequest(self,client):
        message = client.recv(1024)
        request = message.decode()
        while(len(message) == 1024):
            message = client.recv(1024)
            request += message.decode()
        
        print(request)
    
        if(request):
            request = request.split('\n')[0]
            print("Request received: %s" %(request))
            words = request.split()
            url = words[1][1:]

            path = os.getcwd() + "/" + self.folder
            files = os.listdir(path)

            print(url)
            if(url == "/" or url == ""):
                url = self.home

            if(url in files):
                try:
                    file = open(path + "/" + url)
                    fileContent = file.read()
                    file.close()

                    servResponse = 'HTTP/1.0 200 OK\n\n' + fileContent
                except:
                    servResponse = 'HTTP1/0 404 NOT FOUND\n\nFile Not Found'
            else:
                methodParams = url.split("?")
                methodName = methodParams[0]
                if(methodName in self.methods.keys()):
                    if(len(methodParams) == 2):
                        params = methodParams[1].replace("~"," ").split("&")
                    else:
                        params = []
                    paramsDict = dict(param.split("=") for param in params)

                    if(set(self.methods[methodName][1]).issuperset((paramsDict.keys()))):
                        result = str(self.methods[methodName][0](**paramsDict))
                        servResponse = 'HTTP/1.0 200 OK\n\n' + result
                    else:
                        print("ERROR: Params are not suitable for requested method")
                        servResponse = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
                else:
                    print("ERROR: File/Method not found")
                    servResponse = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

            client.sendall(servResponse.encode())
            print("Request handled")
            
        client.close()

#customize error messages
#account for more errors
#prevent server crashing, put in try except

#rename repo and files

#track unique vissits
#track unique users
#implement request ID
    #show when each id has been recieved and handled

#improve how large data is recieved
    #rather than recv 10240, recv 1024 but loop until complete


#URGENT
    #recv all without timeout
        #recieve size firs, then loop until size is found
        #