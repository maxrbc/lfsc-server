
'''
Created on Nov 9, 2014

@author: ricardo
'''

import socket
from multiprocessing import Process , Manager
from server_commands import *
from micro_commands import *
from server.micro_commands import run_micro_server_command




def main():
    print str(os.getcwd())
    host = '0.0.0.0'
    port = 50000
    backlog = 5 
    size = 1024
    
    
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    
    man = Manager()
    mem = {
           "server_mem" : man.dict() , 
           "status" : {
                       "RUNNING": False ,
                        "NEED_CONF" : True ,
                        "READING" : False
                        }
           }
    
    
    
    while 1 : 
        
        client , address = s.accept()
        data = client.recv(size)
        
        if data == "CLIENT1":
            terminal_server(s, client, command, mem)
                    
         
        elif data == "MICRO_CLIENT" :
            micro_sever(s, client, command, mem)
           
        
        else :
            print "Unknown Connection .... will be shut\n"
            print "data sended :"+data+"_"
            client.send("No idea who you are! ")
           
            
            
            
            
            
    


def terminal_server(client,command , mem):
    
    print "hey its client one! \n"
    client.send("CONNECTED")
    command = client.recv(size)
                
    while not command == "EXT":
        run_server_command(client,command , mem)
        client.recv(size)
        client.send("ONLINE")
        command = client.recv(size)
        
    pass



def micro_sever(client,command , mem):
    
    print "Hey its Micro client! \n"
    client.send("CONNECTED")
    command = client.recv(size)
    
    while not command == "EXT":
        run_micro_server_command(client,command, mem)
        client.recv(size)
        client.send("ONLINE")
        command = client.recv(size)
        
    pass



    


if __name__ == "__main__":
    main()
