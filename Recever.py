from microbit import *

import radio
radio.config(group=23)
radio.on()
direction = "-"
class KMotor:
    # Motor Directions
    FORWARD = 0
    REVERSE = 1
 
    # Motor Selectors
    MOTOR_1 = 0
    MOTOR_2 = 1
 
    def __init__(self):
        """
        Turn off both motors and clear the display
        """
        self.motor_off(KMotor.MOTOR_1)
        self.motor_off(KMotor.MOTOR_2)
 
    def motor_on(self, motor, direction, speed=100):
        """
        Turn motor with the given direction and speed.
        If speed is out of range, the NO image will
        be displayed and no motor will be turned on.
        :param motor: KMotor.MOTOR1 or KMotor.Motor2
        :param direction: KMotor.FORWARD or KMOTOR.REVERSE
        :param speed: 0 - 100
        :return:
        """
        # check speed is within range, not in range set to 100
        if not 0 <= speed <= 100:
            speed = 100
 
        # speed needs to be scaled from 0-100 to 0-1023
        speed = self._scale(speed)
 
        # Move Motor Forward
        if direction == KMotor.FORWARD:
            if motor == KMotor.MOTOR_1:
                pin8.write_analog(speed)
                pin12.write_digital(0)
            elif motor == KMotor.MOTOR_2:
                pin0.write_analog(speed)
                pin16.write_digital(0)
 
        # Move Motor In Reverse
        else:
            if motor == KMotor.MOTOR_1:
                pin12.write_analog(speed)
                pin8.write_digital(0)
            elif motor == KMotor.MOTOR_2:
                pin16.write_analog(speed)
                pin0.write_digital(0)
 
    def motor_off(self, motor):
        """
        Place motor in coast mode
        :param motor: KMotor.MOTOR1 or KMotor.Motor2
        :return:
        """
        if motor == KMotor.MOTOR_1:
            pin8.write_analog(0)
            pin12.write_analog(0)
        else:
            pin0.write_analog(0)
            pin16.write_analog(0)
 
    def motor_brake(self, motor):
        """
        Brake the selected motor.
        :param motor:
        :return:
        """
        if motor == KMotor.MOTOR_1:
            pin8.write_digital(1)
            pin12.write_digital(1)
        else:
            pin0.write_digital(1)
            pin16.write_digital(1)
 
    def _scale(self, value):
        """
        Scale the speed from 0-100 to 0-1023
        :param value: 0-100
        :return: scaled speed
        """
        new_value = (1023 / 100) * value
        return int(new_value)
theBoard = KMotor()    
while True:
    # turn motor 1 on in forward for 1 second and turn it off
    #theBoard.motor_on(theBoard.MOTOR_1, theBoard.FORWARD)
    #sleep(1000)
    #theBoard.motor_off(theBoard.MOTOR_1)
    #receiver_compass_x = compass.heading()
    message = radio.receive()
    x_strength = accelerometer.get_x()
    #message = "123456789"
    if message:
        direction = message[0:1]
        sender_accelerometer = int(message[1:5])
        sender_compass_x = int(message[5:9])
        speed = int(sender_accelerometer / 8)
        direction_value_x = abs(sender_compass_x - x_strength)
        if 330 > direction_value_x > 180:
            if sender_compass_x < x_strength:
               theBoard.motor_on(theBoard.MOTOR_2, theBoard.FORWARD,15)
            elif sender_compass_x > x_strength:
                theBoard.motor_on(theBoard.MOTOR_1, theBoard.FORWARD,15)
        elif 30 < direction_value_x <= 180:
            if sender_compass_x > x_strength:
                theBoard.motor_on(theBoard.MOTOR_2, theBoard.FORWARD,15)
            elif sender_compass_x < x_strength:
                theBoard.motor_on(theBoard.MOTOR_1, theBoard.FORWARD,15)
        else:
            if direction == "F":
                theBoard.motor_on(theBoard.MOTOR_1, theBoard.FORWARD,speed)
                theBoard.motor_on(theBoard.MOTOR_2, theBoard.FORWARD,speed)
            elif direction == "R":
                theBoard.motor_on(theBoard.MOTOR_1, theBoard.REVERSE,speed)
                theBoard.motor_on(theBoard.MOTOR_2, theBoard.REVERSE,speed)
            elif direction == "-":
                theBoard.motor_off(theBoard.MOTOR_1)
                theBoard.motor_off(theBoard.MOTOR_2)
