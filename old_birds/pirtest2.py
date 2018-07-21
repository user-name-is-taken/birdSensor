import RPi.GPIO as GPIO
import time
import os
import picamera
#import TWEETER2
camera=picamera.PiCamera()

def pir_loop(pic_group_name):
    sensor = 4

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor,GPIO.IN, GPIO.PUD_DOWN)

    previous_state ='LOW'
    current_state ='LOW'
    k=0
    pic_name="bird.jpg"#doesn't have to be redefined because pic is deleted

    while k<10:
        time.sleep (0.1)
        previous_state = current_state
        current_state= GPIO.input (sensor)
        if current_state != previous_state and current_state:
            time.sleep(.5)
            previous_state=current_state
            current_state=GPIO.input(sensor)
            if current_state:
                k+=1
                take_pic(pic_name)
                new_state ='HIGH'  if current_state else 'LOW'
                TWEETER2.tweet(pic_name)
                os.remove(pic_name)
                time.sleep(5)
                current_State='LOW'

def take_pic(pic_name):
    """takes a picture with the name pic_name"""
    try:
        pic_name=str(pic_name)
    except ValueError:
        print "need to enter a string"
    pic_name=pic_name

    camera.capture(pic_name)
    return

if __name__=="__main__":
    time.sleep(30)
    pir_loop("bird-")
        

