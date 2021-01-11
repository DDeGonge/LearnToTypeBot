import pygame
import random
import time
import os
import Config as cfg

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

class WordGenerator():
    def __init__(self, masterlist, minlen = 0, maxlen = 999):
        with open(masterlist) as f:
            allwords = [w.strip('\n') for w in f.readlines()]

        self.wordlist = [w for w in allwords if len(w) <= maxlen and len(w) >= minlen]

    def get_word(self):
        return random.choice(self.wordlist)


class Text:
    def __init__(self, text, x_center, y_center, fsize=12, color=(0,0,0)):
        font = pygame.font.Font('assets/bebas.ttf', fsize)
        self.text_img = font.render(text, True, color)
        x_center -= (self.text_img.get_size()[0] / 2)
        y_center -= (self.text_img.get_size()[1] / 2)
        self.text_pos = (x_center, y_center)

    def draw(self, screen):
        screen.blit(self.text_img, self.text_pos)


class Button:
    def __init__(self, image, x_center, y_center):
        # self.id = button_id
        self.icon = pygame.image.load(image)
        self.location = (x_center, y_center)
        w, h = self.icon.get_size()
        self.rect = pygame.Rect((x_center - (w/2), y_center - (h/2)), (w, h))
        self.action = None

    def attach_action(self, action):
        self.action = action

    def draw(self, screen):
        w, h = self.icon.get_size()
        screen.blit(self.icon, (self.location[0] - (w/2), self.location[1] -  (h/2)))

    def check_collision(self, cur):
        return self.rect.collidepoint(cur)


class Meter:
    def __init__(self, background_img, arrow_img, x_center, y_center, arrow_rotate, arrow_attach, minang = -90, maxang = 90):
        self.bkgd = pygame.image.load(background_img)
        self.arrow = pygame.image.load(arrow_img)
        self.meter_location = (x_center, y_center)
        self.arrow_rotate = arrow_rotate  # Point in arrow image to rotate around
        self.arrow_attach = arrow_attach  # Rotation point for arrow, relative to bkgd center
        self.minangle = minang
        self.maxangle = maxang

        self.img_angle = 90  # To vertical, positive is CW rotated
        self.value = 0

    def draw(self, screen):
        # Draw background
        w, h = self.bkgd.get_size()
        screen.blit(self.bkgd, (self.meter_location[0] - (w/2), self.meter_location[1] -  (h/2)))

        # Draw current meter value with rotated arrow
        value_degs = self.minangle + (self.value * (self.maxangle - self.minangle))
        rotation_degs = - value_degs + self.img_angle

        w, h       = self.arrow.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(rotation_degs) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        pivot        = pygame.math.Vector2(self.arrow_rotate[0], -self.arrow_rotate[1])
        pivot_rotate = pivot.rotate(rotation_degs)
        pivot_move   = pivot_rotate - pivot

        arrow_rotation_pt = [self.meter_location[0] + self.arrow_attach[0], self.meter_location[1] + self.arrow_attach[1]]
        origin = (arrow_rotation_pt[0] - self.arrow_rotate[0] + min_box[0] - pivot_move[0], arrow_rotation_pt[1] - self.arrow_rotate[1] - max_box[1] + pivot_move[1])
        rotated_image = pygame.transform.rotate(self.arrow, rotation_degs)

        screen.blit(rotated_image, origin)

    def update_value(self, newval):
        self.value = newval


class Page:
    def attach_action_to_button(self, button_name, action):
        self.buttons[button_name].attach_action(action)


class Homescreen(Page):
    buttons = {
        'learn': Button('assets/home_learn.png', 75, 150),
        'timetrial': Button('assets/home_timetrial.png', 150, 150),
        'hardtimetrial': Button('assets/home_hardtimetrial.png', 225, 150),
        'accuracy': Button('assets/home_accuracy.png', 300, 150),
        'dumb': Button('assets/home_accuracy.png', 375, 150),
    }
    text = {
        'title': Text("Learn To Type!", 225, 30, fsize=36, color=(0,0,0)),
        'subtitle': Text("or else...", 225, 60, fsize=12, color=(0,0,0)),
        'learn': Text("Practice", 75, 200, fsize=12, color=(0,0,0)),
        'timetrial': Text("Time Trial (ez)", 150, 200, fsize=12, color=(0,0,0)),
        'hardtimetrial': Text("Time Trial (hard)", 225, 200, fsize=12, color=(0,0,0)),
        'accuracy': Text("Hardcore Mode", 300, 200, fsize=12, color=(0,0,0)),
        'dumb': Text("Ding-Ding!", 375, 200, fsize=12, color=(0,0,0))
    }

    def __init__(self, s):
        self.speaker = s
        self.reset()

    def reset(self):
        self.speaker.stop()
        pass

    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw(screen)
        for t in self.text.values():
            t.draw(screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action


class Learn(Page):
    buttons = {
        'back': Button('assets/back.png', 30, 42)
    }
    meter = Meter('assets/speedometer.png', 'assets/arrow.png', 225, 150, (2, 32), (0, 32), minang=-70, maxang=70)

    def __init__(self, s, k):
        self.speaker = s
        self.keybot = k
        self.keybot.start_sensor_polling()
        self.reset()

    def reset(self):
        self.keybot.start_sensor_polling()

    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw(screen)
        # self.meter.update_value(self.keybot.get_score())
        self.meter.update_value(0)
        self.meter.draw(screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        self.keybot.stop_sensor_polling()
                        return v.action


class TypeGame(Page):
    buttons = {
        'back': Button('assets/back.png', 30, 42)
    }
    font = pygame.font.Font('assets/bebas.ttf', 32)

    wpm_title = font.render("WPM:", True, (0, 0, 0))
    acc_title = font.render("ACCURACY:", True, (0, 0, 0))
    tar_title = font.render("WPM TARGET:", True, (0, 0, 0))

    def __init__(self, s, hard_words, accuracy_mode):
        self.hardmode = hard_words
        self.accuracymode = accuracy_mode
        self.speaker = s

        # Initialize random word generator based on test type
        if self.hardmode:
            self.rwg = WordGenerator('assets/words.txt', minlen=9)
        elif self.accuracymode:
            self.rwg = WordGenerator('assets/words.txt')
        elif not self.hardmode and not self.accuracymode:
            self.rwg = WordGenerator('assets/words.txt', maxlen=7)

        self.reset(skip_sounds=True)
        self.fill_word_buffer()

    def reset(self, skip_sounds=False):
        self.current_word = self.rwg.get_word()
        self.typed_word = ''
        self.next_words = []
        self.fill_word_buffer()
        self.cursor_index = 0

        self.words_correct = 0
        self.words_incorrect = 0
        self.thresh = 0
        self.thresh_index = 0

        self.start_time = None

        if not skip_sounds:
            self.speaker.play_fitness_intro()

    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw(screen)
 
        letter_spacing = 20
        letter_x = 150
        letter_y = 100
        user_letter_y = 140

        # Draw some rectangles for clarity
        pygame.draw.rect(screen, (200,200,200), pygame.Rect((0, letter_y), (450, 35)))
        pygame.draw.rect(screen, (150,150,150), pygame.Rect((letter_x-3, letter_y), (20, 80)))

        # Draw test letters
        letters = self.current_word
        for w in self.next_words:
            letters += ' ' + w
        letter_pos_x = letter_x
        letter_pos_x -= (letter_spacing * self.cursor_index)
        for l in letters:
            color = (0,0,0) if letter_pos_x >= letter_x else (150,150,150)
            img = self.font.render(l, True, color)
            screen.blit(img, (letter_pos_x, letter_y))
            letter_pos_x += letter_spacing

        # Draw user input letters
        letter_pos_x = letter_x - (letter_spacing * self.cursor_index)
        for l in self.typed_word:
            img = self.font.render(l, True, (0,0,0))
            screen.blit(img, (letter_pos_x, user_letter_y))
            letter_pos_x += letter_spacing

        # Display accuracy and WPM if game is started
        if self.start_time is not None:
            wpm_color = (0,0,0) if self.wpm > self.thresh else (255,0,0)
            wpm_img = self.font.render(str(int(self.wpm)), True, wpm_color)
            acc_img = self.font.render(str(int(100 * self.accuracy)), True, (0, 255*self.accuracy, 0))
            tar_img = self.font.render(str(int(self.thresh)), True, (0,0,0))
            screen.blit(wpm_img, (400, 5))
            screen.blit(self.wpm_title, (400 - 10 - self.wpm_title.get_size()[0], 5))
            screen.blit(acc_img, (400, 35))
            screen.blit(self.acc_title, (400 - 10 - self.acc_title.get_size()[0], 35))
            screen.blit(tar_img, (230, 20))
            screen.blit(self.tar_title, (230 - 10 - self.tar_title.get_size()[0], 20))

        # Some periodic test related stuff
        if self.time_elapsed > cfg.thresh_times[self.thresh_index]:
            if self.wpm < self.thresh:
                print('Fun time...')

            self.thresh_index += 1
            self.thresh += cfg.thresh_increment
            self.speaker.play_speedup()

    def correct_input(self):
        self.words_correct += 1

    def incorrect_input(self):
        self.words_incorrect += 1

    def increment_buffer(self):
        self.typed_word = ''
        self.current_word = self.next_words[0]
        self.next_words = self.next_words[1:]
        self.fill_word_buffer()

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action
        elif event.type == pygame.KEYDOWN:
            # Start on first keypress
            if self.start_time is None:
                self.start_time = time.time()
                self.speaker.stop()

            if event.key == pygame.K_SPACE:
                if self.typed_word == self.current_word:
                    self.correct_input()
                else:
                    self.incorrect_input()
                self.increment_buffer()
                self.cursor_index= 0
            elif event.key == pygame.K_BACKSPACE:
                self.cursor_index -= 1
                self.cursor_index = 0 if self.cursor_index < 0 else self.cursor_index
                self.typed_word = self.typed_word[0:-1]
            else:
                self.typed_word += chr(event.key)
                self.cursor_index += 1


    def fill_word_buffer(self):
        while len(self.next_words) < 5:
            self.next_words.append(self.rwg.get_word())

    @property
    def accuracy(self):
        wordcount = (self.words_correct + self.words_incorrect)
        return 0 if wordcount == 0 else self.words_correct / wordcount

    @property
    def wpm(self):
        timeelapsed = (time.time() - self.start_time)
        return 0 if timeelapsed == 0 else 60 * self.words_correct / timeelapsed

    @property
    def time_elapsed(self):
        return 0 if self.start_time is None else time.time() - self.start_time


class Dumb(Page):
    buttons = {
        'back': Button('assets/back.png', 30, 42)
    }
    def __init__(self, s):
        self.speaker = s
        self.reset()

    def reset(self):
        pass

    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw(screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action
