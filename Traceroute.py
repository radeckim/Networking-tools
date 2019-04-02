#!/usr/bin/python
import socket

def main(dest_name):

	desinationAdd = socket.gethostbyname(dest_name)

	port = 33434
	max_hops = 30
	
	icmp = socket.getprotobyname('icmp')
	udp = socket.getprotobyname('udp')
	
	ttl = 1
	
	while True:
		
		recvSoc = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		sendSoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
		
		sendSoc.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)	
		recvSoc.bind(("", port))
		sendSoc.sendto("", (dest_name, port))
		
		currAddr = None
		currName = None		
		
		try:
			
			_, currAddr = recvSoc.recvfrom(512)
			currAddr = currAddr[0]			
			
			try:
				
				currName = socket.gethostbyaddr(currAddr)[0]		
				
			except socket.error:					
				
				currName = currAddr					
					
		except socket.error:
			
			pass
			
		finally: 
				
			sendSoc.close()
			recvSoc.close()
			
		if currAddr is not None:
			
			currHost = "%s (%s)" % (currName, currAddr)
			
		else: 
			
			currHost = "*"
			
		print "%d\t%s" % (ttl, currHost)
			
		ttl += 1
			
		if currAddr == desinationAdd or ttl > max_hops:
			break
				
main('lancaster.ac.uk')
