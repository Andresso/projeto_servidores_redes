#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''	Implementação de um servidor FTP em python

	@autor: Andresso
'''	
import socket as sk

serverPort = 12000
serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)

print("Servidor pronto para receber")

def get_arg(command):
    ''' Retorna o argumento do comando '''
    return command.split()[1].replace("\r\n", "")
def get_command(command):
    ''' Retorna o comando '''
    return command.split()[0]
def encode_msg(msg):
    return msg.encode('utf-8')

while True:
    connectionSocket, addr = serverSocket.accept()    
    try:
        # Quando conecta já manda essa mensagem para informar que está
        # pronto para o usuário
        connectionSocket.send("220-PyFile Server version 0.0.1 beta\r\n".encode('utf-8'))
        connectionSocket.send("220-written by Andresso (email)\r\n".encode('utf-8'))
        connectionSocket.send("220 Please visit http:site\r\n".encode('utf-8'))
    except:
        print "Erro na conexão"

    while(connectionSocket):
        message = connectionSocket.recv(1024)
        if(message):
            print("mensagem", message.decode())

            command = message.decode()
            print "comando", get_command(command)
            
            # ----------------------------------------------------------
            # Autenticação
            # ----------------------------------------------------------
            # Recebe
            if(get_command(command) == "AUTH"):
                # Responde
                print "entrou em AUTH", get_arg(command)
                connectionSocket.send("530 Please login with USER and PASS.\r\n".encode('utf-8'))
            # Recebe
            elif(get_command(command) == "USER"):
                username = get_arg(command) #" # username = nome do usuário
                # Responde
                connectionSocket.send("331 Please specify the password.\r\n".encode('utf-8'))
            # Recebe
            elif(get_command(command) == "PASS"):
                password = get_arg(command) # password = senha do usuário.
                # Responde 
                connectionSocket.send("230 Login Successful.\r\n".encode('utf-8'))
            # Recebe
            elif(get_command(command) == "SYST"):
                # Responde 
                connectionSocket.send("215.\r\n".encode('utf-8'))
            # Recebe
            elif(get_command(command) == "PWD"):
                print "PWD"
                # Responde 
                connectionSocket.send("257 '/'.\r\n".encode('utf-8'))
            # Recebe
            elif(get_command(command) == "PORT"):
                # Responde 
                connectionSocket.send('200 PORT OK\r\n'.encode('utf-8'))
            # Recebe
            elif(get_command(command) == "PORT"):
                # Responde 
                connectionSocket.send('200 PORT OK\r\n'.encode('utf-8'))


            # ----------------------------------------------------------
            # Transferência de arquivo
            # ----------------------------------------------------------
            # Do server para o Client
            # Recebe 
            elif(get_command(command) == "STOR"):
                # Nome do arquivo
                fileName = get_arg(command)
                # Responde
                connectionSocket.send("150 Ok to send data.\r\n".encode('utf-8'))  # 150 = File status okay; about to open data connection
                # Aqui cria o outro socket TCP para a transferência do arquivo
                dataPort=12002
                # O IP do cliente conectado é o primeiro elemento da tupla addr
                clientAdress=addr[0]
                dataSocket=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                dataSocket.connect((clientAdress, dataPort))
                # Recebe os dados
                dataSocket.recv(1024)
                dataSocket.close()

                # E quando termina de enviar o arquivo para o cliente, envia
                connectionSocket.send("250 Transfer complete.\r\n".encode('utf-8'))

            # Do Client para o server
            # Recebe
            elif(get_command(command) == "RETR"):
                # Nome do arquivo solicitado
                fileName = get_arg(command)
                try:
                    # Tenta abrir arquivo
                    file = open(fileName, 'r')
                except IOError:
                    # Retorna erro caso o arquivo não exista
                    connectionSocket.send('550 File not found\r\n'.encode('utf-8'))
                else:
                    dataFile = file.read()
                    # Se o arquivo existir
                    connectionSocket.send("150\r\n".encode('utf-8'))  # 150 = File status okay; about to open data connection
                    # Cria o outro socket TCP para a transferência do arquivo
                    dataPort=12002
                    # O IP do cliente conectado é o primeiro elemento da tupla addr
                    clientAdress=addr[0]

                    dataSocket=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                    dataSocket.connect((clientAdress, dataPort))
                    # Envia os dados
                    dataSocket.send(dataFile.encode('utf-8'))
                    dataSocket.close()
                    file.close()

                # E quando termina de enviar o arquivo para o servidor, envia
                connectionSocket.send("250 Transfer complete.\r\n".encode('utf-8'))
            
            elif(get_command(command) == "QUIT"):
                connection.send('221 bye\r\n'.encode('utf-8'))
                connectionSocket.close()

            else:
                # Se for um comando não reconhecido
                connection.send('221 bye\r\n'.encode('utf-8'))
                connectionSocket.close()
        else:
            # Se for mensagem vazia
            pass
    
    





