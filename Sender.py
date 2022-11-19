# Imports go at the top
from microbit import *

import radio
radio.config(group=23)
radio.on()

def leftPad(str,chr,lenght):
    for i in range(lenght - len(str)):
        str = chr + str
    return str


# Code in a 'while True:' loop repeats forever
while True:
    y_strength = accelerometer.get_y()
    if y_strength > 100:
        direction = "R"
    elif y_strength < -100:
        direction = "F"
    else:
        direction = "-"
    accValue = leftPad(str(abs(y_strength)),"0",4)
    magnet_strength_x = compass.heading()
    comValue = leftPad(str(magnet_strength_x),"0",4)
    Message = direction + accValue + comValue
    if y_strength > 100 :
        display.show(Image.ARROW_S)
    elif y_strength < -100 :
        display.show(Image.ARROW_N)
    else:
        display.show(Image("00000:"
                           "00000:"
                           "99999:"
                           "00000:"
                           "00000:"))
    radio.send(Message)
    # display.scroll(magnet_strength_x)
