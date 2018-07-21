# 2016.09.25 16:13:48 UTC
import RPi.GPIO as GPIO
import timeit
import os
import picamera
import time
import threading
from datetime import datetime
camera = picamera.PiCamera()

class hardware(object):
    """for setting up the hardware"""


    def __init__(self, LED = 18, sensor = 4,FLASH=21):
        self.LED = LED
        self.sensor = sensor
        self.FLASH=FLASH
        self.p = None
        self.cycle_t = 0.1
        self.open_gpio()



    def open_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.FLASH, GPIO.OUT, initial=GPIO.LOW)


    def close_gpio(self):
        GPIO.remove_event_detect(self.sensor)
        if hasattr(self.p, 'stop'):
            self.p.stop()
        GPIO.cleanup()



    def pwm_loop(self, Hz = 10, signal_t = 300, dc = 10):
        """self.cycle_t shouldn't be defined in this function, but
        it uses these values, which aren't necessary for the class as a whole.
        """
        if not(hasattr(self.p, 'start')):
            self.p = GPIO.PWM(self.LED, Hz)
            self.p.start(dc)
        else:
            self.p.ChangeFrequency(Hz)
            self.ChangeDutyCycle(dc)
        time.sleep(signal_t)
        self.p.stop()




class watchdog(object):
    """this whole thing will be in a thread."""


    def __init__(self, hard, pic_limit = 20, ctt = 3):
        """ctt= cycles to timeout"""
        self.t = timeit.default_timer()
        self.hard = hard
        self.tot = ctt * hard.cycle_t
        self.numbPics = 0
        self.pic_limit = pic_limit


    mp = 3

    def cb(self, r):
        """needs to be tested, ideally self.t will update with every edge
        meaning, ct==self.t only if an edge didn't happen. Only works if ~15 threads
        can run at once.
        This doesn't work. need to separate the updating of self.t from the test loop"""
        ct = timeit.default_timer()
        t_t_L_s=ct-self.t #time to last signal, should fix sporatic signals
        self.t = ct
        if t_t_L_s<.5:
            #doesn't execute if time to last signal is longer than 3
            threading.Thread(target=self.event_timer, args=(ct,)).start()



    def event_timer(self, ct):
        """this one should watch for updates to be older than sec seconds"""
        time.sleep(self.tot)
        if ct == self.t:
            print "thread timed. wait_for_event_detect"
            i=datetime.now()
            name='bird'+i.strftime('%Y%m%d-%H%M%S')+".jpg"
            camera.capture(name)
            print "picture taken"
            os.popen("mv /home/pi/birds/"+name+" /home/pi/birds/bird_pics/")
            self.numbPics += 1
            print 'picture moved',
            print ct,
            print '  ',
            print self.t
            GPIO.output(self.hard.FLASH,1)
            time.sleep(.1)
            GPIO.output(self.hard.FLASH,0)
            
            if self.numbPics >= self.pic_limit:
                self.hard.close_gpio()
                
                exit()



h = hardware()

def main():
    global h
    global wd
    try:
        wd = watchdog(h)
        GPIO.add_event_detect(h.sensor, GPIO.RISING, callback=wd.cb)
        h.pwm_loop()
        h.close_gpio()
        camera.close()
    except KeyboardInterrupt:
        h.close_gpio()
        camera.close()


#if __name__ == '__main__':
   # main()

#+++ okay decompyling bird_bot_final.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.09.25 16:13:53 UTC
