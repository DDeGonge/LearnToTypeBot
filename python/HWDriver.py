__version__ = '0.1.0'

from gpiozero import Button, LED
import threading
import Config as cfg
import os
import time
import math


class KeyboardSensor(object):
    def __init__(self):
        self.sensors = [Button(i) for i in cfg.SENSE_PINS]
        self.buffer_size = cfg.window_update_hz * cfg.window_size_s
        self.buffer = [0x00] * self.buffer_size
        self.idle = True
        self.score = 0.5

    def read_sensors(self):
        return [s.is_pressed for s in self.sensors]

    def get_num_sensors_engaged(self):
        """ Returns n sensors in format 0xab, where a is left sum and b is right """
        allsensors = self.read_sensors()
        left = 4 - sum(allsensors[0:4])
        right = 4 - sum(allsensors[4:8])
        return hex(left*16 + right)

    def start_sensor_polling(self):
        self.score = 0.5
        self.kill_logging = threading.Event()
        self.logthread = threading.Thread(target=self.update_buffer, daemon=True)
        self.logthread.start()

    def stop_sensor_polling(self):
        self.kill_logging.set()
        self.logthread.join()

    def update_score(self):
        ints = [int(str(i), 16) for i in self.buffer]
        l = [int(k / 16) for k in ints]
        r = [k % 16 for k in ints]

        last = [l[0], r[0]]
        diffs = [0, 0]
        for lp, rp in zip(l, r):
            if lp != last[0]:
                diffs[0] += 1
            if rp != last[1]:
                diffs[1] += 1
            last = [lp, rp]

        # print(l)
        # print(r)
        # print(sum(l) + sum(r), sum(diffs))
        sumcnt = (sum(l) + sum(r)) / 2

        if sum(diffs) / 2 < cfg.changes_thresh or sumcnt < cfg.idle_sum_thresh:
            self.idle = True
        elif sumcnt < cfg.peck_sum_thresh:
            self.idle = False
            self.score -= cfg.score_inc
        else:
            self.idle = False
            self.score += cfg.score_inc

        self.score = 0 if self.score <= 0 else self.score
        self.score = 1 if self.score >= 1 else self.score

    def get_score(self):
        return self.score

    def update_buffer(self):
        buffer_i = 0
        time_step_s = 1 / cfg.window_update_hz
        next_step_s = time.time() + time_step_s
        while not self.kill_logging.is_set():
            while time.time() < next_step_s: pass
            self.buffer[buffer_i] = self.get_num_sensors_engaged()
            buffer_i += 1
            buffer_i %= self.buffer_size
            next_step_s += time_step_s
            self.update_score()

    def buffer_dump(self):
        return self.buffer
   

class LEDs(object):
    def __init__(self):
        self.leds = [LED(i) for i in cfg.LED_PINS]
        self.all_leds_off()

    def strobe(self, runtime_s = 2):
        tstart = time.time()
        stobe_delay = 1 / (2 * cfg.led_strobe_hz)
        while time.time() - tstart < runtime_s:
            self.leds[0].on()
            self.leds[1].off()
            time.sleep(stobe_delay)
            self.leds[0].off()
            self.leds[1].on()
            time.sleep(stobe_delay)

        self.all_leds_off()

    def all_leds_off(self):
        [l.off() for l in self.leds]


class Zapper(object):
    def __init__(self):
        self.zap = LED(cfg.SHOCK_PIN)
        self.zap.off()

    def zap_dem(self, zaptime_s = 1):
        self.zap.on()
        time.sleep(zaptime_s)
        self.zap.off()
