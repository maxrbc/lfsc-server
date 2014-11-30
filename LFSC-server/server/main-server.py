
'''
Created on Nov 9, 2014

@author: ricardo
'''

import socket , os
from multiprocessing import Process , Manager
from server_commands import *
from micro_commands import *





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
    mem_init = {
           "server_mem" : get_servem(), 
           "RUNNING": False ,
            "NEED_CONF" : True ,
            "READING" : False
           }
           
    mem = man.dict()
    mem.update(mem_init)
    
    counter = 0
    
    
    while 1 : 
        
        client , address = s.accept()
        data = client.recv(size)
        print counter
        
        
        if data == "CLIENT1":
            
            p = Process(target = terminal_server , args=(s, client,mem))
            p.start()
            p.join()
                    
         
        elif data == "MICRO_CLIENT" :
            p = Process(target=micro_sever , args= (s, client,mem))
            p.start()
            p.join()
           
        
        else :
            print "Unknown Connection .... will be shut\n"
            print "data sended :"+data+"_"
            client.send("No idea who you are! ")
        
        counter +=1
        print "ON main " +str(mem["server_mem"]["INIT_JOB"])+"\n"
           
            
            
         

def terminal_server(s,client, mem):
    
    print "hey its client one! \n"
    client.send("CONNECTED")
    command = client.recv(size)
                
    while not command == "CLOSING" :
        
        run_server_command(client,command , mem)
        client.send("ONLINE")
        command = client.recv(size)
        print mem["server_mem"]["INIT_JOB"]+"\n"
        
        
        
    client.send("BYE BYE")
    client.close()
    pass



def micro_sever(s,client, mem):
    
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
