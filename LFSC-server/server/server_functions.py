'''
Created on Nov 17, 2014

@author: xaradrim
'''

'''
Created on Nov 24, 2014

@author: xaradrim
'''
import subprocess as sub

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
 Function to parse , read and update the machine 
 configuration values present for the calculation of the 
 sun position
'''

def conf_parser(conf_path):
    
    conf = {}
    for line in open(conf_path , "r"):
        if not "#" in line:
            conf[line.split(">")[0].strip()] = line.split(">")[1].strip()
    return conf


'''
    Function to determine , based on some initial values , where the sun 
    should be [ azimuth and zenith ] at a certain date/time in the day 
'''


def job_submit(init_date , final_date):
    
    conf = conf_parser(conf_path)
    servem ["CONF"] =  conf
    servem["INIT_JOB"] = init_date
    servem["FINAL_JOB"] = final_date
    
    spa_output = sub.check_output([spa_script,init_date,final_date,conf["LATITUD"],conf["LONGITUD"],conf["HEIGHT"]])
    print spa_output
    list_output = spa_output.split("\n")
    
    sun_positions = []
    num_positions = 0
    
    for e in list_output:
        
        if "====" in e:
            sun_positions.append(dict())
        if "Date" in e:
            sun_positions[num_positions]["date"] = e.split(">")[1]
        if "azimuth" in e:
            sun_positions[num_positions]["azimuth"] = e.split(">")[1]
        if "zenith" in e:
            sun_positions[num_positions]["zenith"] = e.split(">")[1]
            print e.split(">")[1]
            num_positions += 1
        
            for k,v in sun_positions[num_positions-1].iteritems():
                print str(k)+" : "+str(v)+"\n"
                
    dates = []
    motor_positions  = []
    
    for position in sun_positions:
        motors = calculate_motor_positions(position["azimuth"] , position["zenith"])
        dates.append(position["date"])
        motor_positions.append(motors)
        
    servem["DATES"] = dates
    servem["MOTOR_POSITIONS"] = motor_positions
    
    for motor in motor_positions:
        print str(motor)+"\n"
        
    
    doc = open("./Logs/log_text_file.txt","w")
    for line in motor_positions:
        doc.write("==========================================\n")
        doc.write(str(line))
        doc.write("\n")
    doc.close()
        
    
    return
    

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

