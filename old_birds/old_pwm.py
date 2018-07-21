    def pwm_loop(self, off_sleep = 0.1, Hz = 500, on_sleep = 0.01, signal_t = 300, dc = 50):
        """self.cycle_t shouldn't be defined in this function, but
        it uses these values, which aren't necessary for the class as a whole.
        """
        if hasattr(self.p, 'start') == False:
            self.p = GPIO.PWM(self.LED, Hz)
        else:
            self.p.ChangeFrequency(Hz)
        self.p.start(0)
        t = timeit.default_timer()
        nt = t
        self.cycle_t = on_sleep + off_sleep
        while nt - t < signal_t:
            time.sleep(off_sleep)
            self.p.ChangeDutyCycle(dc)
            time.sleep(on_sleep)
            self.p.ChangeDutyCycle(0)
            nt = timeit.default_timer()

        self.p.stop()
