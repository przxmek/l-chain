import requests
import xml.etree.ElementTree as ET
import time

def get_power_consumption(socket):
    socketId = socket.homematicBillingId
    print("Homematic: getting power consumption for socket: " + socket.socketId + " homematicId: " + socketId)
    #send a request to the homematic gateway xml-api (https://github.com/hobbyquaker/XML-API)
    response_socket = requests.get('http://172.16.50.187/config/xmlapi/state.cgi?datapoint_id=' + socketId ,timeout=3)
    #parse the xml response from the homematic gateway xml-api
    root_socket = ET.fromstring(response_socket.text)
    #read the value for ENERGY_COUNTER from the XML, child.attrib['value']

    for child in root_socket:
        return child.attrib['value']

    return '0.0'


#
# #read all four socket measurements (ELV Homematic DIN rail switch actuator with power measurement HM-ES-PMSw1-DR)
# measurements = ['1585','1635','1535','1472']
# ENERGY_COUNTER  = [0.0,0.0,0.0,0.0]
#
# for i in range(0, 4):
#     #send a request to the homematic gateway xml-api (https://github.com/hobbyquaker/XML-API)
#     response_socket = requests.get('http://172.16.50.187/config/xmlapi/state.cgi?datapoint_id=' + measurements[i],timeout=3)
#     #parse the xml response from the homematic gateway xml-api
#     root_socket = ET.fromstring(response_socket.text)
#     #read the value for ENERGY_COUNTER from the XML, child.attrib['value']
#     for child in root_socket:
#         ENERGY_COUNTER[i] = child.attrib['value']
#         print(measurements[i] + ' = ' + ENERGY_COUNTER[i])

#switch on the socket
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1530&new_value=true',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1467&new_value=true',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1630&new_value=true',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1580&new_value=true',timeout=3)
#switch off the socket
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1530&new_value=false',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1467&new_value=false',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1630&new_value=false',timeout=3)
#r = requests.get'http://172.16.50.187/config/xmlapi/statechange.cgi?ise_id=1580&new_value=false',timeout=3)
