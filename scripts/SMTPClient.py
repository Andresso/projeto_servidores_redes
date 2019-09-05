# -*- coding: utf-8 -*-
 
# Importa módulo socket, que forma base das comunicações em rede em Python
import socket as sk
# Importa módulo base64, que forma codifica mensagem texto em binário de 64 bits
import base64 as b64
# Importa módulo sst, que implementa camada de soquete de segurança (criptografia)
import ssl
# Importa módulo getpass para pegar a senha do usuário
import getpass

def show_info(emailFrom, emailTo, subject, message):
	print """
	de  : %s
	para: %s
	assunto: %s
	messagem: %s
	"""%(emailFrom, emailTo, subject, message)

# Define nome (ou IP) e número de porta do servidor SMTP
serverName = 'smtp.gmail.com'
serverPort = 587
  
# Cria soquete TCP do cliente
clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
 
# Solicita estabelecimento de conexão com servidor
clientSocket.connect((serverName, serverPort))
recv = clientSocket.recv(1024) # Aguarda confirmação 220 do servidor
print(recv.decode('utf-8'))
 
# Envia mensagem HELO para servidor
clientSocket.send('HELO gmail.com\r\n'.encode('utf-8'))
recv = clientSocket.recv(1024) # Aguarda confirmação 250 do servidor
print(recv.decode('utf-8'))
 
# Inicia sessão TLS com servidor
clientSocket.send('STARTTLS\r\n'.encode('utf-8'))
recv = clientSocket.recv(1024) # Aguarda confirmação 220 do servidor
print(recv.decode('utf-8'))
     
# Cria soquete seguro e solicita login com servidor via sessão TLS
secureclientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
secureclientSocket.send('AUTH LOGIN\r\n'.encode('utf-8'))
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
print(recv.decode('utf-8'))

# Envia nome de usuário ao servidor via sessão TLS
emailFrom = raw_input("Informe seu email: ")
password = getpass.getpass("Informe sua senha: ")

secureclientSocket.send(b64.b64encode(emailFrom.encode('utf-8')) + '\r\n'.encode('utf-8'))
recv = secureclientSocket.recv(1024) # Aguarda confirmação 334 do servidor
# print(recv.decode('utf-8'))

# Envia senha ao servidor via sessão TLS
secureclientSocket.send(b64.b64encode(password.encode('utf-8')) + '\r\n'.encode('utf-8')) 
recv = secureclientSocket.recv(1024) # Aguarda confirmação 235 do servidor
recv = recv.decode('utf-8')
if(recv.split()[0] == '235'):
	print("Login efetuado com sucesso.")
else:
	print("Erro ao efetuar login.")
 
# Introduzir aqui códido do aluno
emailTo = raw_input("Informe email de destino: ")
# Lê o assunto do email
subject = raw_input("Informe o assunto: ")
# Lê mensagem a enviar digitada com teclado e atribui à variável message
message = raw_input('Sentença de entrada (letras minúsculas): ') + '\r\n.\r\n'
# Mostra informações sobre o email
show_info(emailFrom, emailTo, subject, message)

# Informa o email de origem
mailFrom = "MAIL FROM: <%s> \r\n"%emailFrom
print(mailFrom)
secureclientSocket.send(mailFrom.encode('utf-8'))
recv2 = secureclientSocket.recv(1024)
print("Resposta ao comando MAIL FROM: "+ recv2.decode('utf-8'))

# Informa o email de origem
rcptTo = "RCPT TO: <%s> \r\n"%emailTo
secureclientSocket.send(rcptTo.encode('utf-8'))
recv = secureclientSocket.recv(1024)
print("Resposta ao comando RCPT TO: "+ recv.decode('utf-8'))

# INforma o email de destino
data = "DATA\r\n"
secureclientSocket.send(data)
recv = secureclientSocket.recv(1024)
print("Resposta ao comando DATA: "+ recv.decode('utf-8'))

secureclientSocket.send(("Subject: %s\r\n\r\n"%subject).encode())
secureclientSocket.send(message.encode())
secureclientSocket.send('\r\n.\r\n'.encode())
recv_msg = secureclientSocket.recv(1024)
recv_msg = recv_msg.decode('utf-8')
print("Resposta ao envio do corpo da mensagem:"+recv_msg)

if(recv_msg):
	print("Email enviado com sucesso.")
else:
	print("Falha ao enviar o email. Tente novamente.")
# Informa que as operações chegaram ao fim
quit = "QUIT\r\n"
secureclientSocket.send(quit.encode())
recv = secureclientSocket.recv(1024)
print(recv.decode('utf-8'))

# Fecha soquete SSL do cliente
secureclientSocket.close()
 
# Fecha soquete do cliente
clientSocket.close()