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
                  
                  "GET_POSIT" : lambda client : do_micro_get_position(client),
                  "SET_CONF" : lambda client : do_set_configuration(client),
                  "GET_LAT" : lambda client : do_get_latitud(client),
                  "GET_LON" : lambda client : do_get_longitud(client),
                  "GET_ALT" : lambda client : do_get_altitud(client),
                  "GET_INDT" : lambda client : do_get_statTime(client),
                  "GET_STAT" : lambda client : do_get_status(client),
                  "GET_OPTM" : lambda client : do_get_OpTime(client),
                  "SEND_PIC" : lambda client : do_get_picture(client)
                  }




def run_micro_server_command(client,command):
    
    if command in micro_commands.iterkeys():
        micro_commands[command](client)
        
    else:
        client.send("Unkown command")
        
    return



def do_micro_get_position(client):
    client.send("ACK_COMM")
    
    date = client.recv(size).strip() # ASK for the date to look for 
    client.send("ACK_DATE")
    
    motor = client.recv(size).strip() # ASk for the motor to be looked  [ one pos at time ] 
    
    m_posit = get_next_position(motor, date)
    
    client.send(str(m_posit))
    client.recv(size).strip() # RECV Motor ack that the motor had arrived to the micro proc

    pass

def do_get_picture(client):
    
    # Routine to receive the picture from the microprocessor
    client.send('ACK_COMM') 
    # ack the command has been received and enter the routine
    number_of_pkt = int(client.recv(size).strip())
    # should receive a init number with the amount of steps (packets ) that will take receiving the whole pic 
    client.send("RCV_NPKT")
    picture_buff = []
    for index_pkt in range(number_of_pkt):
        picture_buff.extend(client.recv(size).strip())
        client.send("RECV_PKT")
        client.recv(size).strip() # should be NEXT or DONE if no more packets to be sended
    
    print str(picture_buff)
    import time as t
    log_folder = "./jobs/picture_"
    file_name = t.strftime("%d_%m_%Y_%S_%M_%H" , t.localtime())
    pic_log_name = log_folder+file_name+".jpeg"
    
    import binascii as ba
    pic_str = ''.join(picture_buff);
    pic = ba.a2b_hex(pic_str)
        
    doc = open(pic_log_name,"w")
    doc.write(pic)
    doc.close()
    
        
    pass




'''

    GETTERS Y SETTERS FOR THE CONFIGURATION VALUE 


'''     


def do_get_latitud(client):
    
    conf = configuration()
    client.send(conf['latitud'])
    client.recv(size) ## Done flag 
    
    pass

def do_get_longitud(client):
    conf = configuration()
    client.send(conf['longitud'])
    client.recv(size) ## Done flag 
    pass

def do_get_altitud(client):
    conf = configuration()
    client.send(conf['altitud']) 
    client.recv(size) ## Done flag 
    pass

def do_get_statTime(client):
    job = get_current_job()
    client.send(job['init_date'])
    client.recv(size) ## Done flag 
    pass
def do_get_OpTime(client):
    job = get_current_job()
    client.send(str(job['duration_time']))
    client.recv(size) ## Done flag 
    pass

def do_get_status(client):
    job = get_current_job()
    client.send(job['status'])
    client.recv(size) ## Done flag 
    pass


def do_set_status(client):
    
    client.send("ACK_COMM")
    new_stat = client.recv(size).strip()
    
    set_job_status(new_stat)
    
    

def do_set_configuration(client):
    
    # commands to receiv the data needed for operation 
    client.send("ACK_COMM")
    lon = client.recv(size).strip()
    
    client.send("ACK_COMM")
    lat = client.recv(size).strip()
    
    client.send("ACK_COMM")
    alt = client.recv(size).strip()
    
    client.send("ACK_COMM")
    date = client.recv(size).strip()
    
    client.send("ACK_COMM")
    opt = client.recv(size).strip()
    
    
    set_conf(lat,lon,alt)
    new_job(date,opt)
    
    pass
    
    
    
    