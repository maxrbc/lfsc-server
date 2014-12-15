'''
Created on Nov 17, 2014

@author: xaradrim
'''

'''
Created on Nov 24, 2014

@author: xaradrim
'''
import subprocess as sub
import pymongo 

IP = 'maxrberrios.koding.io'
IP2 = 'localhost'

client = pymongo.MongoClient(IP,27017)
db  = client['lfsc-db'] 




servem = {
          "MOTOR_POSITIONS": None ,
           "DATES" : None ,
            "CURRENT_INDEX" : None ,
             "INIT_JOB" : None ,
              "FINAL_JOB" : None , 
              "CONF" : None
              }

conf_path = "./param.conf"
spa_script = "./spa_alg/spa_main"


'''
    #
    # Functions 
    #
    
    dict() conf_parser(conf_path) 
    void job_submit(init_date , final_date)
    list[] calculate_motor_positions(cal_azimuth , cal_zenith)
    
'''



def get_servem():
    return servem.copy()

def set_servem(mem):
    servem.update(mem)

def get_current_job():
    
    table = db['jobs']
    entries = table.find()
    temp = entries[entries.count() - 1]
    job = {}
    
    for k,v in temp.iteritems():
        if not k == '_id':
            job[k] = v 
    
    return job

def calculate_diference(init_date,current_date):
    import time as t
    init = date_converter(init_date)
    print current_date
    curr = date_converter(current_date)
    
    delta = t.mktime(init) - t.mktime(curr)
    result = delta/240
    
    return int(result)


'''
    This function will take a string formated date as this
    softwares expects it : mm/dd/yy/hh/min and will make a struct 
    of time 

'''

def date_converter(date):
    import time as t
    
    
    temp = date.split("/")
    temp.extend(temp.pop().split(":"))

    
    new_date = [0 for x in range(6)]
    
    new_date[4] = int(temp.pop()) ## Minutes
    new_date[3] = int(temp.pop()) ## Hours
    new_date[0] = int(temp.pop()) ## Year
    new_date[1] = int(temp.pop()) ## Month
    new_date[2] = int(temp.pop()) ## Day ( in terms of month ) 
    new_date[5] = 0               ## Seconds 
    new_date.extend([0,0,0])      ## last values are taken by pc
    
    return new_date


'''
    
'''
def set_conf(lat=None , lon = None , height = None):
    table = db['configuration']
    conf = {}
    
    if not lat == None :
        conf['latitud'] = lat
    
    if not lon == None :
        conf ['longitud'] = lon
        
    if not height == None : 
        conf['height'] = height 
    
    conf['temperature'] = str(10) #kelvin degrees
    conf['pressure'] = str(1010) # atmosphere
    
    table.insert(conf)
    
    pass


def new_job(init_date , final_date):
    table = db['jobs']
    job = {}
    job ['init_date'] = init_date
    job [ 'final_date'] = final_date
    job [' duration_time'] = calculate_diference(final_date , init_date)
    job ['status'] = 'RUN'
    
    table.insert(job)
    pass



'''
 Function to parse , read and update the machine 
 configuration values present for the calculation of the 
 sun position
'''

def configuration():
    
    conf = {}
    table = db['configuration']
    entries = table.find()
    temp = entries[entries.count() -1 ]
    
    for k,v in temp.iteritems():
        if not k == '_id' : 
            conf[k] = v
    
    return conf


'''
    Function to determine , based on some initial values , where the sun 
    should be [ azimuth and zenith ] at a certain date/time in the day 
'''


def get_next_position(motor_id , date):
    sun_position = calculate_spa(date)
    motors = calculate_motor_positions(sun_position['azimuth'], sun_position['zenith'])
    return motors[int(motor_id) - 1]
    
    
    
def calculate_spa(date):
    conf = configuration()
    
    #calculation here are done for a single date alone 
    
    spa_output = sub.check_output([spa_script,
                                   date,
                                   date,
                                   conf["latitud"],
                                   conf["longitud"],
                                   conf["height"],
                                   conf['temperature'],
                                   conf['pressure']
                                   ])

    list_output = spa_output.split("\n")
    sun_position = {}
        
    for e in list_output:
        
        if "Date" in e:
            sun_position["date"] = e.split(">")[1]
        if "azimuth" in e:
            sun_position["azimuth"] = e.split(">")[1]
        if "zenith" in e:
            sun_position["zenith"] = e.split(">")[1]
        
        
    return sun_position


def calculate_motor_positions(cal_azimuth , cal_zenith):
    import math
    motor_positions = []
    
    azimuth = float(cal_azimuth)
    zenith = float(cal_zenith)
        
    yc = 1.58
    xc = [-0.28 , -0.14 , 0 , 0.14 , 0.28]
    angulo_incidente = math.atan(math.tan(math.radians(zenith))*math.sin(math.radians(azimuth)))
        
    for motor in range(5):
       
        if motor < 2 :
            angle_pos = math.degrees(angulo_incidente - math.atan(float(yc)/-xc[motor])+(math.pi/2))/2.0            
        elif motor > 2: 
            angle_pos = math.degrees(angulo_incidente + math.atan(float(yc)/xc[motor])-(math.pi/2))/2.0
        else : 
            angle_pos = math.degrees(angulo_incidente/2.0)
            
        motor_positions.append(angle_pos)
        
    return motor_positions

