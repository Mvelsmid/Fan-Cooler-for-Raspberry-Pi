#!/usr/bin/python
# Autor M. Velsmid
# version: 1.1

import time
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
import RPi.GPIO as GPIO

Teplotamin = 46  # setup min. temerature
pin = 4          # set pin BCM
cakaj = 10       # repeat control temerature
Hz = 30          # frekquency PWM
advanc = 0       # 0 off - 1 on  /decrease of temperature to min.
R = 3            # difference min. temepratre from cooling down  /it must be turned on advanc   
RT = 120          # time in seconds to re-compare the temperature

# config
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

fan=GPIO.PWM(pin,Hz)
fan.start(0);
fspeed=0
i=0
s=0.0
s2=0.0
T1=Teplotamin

# fan control
try:
    while 1:
        tempfile=open("/sys/class/thermal/thermal_zone0/temp","r")
        #tempfile=open("temp","r")
        ctemp=float(tempfile.read())/1000
        tempfile.close()
        #T=float(Teplotamin*0.01)
        T=Teplotamin*0.01
        temp=ctemp*100
        
        #s=float(ctemp/100-T)
        s=ctemp/100-T
        speed=ctemp/100+s+s2
        fspeed=speed*100
        
        if(i >= 1):
            ctempold=ctemp
            T1=Teplotamin-R
            #print('fan on',time.ctime())
        
        i=i+1   
        if(advanc < 1):
                T1=Teplotamin
        
        if(ctemp <= T1):
            fspeed = 0
            s2=0.0
            i=0
            T1=Teplotamin
            #print('fan off',time.ctime())
            
        #print('ctemp:',ctemp)
        #print('ctempold:',ctempold)
        #print('T1:',T1)
        #print('fspeed:',fspeed)
        #print('s:',s)
        #print('i:',i)
       
        T2=i*cakaj
        
        if(T2 >= RT):
                i=0
                if(ctempold <= ctemp):
                        s2=s2+0.05
                        ctempold=ctemp
                       # print(time.ctime(),'speed+', s+s2)
                        if(ctemp/100+s+s2 > 1): 
                            s2=s2-0.05  
                           # print(time.ctime(),'speed-', s+s2)  
                elif(ctempold - ctemp < 1):
                        s2=s2+0.05
                        ctempold=ctemp
                       # print(time.ctime(),'speed+', s+s2)
                        if(ctemp/100+s+s2 > 1): 
                            s2=s2-0.05  
                           # print(time.ctime(),'speed-', s+s2) 
  
        else:
                s=0.0  
            
        if(fspeed > 100):
                fspeed=100
        fan.ChangeDutyCycle(fspeed)
        time.sleep(cakaj)


except(KeyboardInterrupt):
    print('break CTRL+C')
    GPIO.cleanup()
    sys.exit()
    
