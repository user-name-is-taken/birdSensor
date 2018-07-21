import timeit
import time
import threading
class watchdog(object):
    """this whole thing will be in a thread."""
    def __init__(self):
        """ctt= cycles to timeout"""
        self.t=timeit.default_timer()
        self.tot=3
    def cb(self):
        """needs to be tested, ideally self.t will update with every edge
meaning, ct==self.t only if an edge didn't happen. Only works if ~15 threads
can run at once.
This doesn't work. need to separate the updating of self.t from the test loop"""
        #tot=self.hard.cycle_t*1000*mp #timeout time
        ct=timeit.default_timer()
        self.t=ct
        threading.Thread(target=self.event_timer,args=(ct,)).start()        
            
    def event_timer(self,ct):
        """this one should watch for updates to be older than sec seconds"""
        time.sleep(self.tot)
        print ct
        if ct==self.t:
            print "picture taken", ct, "  ",self.t
