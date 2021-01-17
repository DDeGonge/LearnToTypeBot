__version__ = '0.1.0'

from gpiozero import Button, LED
from NeuralNet import *
import numpy as np
import threading
import Config as cfg
import os
import time
import math


class KeyboardSensor(object):
    def __init__(self, skip_neural=False):
        self.sensors = [Button(i) for i in cfg.SENSE_PINS]
        self.buffer_size = cfg.window_update_hz * cfg.window_size_s
        self.buffer = [0x00] * self.buffer_size
        self.idle = True
        self.score = 0.5
        self.last_NN_outputs = None

        if not skip_neural:
            self.neuralModel = NeuralNet(model_path=cfg.model_path)
            self.neuralModel.load_weights()

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
        self.logthread = threading.Thread(target=self.update_buffer)#, daemon=True)
        self.logthread.start()

    def stop_sensor_polling(self):
        self.kill_logging.set()
        self.logthread.join()

    def update_score_neural(self):
        buffer_ints = [int(str(r), 16) for r in self.buffer]
        pecking, active = self.neuralModel.Predict(buffer_ints)

        # print(pecking, active)

        if active > cfg.changes_thresh:
            if pecking > cfg.pecking_thresh:
                self.score -= cfg.score_inc_dn
            else:
                self.score += cfg.score_inc_up
            self.normalize_score()

        self.last_NN_outputs = [pecking, active]

    def get_diffs(self, l, r):
        last = [l[0], r[0]]
        diffs = [0, 0]
        for lp, rp in zip(l, r):
            if lp != last[0]:
                diffs[0] += 1
            if rp != last[1]:
                diffs[1] += 1
            last = [lp, rp]

        return diffs

    def update_score(self):
        ints = [int(str(i), 16) for i in self.buffer]
        l = [int(k / 16) for k in ints]
        r = [k % 16 for k in ints]

        diffs = self.get_diffs(l, r)

        # print(l)
        # print(r)
        # print(sum(l) + sum(r), sum(diffs))
        sumcnt = (sum(l) + sum(r)) / 2

        if sum(diffs) / 2 < cfg.changes_thresh or sumcnt < cfg.idle_sum_thresh:
            self.idle = True
        elif sumcnt < cfg.peck_sum_thresh:
            self.idle = False
            self.score -= cfg.score_inc_dn
        else:
            self.idle = False
            self.score += cfg.score_inc_up

        self.normalize_score()

    def normalize_score(self):
        self.score = 0 if self.score <= 0 else self.score
        self.score = 1 if self.score >= 1 else self.score

    def get_score(self):
        return self.score

    def set_score(self, newscore):
        self.score = newscore

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

    def buffer_dump(self):
        return self.buffer
   

class LEDs(object):
    def __init__(self):
        self.leds = [LED(i) for i in cfg.LED_PINS]
        self.all_leds_off()
        self.last_strobe = 0
        self.ledthread = None

    def time_passed(self, timereq):
        return (time.time() - self.last_strobe) > timereq

    def all_leds_off(self):
        [l.off() for l in self.leds]

    def strobe(self, strobetime_s = 1):
        if self.ledthread is not None:
            self.ledthread.join()  # Join old thread if needed
        self.last_zap = time.time()
        self.ledthread = threading.Thread(target=self._strobe_thread, args=(strobetime_s,))
        self.ledthread.start()

    def _strobe_thread(self, runtime_s):
        tstart = time.time()
        self.last_strobe = tstart
        stobe_delay = 1 / (2 * cfg.led_strobe_hz)
        while time.time() - tstart < runtime_s:
            self.leds[0].on()
            self.leds[1].off()
            time.sleep(stobe_delay)
            self.leds[0].off()
            self.leds[1].on()
            time.sleep(stobe_delay)
        self.all_leds_off()


class Zapper(object):
    def __init__(self):
        self.zap = LED(cfg.SHOCK_PIN)
        self.zap.off()
        self.zapthread = None
        self.last_zap = 0

    def time_passed(self, timereq):
        return (time.time() - self.last_zap) > timereq

    def zap_it(self, zaptime_s = 1):
        if self.zapthread is not None:
            self.zapthread.join()  # Join old thread if needed
        self.last_zap = time.time()
        self.zapthread = threading.Thread(target=self._zap_thread, args=(zaptime_s,))
        self.zapthread.start()

    def _zap_thread(self, zaptime):
        tstart = time.time()
        self.zap.on()
        while time.time() - tstart < zaptime:
            time.sleep(0.1)
        self.zap.off()
