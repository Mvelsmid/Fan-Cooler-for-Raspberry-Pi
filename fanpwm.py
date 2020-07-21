#!/usr/bin/python
# Autor Kiker
# verzia 1.2

import time
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
import RPi.GPIO as GPIO

Teplotamin=50  #minimalna nastavena teplota /ventilator nepojde ak bude nizsia
pin = 4        #nastavenie pinu BCM
cakaj = 14      #nastavenie opakovania kontroly teploty
Hz = 35        #frekvencia PWM
advanc = 1     # 0 vypnute - 1 zapnute  /znizenie teploty na minimalnu
R = 3          # rozdiel v minimalne nastavenej teplote od vychladenia /ak je zapnute advanc   
RT = 30        # cas v sekundach na porovnanie teploty

# konfiguracia 

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

fan=GPIO.PWM(pin,Hz)
fan.start(0);
fspeed=0
i=0
s=0.0
s2=0.0
T1=Teplotamin

# riadenie ventilatora

try:
    while 1:
        tempfile=open("/sys/class/thermal/thermal_zone0/temp","r")
        ctemp=float(tempfile.read())/1000
        tempfile.close()
        T=Teplotamin*0.01
        temp=ctemp*100
        s=ctemp/100-T
        speed=ctemp/100+s+s2
        fspeed=speed*100
        if(fspeed > 100):      
                   fspeed=100 
        
        if(i >= 1):
            ctempold=ctemp
            T1=Teplotamin-R
        
        i=i+1 
          
        if(advanc < 1):
                T1=Teplotamin
        
        if(ctemp <= T1):
            fspeed = 0
            s2=0.0
            i=0
            T1=Teplotamin
                        
        T2=i*cakaj
        
        if(T2 >= RT):
                i=0
                if(ctempold <= ctemp):
                        s2=s2+0.05
                        ctempold=ctemp
                        
                        if(ctemp/100+s+s2 > 1): 
                            s2=s2-0.05  
                            
                elif(ctempold - ctemp < 1):
                        s2=s2+0.05
                        ctempold=ctemp
                        
                        if(ctemp/100+s+s2 > 1): 
                            s2=s2-0.05  
                            
        else:
                s=0.0    
            
    
        fan.ChangeDutyCycle(fspeed)
        time.sleep(cakaj)


except(KeyboardInterrupt):
    print('prerusenie CTRL+C')
    GPIO.cleanup()
    sys.exit()
    
