'''
Created on Nov 9, 2014

@author: ricardo
'''

import socket


host = 'localhost'
port = 50000
size = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

while 1:
    
    # Init COmuncation with Server
    s.send("MICRO_CLIENT")
    line = s.recv(size)
    print "Received : ",line
    
    # Open terminal to send instructions 
    while 1:
        sending = raw_input("> ")
        s.send(sending)
        
        if sending == "CPOSIT" :
            measures_size = int(s.recv(size))
            s.send("OK")
            
            motor_position = []
            
            for i in range(measures_size):
                motor = []
                for i in range(5):
                    m = s.recv(size)
                    motor.append(m)
                    s.send("OK")
                motor_position.append(motor)
                    
            for i in motor_position:
                print str(i)+"\n"
            
            done = s.recv(size)
            print "POSITIONS: "+done+"\n"
            s.send("RECV")
        
        
        ## Verification Ending of communication session 
        check = s.recv(size)
        if sending == "EXT" or not check == "DONE OK":
            print "VERIFICATION VALUE \nCheck : "+check+"\nCOMMAND : "+sending+"\n"
            d = s.recv(size)
            print "WE ARE ",d
            break
        
    s.close()
    break
    


#print 'Received : ', data 
