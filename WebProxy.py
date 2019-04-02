from socket import * 
from threading import * 
import sys 

def handleRequest(tcpSocket):		
	
	packet = tcpSocket.recv(4096)		
	path = packet.split("\n")[0]	
	url = path.split(' ')[1]	
	http_pos = url.find("://")
	
	if (http_pos ==- 1):
		myUrl = url - 1
		
	else:		
		myUrl = url[(http_pos+3):len(url)-1] 	
			
	s2= socket(AF_INET, SOCK_STREAM)
	s2.connect((myUrl,80))		
	s2.send(packet)
	rec = s2.recv(1024)
	
	tcpSocket.sendall(rec)		
	tcpSocket.send(packet)					
	tcpSocket.close()

def startServer(serverAddress, serverPort):	
	
	sSocket = socket(AF_INET, SOCK_STREAM)	
	sSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)		
	sSocket.bind((serverAddress, serverPort))	
		
	sSocket.listen(1)
	uSocket, address = sSocket.accept()
	handleRequest(uSocket)
	
	sSocket.close()			
port = input("Port: ") 

startServer("", port)
