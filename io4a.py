# Raspberry Pi 3 Traffic Light Back End Program
# Should run this beofre Front End Program
# Control + C to enb
# please notice the GPIO pins are not cleaned up

import RPi.GPIO as GPIO
import time

#config GPIO
GPIO.setmode(GPIO.BCM)
#disable the warnings that multiple scrips using the same GPIO pins
#liability on one's own
GPIO.setwarnings(False)

#config Traffice Light channel; reference Raspberry Pi pin map
#these pins connect to relays
mainG = 13
mainY = 19
mainR = 26
auxG = 21
auxY = 20
auxR = 16
chanList = [mainG,mainY,mainR,auxG,auxY,auxR]
#config sequence
#seq1 = [1,0,0,0,0,1]
#seq2 = [0,1,0,0,0,1]
#seq3 = [0,0,1,0,0,1]
#seq4 = [0,0,1,1,0,0]
#seq5 = [0,0,1,0,1,0]
#seq6 = [0,0,1,0,0,1]
#seq = [[seq1,seq2,seq3],[seq4,seq5,seq6]]
#initialize GPIO chanel
#GPIO.setup(chanList, GPIO.OUT)
#initialize output chanel to off state where GPIO.LOW=0
#GPIO.output(chanList,0)

#++ version oi4a.py
#++ mechanical relay, low is active and high is idle
#config sequence
seq1 = [0,1,1,1,1,0]
seq2 = [1,0,1,1,1,0]
seq3 = [1,1,0,1,1,0]
seq4 = [1,1,0,0,1,1]
seq5 = [1,1,0,1,0,1]
seq6 = [1,1,0,1,1,0]
seq = [[seq1,seq2,seq3],[seq4,seq5,seq6]]
#initialize GPIO chanel
GPIO.setup(chanList, GPIO.OUT)
#initialize output chanel to off state where GPIO.LOW=0
GPIO.output(chanList,1)

#status GPIO; must be consistent with Front End program
oReq=12
iNT=17
iSS=27
iPD=22
#must put the setup the same as Front End of program
GPIO.setup([iNT,iSS,iPD,oReq], GPIO.OUT)
#initialize
GPIO.output([iNT,iSS,iPD,oReq], 0)

while True:
    #Normal Traffic
    while GPIO.input(iNT)==1:
        #notify in Normal traffic mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
        for iseq in seq:
            #for Green light
            GPIO.output(chanList, iseq[0])
            endTime = time.time() + 5
            while time.time() < endTime:
                time.sleep(0.5)
                #if new mode requested, break from while timing loop
                #note oReq should be 1
                if GPIO.input(iNT)==0:
                    break
            print('Green ', iseq[0], ' ', time.time()-endTime+5)
            #for Yellow light
            GPIO.output(chanList, iseq[1])
            time.sleep(2)
            print('Yellow ', iseq[1])
            #for Red light
            GPIO.output(chanList, iseq[2])
            time.sleep(1)
            print('Red ', iseq[2])
            
            #if new mode requested, break from for sequence loop
            #note oReq should be 1
            if GPIO.input(iNT)==0:
                break

    #Stop Sign
    while GPIO.input(iSS)==1:    
        #notify in Stop Sign mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
        GPIO.output(chanList, seq3)
        time.sleep(1)
        print('flash red')
        #GPIO.output(chanList,0)
        #version4a low is on, high is off
        GPIO.output(chanList,1)
        time.sleep(1)
        print('flash off')
        
    #Power Down
    while GPIO.input(iPD)==1:    
        #notify in Power Down mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
        #GPIO.output(chanList,0)
        #version4a low is on, high is off
        GPIO.output(chanList,1)
        time.sleep(2)
        print('traffic light off')

    #give system 0.5sec to do something else
    time.sleep(0.5)

#Just put below script here. User Control+C to break the program
print('Shut down. Release GPIO ports..')
GPIO.cleanup()

#========
#run by elapsed time; use 5sec as example
#endTime = time.time() + 5
#GPIO.output(chanList, seq[0][0])
#print(seq[0][0])
#while time.time() < endTime:
#    time.sleep(0.01)
#print(time.time()-endTime+5)
#print(GPIO.input(chanList[0]),GPIO.input(chanList[1]),GPIO.input(chanList[2]),
#      GPIO.input(chanList[3]),GPIO.input(chanList[4]),GPIO.input(chanList[5]))
