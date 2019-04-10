#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''	Implementação de um servidor FTP em python

	@autor: Andresso
	
	Fiz a maioria das coisas a partir dos exemplos deste site: 
	https://realpython.com/python-sockets/#background
'''	
import socket as sk

serverPort = 12000
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)

print("Servidor pronto para receber")

while True:
    connectionSocket , addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    
    if(message):
        print()
        commandList = message.decode().split()
        print(commandList)
        if('GET' in commandList or 'get' in commandList):
            pass
    else:
        pass
    
    connectionSocket.close()
