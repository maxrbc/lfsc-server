
'''
Created on Nov 9, 2014

@author: ricardo
'''

import os
import sys
import socket
from server_commands import *




def main():
    print str(os.getcwd())
    host = '0.0.0.0'
    port = 50000
    backlog = 5 
    size = 1024
    
    
    scooping = "No"
    
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    
    while 1 : 
        
        client , address = s.accept()
        child_pid = os.fork()
        
        
        if not child_pid : 
            
            s.close()
            
            data = client.recv(size)
            
            if data == "CLIENT1":
                print "hey its client one! \n"
                client.send("CONNECTED")
                command = client.recv(size)
                
                while not command == "EXT":
                    talk_client(client,command)
                    command = client.recv(size)
                    
                        
             
            elif data == "MICRO_CLIENT" :
                print "Hey its Micro client! \n"
                client.send("CONNECTED")
                command = client.recv(size)
                
                while not command == "EXT":
                    talk_client(client,command)
                    command = client.recv(size)
                    
            
            else :
                print " the hell is this ?\n"
                print "data sended :"+data+"_"
                client.send("No idea who you are! ")
               
            
            client.close()
            sys.exit()
            
        else:
            print scooping
            scooping = 'Yes'
        
        print " Im out "
            

def talk_client(client,command):
    run_server_command(client,command)
    client.recv(size)
    client.send("ONLINE")
    
    

    


if __name__ == "__main__":
    main()
