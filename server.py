# server.py
import Queue
import socket
import threading
import calendar
import time
import MySQLdb
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt

#from dns.rdatatype import NULL
def logdiagdata(logstring):
    print('{}-{}-{} {}:{}'.format(time.strftime("%d"),time.strftime("%m"),time.strftime("%Y"),time.strftime("%H:%M:%S"),logstring))

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def build_response():
    #We need these to be the global ones since these have been set up to access the database
    global db
    global cur
    #please see calls_query.sql for this query in a better format
    query_string=("SELECT final_calls.agent_id, current.lat_data, current.long_data, final_calls.call_flag, final_calls.user_that_called, final_calls.call_timestamp, final_calls.lat_data, final_calls.long_data,people.user_agent_type FROM agent_current_info AS current, ( ( SELECT u.`agent_id`, u.`lat_data`, u.`long_data`, u.`call_flag`, u.`user_that_called`, u.`call_timestamp` FROM agent_calls AS u INNER JOIN ( SELECT `agent_id`, MAX(`call_timestamp`) AS time_stamp FROM agent_calls GROUP BY `agent_id` ) AS q ON u.`agent_id` = q.`agent_id` AND u.`call_timestamp` = q.`time_stamp` ) AS final_calls ),operator_list as people WHERE final_calls.agent_id = current.agent_id AND final_calls.agent_id = people.agent_id AND current.online_flag = 1")
    cur.execute(query_string)
    agent_data = cur.fetchall ()
    db.commit()
    xml_string_build = "<user_data>"
    for row in agent_data :                
        xml_string_build += "<agent_pos>"
        xml_string_build += "<agent_id>"+str(row[0])+"</agent_id>"
        xml_string_build += "<latitude>"+str(row[1])+"</latitude>"
        xml_string_build += "<longitude>"+str(row[2])+"</longitude>"
        xml_string_build += "<responding_status>"+str(row[3])+"</responding_status>"
        xml_string_build += "<responding_to_user>"+str(row[4])+"</responding_to_user>"
        xml_string_build += "<responding_operator_role>"+str(row[8])+"</responding_operator_role>"
        #if this agent is to respond tell him where to go
        if (row[3] == 1):
            xml_string_build += "<respond_to_latitude>"+str(row[6])+"</respond_to_latitude>"
            xml_string_build += "<respond_to_longitude>"+str(row[7])+"</respond_to_longitude>"
        xml_string_build += "</agent_pos>"
    xml_string_build += "</user_data>"

    return xml_string_build

def build_login_response(passedusername):
    #We need these to be the global ones since these have been set up to access the database
    global db
    global cur
    #please see calls_query.sql for this query in a better format
    query_string=("SELECT * FROM operator_list WHERE username='"+passedusername+"'")
    cur.execute(query_string)
    agent_data = cur.fetchall ()
    db.commit()
    xml_string_build = "<login_data>"
    for row in agent_data :        
        xml_string_build += "<operator_id>"+str(row[0])+"</operator_id>"
        xml_string_build += "<name>"+str(row[1])+"</name>"
        xml_string_build += "<surname>"+str(row[2])+"</surname>"
        xml_string_build += "<username>"+str(row[4])+"</username>"
        xml_string_build += "<user_agent_type>"+str(row[6])+"</user_agent_type>"
        if (row[6] == 1):
            xml_string_build += "<company>"+str(row[3])+"</company>"        
    xml_string_build += "</login_data>"

    return xml_string_build

logdiagdata("Waiting for startup to be complete...")
time.sleep(2)
logdiagdata("Startup complete!")
#CREATION OF INTERNAL SOCKET TO LISTEN FOR ACTIONS
# create a server socket object
serverport = 9998
try:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    logdiagdata("Failed to create server socket")
    sys.exit()
# get local machine name
host = socket.gethostname()
# bind to the port
serversocket.bind(('0.0.0.0', serverport))
# queue up to 5 requests
serversocket.listen(5)

#create a connection to the database
db = MySQLdb.connect(host="localhost",user="root",passwd="empyrean69",db="SAfer")
cur = db.cursor()

server_run = True
closest_agent = 0
message_type = None

while server_run:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    data = clientsocket.recv(1024)
    if data:
        if (str(data) != "ping"):
            if (len(str(data))>10):
                #logdiagdata(str(data))
                e=ET.fromstring(str(data))
                #*******************************    
                #CHECK THE USER MESSAGES
                #*******************************                
                message_type = e.tag
                if (message_type == 'user_data'):
                    logdiagdata("--Update Request")
                    lat_string=e.find('LatData').text
                    long_string=e.find('LongData').text
                    user_id = e.find('UserId').text
                    call_flag = e.find('CallFlag').text
                    agent_type = e.find('TypeRequested').text                    
                    #logdiagdata("<<User:"+user_id+" Lat:"+lat_string+" Long:"+long_string+" Call Flag:"+call_flag+">>")                    
                    if (call_flag == '1'):                        
                        #################################################################
                        #                   FIND THE CLOSEST AGENT
                        #################################################################
                        #find the closest guy
                        query_string=("SELECT * FROM agent_current_info,operator_list WHERE online_flag = 1 AND user_agent_type="+agent_type+" AND agent_current_info.agent_id=operator_list.agent_id")
                        cur.execute(query_string)
                        agent_data = cur.fetchall ()
                        db.commit()
                        distance_calculated=1000000                        
                        for row in agent_data :
                            new_distance = haversine(float(long_string),float(lat_string),float(row[3]),float(row[2]))
                            #logdiagdata("<<Agent:"+str(row[1])+" Lat:"+str(row[2])+" Long:"+str(row[3])+" Dist:"+str(new_distance)+">>")
                            if (new_distance < distance_calculated):
                                closest_agent = int(row[1])
                                distance_calculated = new_distance
                        #Right now this is just assigned to agent one - we would run a query for this
                        logdiagdata("--Log Call")
                        #################################################################
                        #                   AGENT TABLES UPDATE
                        #################################################################
                        #Insert into the database all of the calls and where the agent must go
                        query_string=("INSERT INTO agent_calls (agent_id,lat_data,long_data,call_flag,user_that_called,call_timestamp) VALUES (%s,%s,%s,%s,%s,%s)")
                        data_string=(closest_agent,lat_string,long_string,'1',user_id,time.strftime('%Y-%m-%d %H:%M:%S'))
                        cur.execute(query_string,data_string)
                        db.commit()
                        #Insert into the database all of the calls and where the agent must go
                        query_string=("INSERT INTO user_requests (user_id,lat_data,long_data,call_flag,responder_id) VALUES (%s,%s,%s,%s,%s)")
                        data_string=(user_id,lat_string,long_string,'1',closest_agent)
                        cur.execute(query_string,data_string)
                        db.commit()                                                                        
                    else:
                        logdiagdata("--No Call")

                    response = build_response()                    
                    logdiagdata("--User Response Complete")
                #*******************************    
                #NOW CHECK THE AGENT MESSAGES
                #*******************************                
                message_type = e.tag
                if (message_type == 'agent_data'):                   
                    lat_string=e.find('LatData').text
                    long_string=e.find('LongData').text
                    agent_id = e.find('AgentId').text
                    online_flag = e.find('OnlineFlag').text
                    call_complete = e.find('CallComplete').text  
                    logdiagdata("--Update Agent Pos: "+str(agent_id))                                      
                    #################################################################
                    #             UPDATE THE CURRENT AGENTS POSITION
                    ################################################################# 
                    query_string=("UPDATE agent_current_info SET lat_data=%s,long_data=%s,online_flag=%s WHERE agent_id=%s")
                    data_string=(lat_string,long_string,online_flag,agent_id)
                    cur.execute(query_string,data_string)
                    db.commit()
                    if (call_complete == '1'):
                        query_string=("UPDATE agent_calls SET call_flag=0 WHERE agent_id=%s")
                        data_string=(agent_id)
                        cur.execute(query_string,data_string)
                        db.commit()
                    response = build_response()
                    logdiagdata("--Agent Response Complete")
                #*******************************    
                #NOW CHECK THE LOGIN MESSAGES
                #*******************************
                message_type = e.tag
                if (message_type == 'login_data'):
                    logdiagdata("--Login Message")
                    username = e.find('username').text
                    password = e.find('password').text
                    query_string=("SELECT * from operator_list WHERE username=%s AND password=%s")
                    data_string=(username,password)
                    cur.execute(query_string,data_string)
                    db.commit()
                    login_data = cur.fetchall ()
                    record_exists = cur.rowcount
                    if (record_exists != 0):
                        logdiagdata("--Login Successful")
                        response = build_login_response(username)
                    else:
                        logdiagdata("--Login Failed")
                        logdiagdata(username)
                        logdiagdata(password)
                        response = "<login_data><error>No Such User</error></login_data>"
                    logdiagdata("--Login Response Complete")
                #*******************************    
                #NOW RESPOND WITH AGENT DETAILS
                #*******************************
                message_type = e.tag
                if (message_type == 'get_agent_data'):
                    logdiagdata("--Agent Data Message")
                    responding_agent_id = e.find('agent_id').text
                    logdiagdata("--Agent Data Message. Get details for ID: "+responding_agent_id)
                    query_string=("SELECT * from operator_list WHERE agent_id=%s")
                    data_string=(responding_agent_id)
                    cur.execute(query_string,data_string)                    
                    db.commit()
                    if (cur.rowcount > 0):
                        logdiagdata("--Valid Agent Data")
                        agent_data = cur.fetchall ()
                        for row in agent_data :
                            response = "<agent_details><agent_name>"+row[1]+"</agent_name>"
                            response += "<agent_surname>"+row[2]+"</agent_surname><agent_company>"+row[3]+"</agent_company>"
                            response += "<agent_registration>"+row[8]+"</agent_registration></agent_details>"  
                    else:   
                        logdiagdata("--Invalid Agent Data")
                        response = "<agent_details><error>Error</error></agent_details>"

                clientsocket.send(response)
            else:
                logdiagdata("--Junk received")
        else:
            clientsocket.send("Ahoy!")
            logdiagdata("Ping Request")
        clientsocket.close()

logdiagdata("--End Program")
serversocket.close()
