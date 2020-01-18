# Raspberry Pi3 Traffic Control Front End
# Using Flask Web Server and Python

import RPi.GPIO as GPIO
import time

from flask import Flask, render_template, request
app = Flask(__name__)

#config GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#status GPIO; must be consistent with Back End Program
iReq=12
oNT=17
oSS=27
oPD=22
#must put the setup the same as Front End of program
GPIO.setup([oNT,oSS,oPD,iReq], GPIO.OUT)


#global variable to recode requested mode:
#value: '','Normal_Traffic','Stops_Sign','Power_Down'
#'' is used at system start (power down)
#'' is used in power down
reqMod = ''
#global variable to recode progress:
#value: ''(complete), 'Switch to ', 'Switching to '(rare when transition fast)
proGress = ''
#global variable for message:
#value: 'Select a button', 'Must confirm status..', 'Traffic lights powered down'
myText = 'Select a button..'

def chkStatGPIO():
    global reqMod
    global proGress
    global myText
    myText = 'Select a button..'
    reqMod = ''
    
    if GPIO.input(iReq)==1:
        proGress = 'Switching to '
    else:
        proGress = ''
        
    if GPIO.input(oNT)==1:
        reqMod = 'Normal_Traffic'
    if GPIO.input(oSS)==1:
        reqMod = 'Stop_Sign'
    if GPIO.input(oPD)==1:
        reqMod = 'Power_Down'
        #if already in Power Down mode
        if proGress == '':
            myText = 'Traffic lights powered down'
    # when back end program first start
    # iReq==0,oNT==0,oSS==0,oPD==0
    # therefore reqMod=='',proGress=='', myText=='Select a button..'
    if reqMod == '':
        myText = 'Traffic lights powered down'
    return
        
    
#web page initialization: update status
#only used at very beginning
@app.route('/')
def index():
    global reqMod
    global proGress
    global myText
    
    #check Status GPIO
    chkStatGPIO()
    
    templateData = {'rMode':reqMod,'prog':proGress, 'note': myText}
    return render_template('index.html', **templateData)

#interactive web page
#will have three request from web page:
#[1] NormalTraffic [2] StopSign [3] PowerDown
#This section create hardware interrupt and update web page

@app.route('/<selected>')
def do(selected):
    global reqMod
    global proGress
    global myText
    
    #check Status GPIO
    chkStatGPIO()
    
    if selected == "NormalTraffic":
        if reqMod != 'Normal_Traffic':
            reqMod = 'Normal_Traffic'
            proGress = 'Switch to '
            GPIO.output([oNT,oSS,oPD,iReq],[1,0,0,1])

    if selected == "StopSign":
        if reqMod != 'Stop_Sign':
            reqMod = 'Stop_Sign'
            proGress = 'Switch to '
            GPIO.output([oNT,oSS,oPD,iReq],[0,1,0,1])
 
    if selected == "PowerDown":
        if reqMod != 'Power_Down':
            reqMod = 'Power_Down'
            proGress = 'Switch to '
            GPIO.output([oNT,oSS,oPD,iReq],[0,0,1,1])
            myText = 'Must confirm status..'
            
    templateData = {'rMode':reqMod,'prog':proGress, 'note': myText}
    return render_template('index.html', **templateData )


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
