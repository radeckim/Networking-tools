import socket
import os
import sys
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
 
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff 
        count = count + 2

    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff 

    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receiveOnePing(my_socket, ID, timeout):
    
    timeLeft = timeout
    
    while True:
        startedSelect = time.time()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect
        if whatReady[0] == []:
            return

        timeReceived = time.time()
        recPacket, addr = my_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
                
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return

def sendOnePing(my_socket, destinationAddress, ID):
   
    destinationAddress  =  socket.gethostbyname(destinationAddress)
    my_checksum = 0

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", time.time()) + data

    my_checksum = checksum(header + data)

    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    packet = header + data
    my_socket.sendto(packet, (destinationAddress, 1)) 

def doOnePing(destinationAddress, timeout):
	
    icmp = socket.getprotobyname("icmp")
    
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)   

    ID = os.getpid() & 0xFFFF

    sendOnePing(sSocket, destinationAddress, ID)
    delay = receiveOnePing(sSocket, ID, timeout)

    sSocket.close()
    return delay


def ping(destinationAddress, timeout, measurement):
	
	increment = 0	
	packetLoss = 0	
	maxDelay = 0
	minDelay = 0
   
	while(increment < measurement):
		
		print destinationAddress,
		
		try:			
				
			delay  =  doOnePing(destinationAddress, timeout)			
			time.sleep(1)			
				
		except socket.gaierror, e:
			print " - sending a packet failed (socket error: '%s')" % e[1]
			break

		if delay  ==  None:
			
			packetLoss = packetLoss + 1
			print " - sending a packet failed (timeout within %ssec.)" % timeout
			
		else:
			
			delay  =  delay * 1000			
			
			if delay > maxDelay:
				
				maxDelay = delay 
				
			else:
				
				minDelay = delay			
			
			print "gets ping in %0.4fms" % delay
         
		increment = increment + 1
		
	print "The minimum ping was: %0.4fms" % minDelay
	print "The maximum ping was: %0.4fms" % maxDelay
	
	percent = packetLoss / measurement
	
	print "%d out of %d packets were lost" % (packetLoss, measurement)


hostName = raw_input("Host name: ")   
measurement = input("Measurement: ")  
timeout = input("Timeout: ")  
   
ping(hostName, timeout, measurement)
   
