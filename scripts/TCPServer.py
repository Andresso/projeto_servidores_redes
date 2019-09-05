#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Implementação de um servidor TCP em python

	@autor: Andresso
	
	Fiz a maioria das coisas a partir dos exemplos deste site: 
	https://realpython.com/python-sockets/#background
'''	

import socket as sk

serverPort = 12001
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)

print("Servidor pronto para receber")

def page(port):
    string = '''
    <html>
    <head>
        <title>Python is awesome!</title>
    </head>
    <body>
        <h1>Usando redes para ler poesia</h1>
        <h2>DIGITE: SERVER_IP:%s/poesia1.txt</h2>
        <h2>or</h2>
        <h2>DIGITE: SERVER_IP:%s/poesia2.txt</h2>
        <p>e bom proveito!</p>
    </body>
    </html>'''%(port, port)
    return string.encode('utf-8')

while True:
    connectionSocket , addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    
    if(message):
        print()
        commandList = message.decode('utf-8').split()
        print(commandList)
        if('GET' in commandList or 'get' in commandList):
            #print("tem get aqui")
            fileName = commandList[1][1:]
            if(fileName.endswith(".txt")):
                print("Requisição do arquivo %s"%str(fileName))
     
                try:
                    file = open("./data/"+fileName, 'r')
                    print("Conteúdo do arquivo")
                    connectionSocket.send("HTTP/1.1 200 OK\n\r".encode('utf-8'))
         
                    for line in file.readlines():
                        print(line)
                        try:
                            connectionSocket.send(line.encode('utf-8'))
                        except:
                            connectionSocket.send("Erro...".encode('utf-8'))
                except IOError:
                    connectionSocket.send("HTTP/1.1 404 Not Found\n\r".encode('utf-8'))
                    print("\n\n404 Not Found\n\n")
                    connectionSocket.send("404 Not Found\r\n".encode('utf-8'))
            else:
                connectionSocket.send("HTTP/1.1 200 OK\n\r".encode('utf-8'))
                connectionSocket.send(page(serverPort))
    else:
        try:
            connectionSocket.send("HTTP/1.1 200 OK\n\r".encode('utf-8'))
            connectionSocket.send(page(serverPort))
        except:
            pass
    
    connectionSocket.close()
