'''
Created on Nov 24, 2014

@author: xaradrim
'''

from server_functions import *


size = 1024



server_commands = {
                   "JOB_SUBMIT" : lambda(client) : run_job_submit(client),
                   "GET_POSIT" : lambda (client): run_get_position(client),
                   "CONF" : lambda (client) : get_conf(client),
                   "SET_CONF" : lambda (client) : run_set_conf(client),
                   "NEW_JOB" : lambda (client) : run_new_job(client)
                   }     


def run_job_submit(client  = None, term = True ,init_position = None , final_position = None):
    if term:
        client.send("> initial position : ")
        init_pos = client.recv(size)
        client.send("> final position : ")
        final_pos = client.recv(size)
        job_submit(init_pos, final_pos)
        client.send("DONE")
        
    elif (not init_position == None and not final_position == None) :
        job_submit(init_position,final_position)
    else:
        client.send("Job cannot be submitted .... Format problem with dates\n")
    
    return

def run_new_job(client):
    client.send("> INIT_DATE : ")
    init_date = client.recv(size)
    
    client.send("> FINAL_DATE : ")
    final_date = client.recv(size)
    
    ## Should soon test for boundary  cases as in for not correct behavior data
    
    
    new_job(init_date, final_date)
    client.send("JOB_SUBMITED")
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
    

def run_get_position(client = None ,term = True , motor = None , date = None):
    if term:
        client.send("> Date to look for : ")
        date = client.recv(size)
        
        motor_index = calculate_diference(servem["INIT_JOB"],date )
        motors_position = servem["MOTOR_POSITIONS"]
        
        client.send("> List all motors to see \n>[comma separated please ] : ")
        motors = client.recv(size)
        motors = motors.split(",")
        
        for motor in motors:
            client.send(str(motors_position[motor_index][int(motor)-1])+"\n")
            client.recv(size)
        
        
        client.send("DONE")
        return
        
    else:
        
        
        motor_index = calculate_diference(servem["INIT_JOB"],date )
        motors_position = servem["MOTOR_POSITIONS"]
        
        motors = motors.split(",")
        to_return = []
        for motor in motors:
            to_return.append(motors_position[motor_index][motor])
            
        return to_return

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
    

def get_conf(client):
    conf = conf_parser(conf_path)
    str= "Latitud : "+conf["latitud"]+" , \nLongitud : "+conf["longitud"]+" \nHieight : "+conf["height"]+"\n"
    print str
    client.send(str)
    pass