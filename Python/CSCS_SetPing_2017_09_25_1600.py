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
#PingResults_SaveFileName = 'CSCS_Ping_Results.txt'
SendingDeviceComPort_FileName = 'CSCS_Config_SendingDevComPort.txt'
pingTreshold_FileName = 'CSCS_Config_PingTreshold.txt'

def exitProgram():
    # next cmd requires import time,os,signal
    os.kill(os.getpid(),signal.SIGTERM)

def SelectComPort():
    tStr=''
    cTemp = ''
    iStart=0
    iEnd=0
    tempFile = ''
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        tStr=str(p)
        if 'Arduino' in tStr:
            iStart = tStr.find('(')
            iEnd = tStr.find(')')
            cTemp = tStr[iStart+1:iEnd]
    messagebox.showinfo("Info","Sending Device found at " + cTemp + '\nSaving data now.')
    tempFile = open(SendingDeviceComPort_FileName,'w')
    tempFile.write(cTemp + '\n')
    tempFile.close()

def GetUserInput_IPAddress():
    #cscsIPV4_File = ''
    #cscsIPV4_Content = ''

    #cscsIPv4Adr = input('Please enter IPV4 Address to ping: ');
    cscsIPv4Adr = simpledialog.askstring("Ping Address", "IPv4 address to ping?",parent=win)

    if (cscsIPv4Adr == None) or (cscsIPv4Adr == ''):
        return

    cscsPath = os.path.join(os.getcwd(),IPAddress_FileName)
    if os.path.isfile(cscsPath):
        # save file exists
        cscsIPV4_File = open(IPAddress_FileName)
        cscsIPV4_Content = cscsIPV4_File.readlines()
        cscsIPV4_File.close()

        if cscsIPV4_Content[0] != '':
            cscsIPV4_File = open(IPAddress_FileName,'a')
            cscsIPV4_File.write(cscsIPv4Adr + '\n')
    else:
        cscsIPV4_File = open(IPAddress_FileName,'w')
        cscsIPV4_File.write(cscsIPv4Adr + '\n')

    cscsIPV4_File.close()

def GetUserInput_PingFrequency():
    tempFile = ''
    #cscsPingFreq = input('Please enter number of seconds to elapse before pinging: ')
    cscsPingFreq = simpledialog.askstring("How often to ping?", "No of seconds between pinging?",parent=win)
    if (cscsPingFreq == None) or (cscsPingFreq == ''):
        return

    tempFile = open(PingFreq_FileName,'w')
    tempFile.write(cscsPingFreq + '\n')
    tempFile.close()

def GetUserInput_DaysBeforeDeletePingResults():
    tInput = ''
    tFile = ''
    tInput = simpledialog.askstring("When should log file be overwritten?", "Enter number of days:",parent=win)
    if (tInput == None) or (tInput == '' ):
        return

    tFile = open(PingResults_DeleteDaysFileName,'w')
    tFile.write(tInput + '\n')
    tFile.close()

def GetUserInput_PingTreshold():
    tempFile = ''
    PingTreshold_Result = simpledialog.askinteger("Ping Treshold to confirm result?", "How many similar pings results, to confirm the result?",parent=win)
    if (PingTreshold_Result == None) or (str(PingTreshold_Result) == ''):
        return

    tempFile = open(pingTreshold_FileName,'w')
    tempFile.write(str(PingTreshold_Result) + '\n')
    tempFile.close()

# =======================================================================
# =======================================================================
#                       main()
# =======================================================================
# =======================================================================

#prep GUI
win=tk.Tk()

win.title("CSCS Ping v0.5 by Oneberry Technologies Pte Ltd")
myFont=tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

w = tk.Label(win,text="Please Set", height=1, width=10)
w.grid(row=0,sticky=tk.W)

IPAddress_Btn = tk.Button(win, text='IPv4 Address', font=myFont, command=GetUserInput_IPAddress, bg='bisque2', height=1, width=24)
IPAddress_Btn.grid(row=1,sticky=tk.W)

PingFreq_Btn = tk.Button(win, text='Ping Frequency', font=myFont, command=GetUserInput_PingFrequency, bg='bisque2', height=1, width=24)
PingFreq_Btn.grid(row=2,sticky=tk.NSEW)

SelectComPort_Btn = tk.Button(win, text='Select Com Port', font=myFont, command=SelectComPort, bg='bisque2', height=1, width=24)
SelectComPort_Btn.grid(row=3,sticky=tk.NSEW)

Daysb4Delete_Btn = tk.Button(win, text='Days b4 overwrite Log', font=myFont, command=GetUserInput_DaysBeforeDeletePingResults, bg='bisque2', height=1, width=24)
Daysb4Delete_Btn.grid(row=4,sticky=tk.NSEW)

spacing1_lbl = tk.Label(win,text="", height=1, width=24)
spacing1_lbl.grid(row=5,sticky=tk.NSEW)

pingTreshold_Btn = tk.Button(win, text='Successive Ping Treshold', font=myFont, command=GetUserInput_PingTreshold, bg='bisque2', height=1, width=24)
pingTreshold_Btn.grid(row=6,sticky=tk.NSEW)

spacing3_lbl = tk.Label(win,text="", height=2, width=24)
spacing3_lbl.grid(row=7,sticky=tk.NSEW)

exitButton = tk.Button(win, text='Exit', font=myFont, command=exitProgram, bg='light grey', height=1, width=6)
exitButton.grid(row=8, sticky=tk.E)

tk.mainloop()
