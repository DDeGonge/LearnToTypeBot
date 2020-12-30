__version__ = '0.1.0'

import time
import argparse
import Config as cfg
from CameraDriver import *
from SpeakerDriver import *
from HWDriver import *


def main():
    parser = argparse.ArgumentParser(description='Learn to type, the easy way.')
    parser.add_argument('-m', type=int, default=0, help='Operational Mode - 0: Standard, 1: TBD, 2: TBD')
    args = parser.parse_args()

    # try:
    s = Speaker()
    c = Camera()
    c.start()

    # Enter operational mode
    if cfg.DEBUG_MODE:
        print('Starting...')


def test():
    # ledobj = LEDs()
    # while True:
    #     _ = input("EEEEEEE: ")
    #     ledobj.strobe(3)
    kbs = KeyboardSensor()
    while True:
        print(kbs.read_sensors())
        time.sleep(0.1)

def strobe():
    l = LEDs()
    l.strobe()

def record():
    import csv
    kbs = KeyboardSensor()
    _ = input("Press enter to begin...")
    kbs.start_sensor_polling()
    time.sleep(7)

    newfile = open('logfile.csv', 'w+')
    csvfile = csv.writer(newfile)
    try:
        while True:
            vals = [0] + kbs.buffer_dump()
            print(vals)
            csvfile.writerow(vals)
            time.sleep(0.1)
    finally:
        newfile.close()

if __name__=='__main__':
    # main()
    # record()
    strobe()
    # test()
