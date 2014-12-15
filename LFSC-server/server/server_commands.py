'''
Created on Nov 24, 2014

@author: xaradrim
'''

from server_functions import *


size = 1024

server_commands = {
                   
                   "GET_POSIT" : lambda (client): run_get_position(client),
                   "CONF" : lambda (client) : get_conf(client),
                   "SET_CONF" : lambda (client) : run_set_conf(client),
                   "NEW_JOB" : lambda (client) : run_new_job(client) , 
                   "GET_JOB" : lambda (client) : do_get_current_job(client)
                   }     




def run_new_job(client):
    client.send("> INIT_DATE : ")
    init_date = client.recv(size)
    
    client.send("> DURATION TIME : ")
    final_date = client.recv(size)
    
    ## Should soon test for boundary  cases as in for not correct behavior data
    new_job(init_date, final_date)
    client.send("CONFIGURATION SUBMITED")
    client.recv(size)
    pass


def run_set_conf(client):
    
    client.send("> latitud : ")
    lat = client.recv(size)
    
    client.send("> longitud : ")
    lon = client.recv(size)
    
    client.send("> Height : ")
    height = client.recv(size)
    
    set_conf(lat, lon, height)
    
    pass
    

def run_get_position(client = None):
    
        client.send("> Date to look for : ")
        date = client.recv(size)
        
        client.send("> List all motors to see \n>[comma separated please ] : ")
        ask_motor = client.recv(size)
        motors_ids = ask_motor.split(",")
        
        
        for motor in motors_ids:
            client.send(get_next_position(motor, date))
            client.recv(size)
        
        
        client.send("DONE")
        return
        
  

def run_server_command(client,command , mem):
    if not mem["RUNNING"] : 
        mem["RUNNING"]  = True
    else:
        set_servem(mem["server_mem"])
    
    if command in server_commands.iterkeys():
        server_commands[command](client)
        mem["server_mem"] = servem
        
    else:
        client.send("> Unkown command")
    
    return mem

def do_get_current_job(client):
    job = get_current_job()
    print str(job.keys())
    data = "INIT_DATE : {} \n DURATION_TIME : {} \n STATUS : {} \n".format(
                                                                                              job['init_date'],
                                                                                              job['duration_time'],
                                                                                              job['status'])
    client.send(data)
    pass
    
def get_conf(client):
    conf = configuration()
    data= "Latitud : "+conf["latitud"]+" , \nLongitud : "+conf["longitud"]+" \nHieight : "+conf["height"]+"\n"
    client.send(data)
    pass