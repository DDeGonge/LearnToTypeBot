#!/usr/bin/env python3

__version__ = '0.1.0'

import time
import argparse
import Config as cfg
# from CameraDriver import *
from SpeakerDriver import *
from HWDriver import *
from NeuralNet import *
from UI import *


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

def main_ui():
    parser = argparse.ArgumentParser(description='Learn to type, the easy way.')
    parser.add_argument('-m', type=int, default=0, help='Operational Mode - 0: Standard, 1: TBD, 2: TBD')
    args = parser.parse_args()

    # try:
    s = Speaker()
    # c = Camera()
    k = KeyboardSensor(skip_neural=False)
    l = LEDs()
    z = Zapper()
    # c.start()


    # Enter operational mode
    if cfg.DEBUG_MODE:
        print('Starting...')

    # Set up window
    screen = pygame.display.set_mode((450, 300))
    # pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
    pygame.display.set_caption("Learn To Type!")
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    clock = pygame.time.Clock()

    # Initialize all screens
    s_homescreen = Homescreen(s)
    s_learn = Learn(s, k, l, z)
    s_timetrial = TypeGame(s, l, z, hard_words=False, accuracy_mode=False)
    s_hardtimetrial = TypeGame(s, l, z, hard_words=True, accuracy_mode=False)
    s_accuracy = TypeGame(s, l, z, hard_words=False, accuracy_mode=True)
    s_dumb = Dumb(s)

    # Add page connections
    s_homescreen.attach_action_to_button('learn', s_learn)
    s_homescreen.attach_action_to_button('timetrial', s_timetrial)
    s_homescreen.attach_action_to_button('hardtimetrial', s_hardtimetrial)
    s_homescreen.attach_action_to_button('endless', s_accuracy)
    s_homescreen.attach_action_to_button('dumb', s_dumb)

    # Attach back buttons to all pages
    for page in [s_learn, s_timetrial, s_hardtimetrial, s_accuracy, s_dumb]:
        page.attach_action_to_button('back', s_homescreen)

    # Initialize active screen as homescreen
    active_screen = s_homescreen

    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                action = active_screen.event_handler(event)
                if action is not None:
                    active_screen = action
                    active_screen.reset()
        screen.fill((255,255,255))

        active_screen.display_screen(screen)

        pygame.display.update()
        clock.tick(5)
    

def print_sensors():
    # ledobj = LEDs()
    # while True:
    #     _ = input("EEEEEEE: ")
    #     ledobj.strobe(3)
    kbs = KeyboardSensor()
    kbs.start_sensor_polling()
    while True:
        # print(kbs.read_sensors())
        kbs.update_score_neural()
        print(kbs.get_score())
        time.sleep(0.04)

def strobe():
    l = LEDs()
    l.strobe()

def record():
    import csv
    kbs = KeyboardSensor()
    _ = input("Press enter to begin...")
    kbs.start_sensor_polling()
    time.sleep(7)

    newfile = open('logfile.csv', 'a+')
    csvfile = csv.writer(newfile)
    try:
        while True:
            vals = [0] + kbs.buffer_dump()
            print(vals)
            csvfile.writerow(vals)
            time.sleep(0.04)
    finally:
        newfile.close()

if __name__=='__main__':
    main_ui()
    # main()
    # record()
    # strobe()
    # print_sensors()
