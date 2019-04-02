
from socket import * 
from threading import * 
import sys 


def handleRequest(tcpSocket):		
	
	packet = tcpSocket.recv(4096)		
	path = packet.split()[1]
	
	try:
			
		f = open(path[1:])	
		output = f.read()	
		f.close()
		
		tcpSocket.send('HTTP/1.0 200 OK\r\n\r\n')
		tcpSocket.send(output)
		
		
	except IOError:
		
		tcpSocket.send('HTTP/1.1 404 Not Found \r\n\r\n')
		f = open('404.html')	
		
		output = f.read()		
		tcpSocket.send(output)	
				
	tcpSocket.close()	
	
def startServer(serverAddress, serverPort, number):	
	
	sSocket = socket(AF_INET, SOCK_STREAM)	
	sSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)		
	sSocket.bind((serverAddress, serverPort))	
	
	threads = []
	
	while number > 0:
		
		sSocket.listen(number)	
		uSocket, address = sSocket.accept()
		
		newthread = Thread(handleRequest(uSocket))
		newthread.start()
		threads.append(newthread)
		number = number - 1	
	
	sSocket.close()	
	

port = input("Port: ") 
number = input("Number of threads: ")

startServer("", port, number)
