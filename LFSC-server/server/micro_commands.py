'''
Created on Nov 29, 2014

@author: xaradrim
'''

from server_functions import *

size = 1024

'''
    Micro commands and communication to be served between system and microprocessor 
    of the project 

'''

micro_commands = {
                  "JOB_SUBMIT" : lambda client : do_micro_job_submit(client),
                  "GET_POSIT" : lambda client : do_micro_get_position(client),
                  "SET_POSIT" : lambda client: do_set_motor_position(client)
                  }




def run_micro_server_command(client,command, mem):
    if not mem["RUNNING"] : 
        mem["RUNNING"]  = True
    else:
        set_servem(mem["server_mem"])
    
    if command in micro_commands.iterkeys():
        micro_commands[command](client)
        mem["server_mem"] = servem
        
    else:
        client.send("Unkown command")
    return mem

def do_micro_job_submit():
    pass


def do_micro_get_position(client):
    client.send("ACK_COMM")
    
    date = client.recv(size).strip() # ASK for the date to look for 
    motor_index = calculate_diference(servem["INIT_JOB"],date )
    motors_position = servem["MOTOR_POSITIONS"]
    client.send("ACK_DATE")
    
    motor = client.recv(size).strip() # ASk for the motor to be looked  [ one pos at time ] 
    m_posit = motors_position[motor_index][int(motor)]
    
    client.send(str(m_posit))
    client.recv(size).strip() # RECV Motor ack that the motoro had arrived to the micro proc

    pass

def do_set_motor_position():
    pass