'''
Created on Nov 29, 2014

@author: xaradrim
'''

from server_functions import *



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
    pass

def do_micro_job_submit():
    pass


def do_micro_get_position():
    pass

def do_set_motor_position():
    pass