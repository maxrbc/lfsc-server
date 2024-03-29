'''
Created on Nov 9, 2014

@author: ricardo
'''

import socket
from curses.ascii import isdigit
from __builtin__ import str


host = 'maxrberrios.koding.io'
port = 40000
size = 1024


toServer_commands = {
                     "GET_POSIT":lambda conn : get_motors(conn),
                     "JOB_SUBMIT":lambda conn : do_job_submit(conn),
                     "CONF": lambda conn : do_get_conf(conn)
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
    

def do_job_submit(conn):
    prompt = conn.recv(size)
    init_post = raw_input(prompt)
    conn.send(init_post)
    
    prompt = conn.recv(size)
    final_post = raw_input(prompt)
    conn.send(final_post)
    
    a = conn.recv(size)
    print " last received "+a+"\n"
    


def toServer(s,command):
    
    
    
    data = s.recv(size)
    
    s.send(command)
    toServer_commands[command](s)
    
    return s
    

def main_terminal():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.send("CLIENT1")
    
    print("welcome to LFSC Terminal : \n")
    print("Commands to RUN \n")
    print "GET_POSIT\n it will ask for a date in format month/mday / year / hh : min\n"
    print("And lastly will ask for a motor to revise or a comma separated list [ 1,2,3,4,5 ]  \n")
    
    print("JOB_SUBMIT \n")
    print ( " It will ask for 2 dates , initial date for the test and the last \n")
    print (" Both will be in std format and military hour \n")
    
    print("EXT is for going out of the terminal\n")
    print("CONF to see the configuration \n")
    
    while(1):
        comm = raw_input(">")
        comm = str(comm).upper().strip()
        
        
        if comm == "EXT":
            s.send("CLOSING")
            s.recv(size)
            s.close()
            break
        else:
            s = toServer(s,comm)
 
if __name__ == "__main__":
    main_terminal()