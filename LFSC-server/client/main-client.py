'''
Created on Nov 9, 2014

@author: ricardo
'''

import socket
from curses.ascii import isdigit
from __builtin__ import str


host = 'localhost'
port = 40000
size = 1024


toServer_commands = {
                     "GET_POSIT":lambda conn : get_motors(conn),
                     "CONF": lambda conn : do_get_conf(conn),
                     "SET_CONF" : lambda conn : do_set_conf(conn),
                     "NEW_JOB" : lambda conn : do_new_job(conn) , 
                     "GET_JOB" : lambda conn : do_get_job(conn)
                     }

    
def get_motors(conn):
    prompt = conn.recv(size)
    date = raw_input(prompt)
    conn.send(date)
    
    prompt = conn.recv(size)
    motors = raw_input(prompt)
    conn.send(motors)
    
    for motor in motors.split(","):
        position = conn.recv(size)
        print("> Motor_"+motor+" : "+str(position))
        conn.send("received")
        
    conn.recv(size)


def do_get_conf(conn):
    str = conn.recv(size)
    print str


def do_new_job(conn):
    print "CREATING NEW JOB \n"
    
    init_date = raw_input(conn.recv(size))
    conn.send(init_date)
    
    duration_time = raw_input(conn.recv(size))
    conn.send(duration_time)
    
    print conn.recv(size)+"\n"
    
    pass
    

def do_set_conf(conn):
    print "SET CONFIGURATION VALUE \n"
    lat = raw_input(conn.recv(size))
    conn.send(lat)
    lon = raw_input(conn.recv(size))
    conn.send(lon)
    height = raw_input(conn.recv(size))
    conn.send(height)
    
    print "DONE CONFIG"
    pass 
    

def do_get_job(conn):
    data = conn.recv(size)
    print data
    pass

def toServer(s,command):
    
    #data = s.recv(size)
    
    s.send(command)
    if command in toServer_commands.iterkeys():
        toServer_commands[command](s)
    else:
        print s.recv(size)
    
    
    return s




def do_naming():
    
    str  = '''
               |\     /|(  ____ \( \      (  ____ \(  ___  )(       )(  ____ \  \__   __/(  ___  )  ( \      (  ____ \(  ____ \(  ____ \                
    | )   ( || (    \/| (      | (    \/| (   ) || () () || (    \/     ) (   | (   ) |  | (      | (    \/| (    \/| (    \/                
    | | _ | || (__    | |      | |      | |   | || || || || (__         | |   | |   | |  | |      | (__    | (_____ | |                      
    | |( )| ||  __)   | |      | |      | |   | || |(_)| ||  __)        | |   | |   | |  | |      |  __)   (_____  )| |                      
    | || || || (      | |      | |      | |   | || |   | || (           | |   | |   | |  | |      | (            ) || |                      
    | () () || (____/\| (____/\| (____/\| (___) || )   ( || (____/\     | |   | (___) |  | (____/\| )      /\____) || (____/\                
    (_______)(_______/(_______/(_______/(_______)|/     \|(_______/     )_(   (_______)  (_______/|/       \_______)(_______/                
                                                                                                                                              
     _______           _        _______  _______  _______            _________ _______  _______  _______ _________ _        _______  _       
    (  ____ \|\     /|( (    /|(  ____ \(  ____ )(  ____ \|\     /|  \__   __/(  ____ \(  ____ )(       )\__   __/( (    /|(  ___  )( \      
    | (    \/| )   ( ||  \  ( || (    \/| (    )|| (    \/( \   / )     ) (   | (    \/| (    )|| () () |   ) (   |  \  ( || (   ) || (      
    | (_____ | |   | ||   \ | || (__    | (____)|| |       \ (_) /      | |   | (__    | (____)|| || || |   | |   |   \ | || (___) || |      
    (_____  )| |   | || (\ \) ||  __)   |     __)| | ____   \   /       | |   |  __)   |     __)| |(_)| |   | |   | (\ \) ||  ___  || |      
          ) || |   | || | \   || (      | (\ (   | | \_  )   ) (        | |   | (      | (\ (   | |   | |   | |   | | \   || (   ) || |      
    /\____) || (___) || )  \  || (____/\| ) \ \__| (___) |   | |        | |   | (____/\| ) \ \__| )   ( |___) (___| )  \  || )   ( || (____/\
    \_______)(_______)|/    )_)(_______/|/   \__/(_______)   \_/        )_(   (_______/|/   \__/|/     \|\_______/|/    )_)|/     \|(_______
         
     
    '''
    print(str+"\n")
    

def do_help():
    help  = '''
   
    welcome to LFSC Terminal :
    Commands to RUN 
    

    GET_POSIT it will ask for a date in format month/mday / year / hh : min
    And lastly will ask for a motor to revise or a comma separated list [ 1,2,3,4,5 ]  
    
    NEW_JOB 
      It will ask for initial date and duration time( in hours  of run 
     Both will be in std format and military hour 
    
    GET_JOB
    print( It will return current information otf the job time running 
    
    EXT is for going out of the terminal

    SET_CONF 
    will let you change the altitud , longitude and latitude

    CONF 
    to see the configuration
    
    '''
    print help

def main_terminal():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.send("CLIENT1")
    s.recv(size)
    
    time_count = 2
    
   
    
    while(1):
        
        count -= 1
        if not count == 0 :
            do_naming()
            count = 2
        
        comm = raw_input(">")
        comm = str(comm).upper().strip()
        
        
        if comm == "HELP":
            do_help()
            continue
        
        
        if comm == '':
            print " Empty command \n "
            continue
        
        if comm == "EXT":
            s.send("CLOSING")
            s.recv(size)
            s.close()
            break
        else:
            s = toServer(s,comm)
 
if __name__ == "__main__":
    main_terminal()