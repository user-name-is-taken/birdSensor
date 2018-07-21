import RPi.GPIO as GPIO
import timeit
#import os
import time
received_signals=dict()#{signal tuple:remote representation}

sensor=4
LED=18
class receiver(object):
    def __init__(self):
        self.full_signal=tuple()
        self.current_state=1#not(GPIO.input(sensor))
        #the not is because the sensor uses 1 to represent off and 0 for on
    def receive(self,channel):
        """used in interrupt
GPIO.add_event_detect(4,GPIO.RISING,callback=k.receive)#bouncetime=0)"""
        t=timeit.default_timer()
        self.current_state=not self.current_state #make sure this is right.
        phase=(t,self.current_state)#asigned so print is fast
        self.full_signal+=(phase,)
        print(phase)
    def append_signal_dict(self):
        """gives the last signal that was sent"""
        name=input("give this signal a name")

        #finds delta_time_signal from full signal
        s=self.full_signal
        dts=map(lambda x:(s[x+1][0]-s[x][0],s[x][1]),range(len(s)-1))
        #delta_time_signal found
        #the above won't do the final off

        #finds last break and cuts out prior signals
        k=lambda x:x if dts[x][0]>.15 else 0#finds the last break between signals
        f=range(len(dts))
        signal_start=max(f,key=k)#performs k on the full signal tuple
        print(dts)
        print(signal_start)
        last_signal=dts[signal_start+1:]#slices the prior signals off
        #found and cut out
        #checks if this is what you want
        print last_signal
        if input("\n is this the signal you want? if so 1"):
            pass
        else:
            print "resend the signal and try again, make sure it's the most recent signal"
            return
        #done checking
        
        #appends the final dict and sets self.full_signal to tuple()
        received_signals[tuple(last_signal)]=name
        self.full_signal=tuple()

k=receiver()        
class sender(object):
    def __init__(self):
        self.make_sendables()
    def make_sendables(self):
        #received signals is a global
        g=dict(zip(received_signals.values(),received_signals.keys()))
        self.sendable_signals=g
    def send(self,signal_name):
        #maybe GPIO.output(not(self.sendable_signals[signal_name][0][1]))
        #as a buffer
        for pulse in self.sendable_signals[signal_name]:
            GPIO.output(LED,pulse[1])#not would be added here
            time.sleep(pulse[0])
        GPIO.output(LED,0)#not(pulse[1]))
def sec_apart_loop(secs,times,delay):
    for s in range(secs):
        time.sleep(.1)
        loop(times,delay)

def loop(times,delay):
    """.0001, 100x"""
    for i in range(times):
        on_off(delay)
        

def on_off(delay):
    g=GPIO.output
    s=time.sleep
    s(delay)
    g(LED,1)
    s(delay)
    g(LED,0)

def close_gpio():
    GPIO.remove_event_detect(sensor)
    GPIO.cleanup()
def open_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor,GPIO.IN,GPIO.PUD_DOWN)
    GPIO.setup(LED,GPIO.OUT,initial=GPIO.LOW)
  
def main():
    #global k
    open_gpio()
    #k=receiver()      
    GPIO.add_event_detect(4,GPIO.BOTH,callback=k.receive)#bouncetime=0)
    #os.popen('sudo python2')

if __name__=="__main__":
    main()
