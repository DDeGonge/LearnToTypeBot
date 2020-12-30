import pygame
from RandomWordGenerator import RandomWord


pygame.init()

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

    def draw_button(self, screen):
        w, h = self.icon.get_size()
        screen.blit(self.icon, (self.location[0] - (w/2), self.location[1] -  (h/2)))

    def check_collision(self, cur):
        return self.rect.collidepoint(cur)

class Meter:
    def __init__(self, background_img, arrow_img, x_center, y_center, arrow_rotate, arrow_attach):
        self.bkgd = pygame.image.load(background_img)
        self.arrow = pygame.image.load(arrow_img)
        self.meter_location = (x_center, y_center)
        self.arrow_rotate = arrow_rotate  # Point in arrow image to rotate around
        self.arrow_attach = arrow_attach  # Rotation point for arrow, relative to bkgd center

        self.img_angle = 90  # To vertical, positive is CW rotated
        self.value = 0

    def draw_meter(self, screen):
        # Draw background
        w, h = self.bkgd.get_size()
        screen.blit(self.bkgd, (self.meter_location[0] - (w/2), self.meter_location[1] -  (h/2)))

        # Draw current arrow position
        rotation_degs = - self.value + self.img_angle
        # calcaulate the axis aligned bounding box of the rotated image
        w, h       = self.arrow.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(rotation_degs) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(self.arrow_rotate[0], -self.arrow_rotate[1])
        pivot_rotate = pivot.rotate(rotation_degs)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        arrow_rotation_pt = [self.meter_location[0] + self.arrow_attach[0], self.meter_location[1] + self.arrow_attach[1]]
        origin = (arrow_rotation_pt[0] - self.arrow_rotate[0] + min_box[0] - pivot_move[0], arrow_rotation_pt[1] - self.arrow_rotate[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(self.arrow, rotation_degs)
        screen.blit(rotated_image, origin)

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
    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw_button(screen)

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
    meter = Meter('assets/speedometer.png', 'assets/arrow.png', 225, 150, (2, 32), (0, 32))
    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw_button(screen)
        self.meter.draw_meter(screen)
        self.meter.value += 10
        self.meter.value %= 360

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action


class TypeGame(Page):
    buttons = {
        'back': Button('assets/back.png', 30, 42)
    }
    current_word = 'cheese'
    typed_word = ''
    next_words = ['butt', 'brain', 'potato', 'tomato']
    cursor_index = 0
    font = pygame.font.Font('assets/bebas.ttf', 32)

    def __init__(self, hard_words, accuracy_mode):
        pass

    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw_button(screen)
 
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


    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(self.typed_word == self.current_word)
                self.typed_word = ''
                self.current_word = self.next_words[0]
                self.next_words = self.next_words[1:]
                self.cursor_index= 0
            elif event.key == pygame.K_BACKSPACE:
                self.cursor_index -= 1
                self.cursor_index = 0 if self.cursor_index < 0 else self.cursor_index
                self.typed_word = self.typed_word[0:-1]
            else:
                self.typed_word += chr(event.key)
                self.cursor_index += 1


    def get_word_buffer(self):
        return len(self.next_words)

    def add_word(self, word):
        self.next_words.append(word)
    


class Dumb(Page):
    buttons = {
        'back': Button('assets/back.png', 30, 42)
    }
    def display_screen(self, screen):
        for b in self.buttons.values():
            b.draw_button(screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for k, v in self.buttons.items():
                    if v.check_collision(event.pos):
                        return v.action


def main():
    # Set up window
    screen = pygame.display.set_mode((450, 300))
    pygame.display.set_caption("Learn To Type!")
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    clock = pygame.time.Clock()

    # Initialize all screens
    s_homescreen = Homescreen()
    s_learn = Learn()
    s_timetrial = TypeGame(hard_words=False, accuracy_mode=False)
    s_hardtimetrial = TypeGame(hard_words=True, accuracy_mode=False)
    s_accuracy = TypeGame(hard_words=False, accuracy_mode=True)
    s_dumb = Dumb()

    # Add page connections
    s_homescreen.attach_action_to_button('learn', s_learn)
    s_homescreen.attach_action_to_button('timetrial', s_timetrial)
    s_homescreen.attach_action_to_button('hardtimetrial', s_timetrial)
    s_homescreen.attach_action_to_button('accuracy', s_timetrial)
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
        screen.fill((255,255,255))

        active_screen.display_screen(screen)

        pygame.display.update()
        clock.tick(60)


if __name__=="__main__":
    main()