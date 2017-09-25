# chg Serial Command to read Com port from file
# To add discard if ip address !right format, same for other user inputs
# To add debug msg or error msg or "missing files etc" msg to 'Error_Log.txt'

import os
import subprocess
import time
import datetime
import shutil
import serial
import serial.tools.list_ports
import tkinter as tk
import tkinter.font
from tkinter import simpledialog
from tkinter import messagebox
import signal

IPAddress_FileName = 'CSCS_Config_IPV4.txt'
PingFreq_FileName = 'CSCS_Config_PingFreq.txt'
PingResults_DeleteDaysFileName = 'CSCS_Config_DaysBeforeDelete.txt'
PingResults_SaveFileName = 'CSCS_Ping_Results.txt'
ArduinoComPort_FileName = 'CSCS_Config_SendingDevComPort.txt'
pingTreshold_FileName = 'CSCS_Config_PingTreshold.txt'
ErrLog_FileName = 'CSCS_Error_Log.txt'

arduinoComPort=0
pingTime_Index = 0
pingTime_Ave = 0
temp = ''
#how many seconds before ping should be sent
timeElapse = 60.0         # default is 60s
timePrev = 0.0
timeNow = 0.0
pingLogDaysB4Deleting = 395  # log will be overwritten after this treshold is exceeded, default: 395
dateTime_Today = datetime.datetime.now()
dateTime_DeleteDay = dateTime_Today + datetime.timedelta(days=pingLogDaysB4Deleting) # default

pingTreshold = 1 # default
successivePingCount = 0

def exitProgram():
    # next cmd requires import time,os,signal
    os.kill(os.getpid(),signal.SIGTERM)

def SetArduinoComPort():
    global arduinoComPort

    tempPath = ''
    arduinoComPort = ''
    tempPath = os.path.join(os.getcwd(),ArduinoComPort_FileName)
    if os.path.isfile(tempPath):
        # file exists
        tempFile = open(ArduinoComPort_FileName)
        arduinoComPort = tempFile.readline()
        tempFile.close()
        #print('com port arduino is: '+ arduinoComPort)
    else:
        arduinoComPort = 'None'

def SetTimeElapse():
    global timeElapse
    tempPath = ''
    tempPath = os.path.join(os.getcwd(),PingFreq_FileName)
    if os.path.isfile(tempPath):
        # TimeFreq file exists, if not, just use default TimeElapse value
        tempFile = open(PingFreq_FileName)
        timeElapse = float(tempFile.readline())
        #print('timeElapse is: ' + str(timeElapse))
        tempFile.close()

def SetPingLogDeleteDays():
    global pingLogDaysB4Deleting
    global dateTime_DeleteDay
    tempPath = os.path.join(os.getcwd(),PingResults_DeleteDaysFileName)
    if os.path.isfile(tempPath):
        # if!exist, use default values
        tempFile = open(PingResults_DeleteDaysFileName)
        pingLogDaysB4Deleting = int(tempFile.readline())
        dateTime_DeleteDay = dateTime_Today + (datetime.timedelta(days=pingLogDaysB4Deleting))
        #print('Time before Log will be overwritten is : ' + str(pingLogDaysB4Deleting))
        #print('\n date is: ' + str(dateTime_DeleteDay) )
        tempFile.close()

def SetPingTreshold():
    global pingTreshold
    tempPath = ''
    tempPath = os.path.join(os.getcwd(),pingTreshold_FileName)
    if os.path.isfile(tempPath):
        tempFile = open(pingTreshold_FileName)
        pingTreshold = int(tempFile.readline())
        #print('pingTreshold: {}'.format(str(pingTreshold)));
        tempFile.close()

def SavePingResults(ipAddress, avePingTime, result):
    tempFile = ''
    tempContent = ''
    tempPath = ''

    tempPath = os.path.join(os.getcwd(),PingResults_SaveFileName)
    if os.path.isfile(tempPath):
        # save file exists
        tempFile = open(PingResults_SaveFileName)
        tempContent = tempFile.readline()
        tempFile.close()

        # if not blank
        if tempContent!= '':
            tempFile = open(PingResults_SaveFileName,'a')

    else:
        tempFile = open(PingResults_SaveFileName,'w')


    #tempFile.write(ipAddress +', '+ str(pingTime_Ave) +', '+ str(result)+'\n')
    tempFile.write(str( datetime.datetime.fromtimestamp(timeNow)) +', '+ ipAddress +', '+ str(avePingTime) +', '+ result+'\n')
    tempFile.close()

# =======================================================================
# =======================================================================
#                       PingTarget()
# =======================================================================
# =======================================================================
def PingTarget():
    # get IP Address from txt file 'CSCS_IP Address' and set var
    cscsPath = os.path.join(os.getcwd(),IPAddress_FileName)
    #print('\n'+str(cscsPath))
    cscsIPAddress_File = open(cscsPath)
    cscsIPAddress = cscsIPAddress_File.read().splitlines()
    #print('\n'+str(cscsIPAddress))

    for ipAddress in cscsIPAddress:
        #print('\n'+ ipAddress)
        if os.name == 'nt':
            #print('---------------------------------------------------------------------------');
            previousPingResult = '' # last ping result
            pingResult = '' # Ping result

            # Loop noOfPingB4GetResult
            for x in range(0, pingTreshold):
                #print('\n pingTreshold is: ' +str(pingTreshold))
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                proc = subprocess.Popen(['ping', '-n', '1', ipAddress],stdout=subprocess.PIPE, startupinfo=startupinfo)
                stdout, stderr = proc.communicate()

                # only 1 ping is sent, hence success?0% loss:100% loss
                # ipaddress, date/time, miliseconds, 1 / 0
                pingFail = False
                if int(proc.returncode) == 0:
                    # the "process" of pinging is successful,
                    # REGARDLESS of whether the destination IP was reacheable or NOT
                    #print('proc.returncode: {}'.format(proc.returncode));
                    #print('\n {} --> Success'.format(ipAddress))
                    #print('\n Successful ping output:')
                    #print(stdout.decode('ASCII'))
                    temp = stdout.decode('ASCII')
                    if 'Average =' in temp:
                        pingTime_Index = temp.index('Average =')
                        #print('\n'+ str(pingTime_Index))
                        pingTime_Ave = (str(temp[pingTime_Index+10:pingTime_Index+13])).strip()
                        #print('\n'+str(pingTime_Ave))
                        pingResult = 'SUCCESS'
                    else:
                        pingFail = True
                else:
                    pingFail = True

                if pingFail:
                    # ping has failed
                    #print('\n {} --> Fail'.format(ipAddress))
                    #print(stdout.decode('ASCII'))
                    pingTime_Ave = 0
                    pingResult = 'FAILURE'

                # Check if previousPingResult NOT blank (is not first loop)
                if previousPingResult is not '':
                    # Check if previousPingResult NOT equal to pingResult
                    if previousPingResult != pingResult:
                        # Reset x
                        x = 0

                # Set previousPingResult
                previousPingResult = pingResult

            #print('---------------------------------------------------------------------------');
            # Final result
            if pingResult == 'SUCCESS':
                # Result is SUCCESS
                # Save to result Log
                SavePingResults(ipAddress, pingTime_Ave, 'OK')
                # Send SUCCESS command to arduino
                arduino.write(b'\x03')
            else:
                # Result is FAILURE
                # Save to result Log
                SavePingResults(ipAddress, pingTime_Ave, 'NO')
                # Send FAILURE command to arduino
                arduino.write(b'\x05')


            #print('---------------------------------------------------------------------------');
        else:
            print('\n This is not a Windows OS. Command failed.')

# =======================================================================
# =======================================================================
#                       main()
# =======================================================================
# =======================================================================

# Set vars
tempFile = ''
tempPath = ''
tParam = ''

# Set value by config file
SetPingLogDeleteDays()
SetTimeElapse()
SetPingTreshold()

# Set Arduino Com Port
SetArduinoComPort()
#print('arduino com port is: ' + str(arduinoComPort))
tParam = arduinoComPort.strip('\t\r\n')
tParam = tParam[0:5]
#tParam = "\'"+tParam+"\'," + '9600,timeout=0,parity=serial.PARITY_EVEN, rtscts=1'
#print(tParam)
#input()
if 'None' not in arduinoComPort:
    #arduino = serial.Serial('COM13', 9600, timeout=0,parity=serial.PARITY_EVEN, rtscts=1)
    arduino = serial.Serial(tParam, 9600, timeout=0,parity=serial.PARITY_EVEN, rtscts=1)
    #print(tParam)
    time.sleep(1)
#print(timeElapse)

z = 0

# App Loop
while True:
    # Get time now
    timeNow = time.time()
    #print('timeNow:  '+str(timeNow))
    #print('timePrev: '+str(timePrev))
    #print('diff: ' + str((timeNow-timePrev)))
    #time.sleep(3)
    if ((timeNow-timePrev) > timeElapse):
        PingTarget() # this fn will also save results to log file
        timePrev = time.time()

        #print('dateTime_Today is: '+str(dateTime_Today))
        #print('\n dateTime_DeleteDay is: '+str(dateTime_DeleteDay))
        #print('\n dateTime_Today>dateTime_DeleteDay is: ' + str(dateTime_Today>dateTime_DeleteDay))
        if dateTime_Today>dateTime_DeleteDay:
            #print('time to delete log')
            tempPath = os.path.join(os.getcwd(),PingResults_SaveFileName)
            if os.path.isfile(tempPath):
                # save file exists
                try:
                    os.unlink(tempPath)
                except PermissionError as e:
                    z = z+1
