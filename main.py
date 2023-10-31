# Mastermind Game in Python using Kivy!
import random
import kivy

# import base Class of our App and UIX features from kivy classes
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.widget import Widget

Window.size = (450, 800)  # 9x16
# create a library of colors
red = 1, 0, 0
orange = 1, 0.5, 0
yellow = 1, 1, 0
green = 0, 1, 0
blue = 0, 0, 1
purple = 1, 0, 1
gray = 0.5, 0.5, 0.5
black = 0, 0, 0
white = 1, 1, 1

guess_colors = [[white, white, white, white],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray],
                [gray, gray, gray, gray]]  # list of lists - all ten rows of guess colors here
fb_colors = [[gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray],
             [gray, gray, gray, gray]]  # list of lists - all ten rows of fb colors here
choice_colors = [red, orange, yellow, green, blue, purple]  # list of red, orange, yellow, green, blue, purple
answer_colors = [random.choice(choice_colors), random.choice(choice_colors),
                 random.choice(choice_colors),
                 random.choice(choice_colors)]  # four colors selected randomly from available choices

turn = 0
solved = False


class MainWidget(Widget):
    horz_lines = []
    horz_points = []
    vert_lines = []
    vert_points = []
    answers = []
    guesses = [[], [], [], [], [], [], [], [], [], []]
    feedback = [[], [], [], [], [], [], [], [], [], []]
    choices = []
    buttons = []
    rect = None
    active = None
    selected = None
    answer_cover = None
    square_size = None
    selected_color = 0
    menu = False
    menu_rects = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_bg()

    def redraw(self):
        global guess_colors, fb_colors, solved
        guess_colors = [[white, white, white, white],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray],
                        [gray, gray, gray, gray]]
        fb_colors = [[gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray],
                     [gray, gray, gray, gray]]
        solved = False
        self.horz_lines = []
        self.horz_points = []
        self.vert_lines = []
        self.vert_points = []
        self.answers = []
        self.guesses = [[], [], [], [], [], [], [], [], [], []]
        self.feedback = [[], [], [], [], [], [], [], [], [], []]
        self.choices = []
        self.buttons = []
        self.rect = None
        self.active = None
        self.selected = None
        self.answer_cover = None
        self.square_size = None
        self.selected_color = 0
        self.menu = False

    def init_bg(self):

        with self.canvas:
            self.rect = Rectangle(bg_color=Color(.125, .165, .267))
            self.active = Rectangle(bg_color=Color(.3, .3, .3))
            self.selected = Ellipse(bg_color=Color(.1, .9, .8))
            Color(.8, .8, .8)
            self.init_buttons()
            for i in range(13):
                self.horz_lines.append(Line(width=3))
            for i in range(3):
                self.vert_lines.append(Line(width=3))
            for i in range(4):
                self.answers.append(
                    Ellipse(bg_color=Color(answer_colors[i][0], answer_colors[i][1], answer_colors[i][2])))
            for i in range(10):
                for j in range(4):
                    color = guess_colors[i][j]
                    self.guesses[i].append(Ellipse(bg_color=Color(color[0], color[1], color[2])))
            for i in range(10):
                for j in range(4):
                    color = fb_colors[i][j]
                    self.feedback[i].append(Ellipse(bg_color=Color(color[0], color[1], color[2])))
            for i in range(6):
                self.choices.append(
                    Ellipse(bg_color=Color(choice_colors[i][0], choice_colors[i][1], choice_colors[i][2])))
            self.answer_cover = Rectangle(bg_color=Color(.65, .35, .45))

    def init_buttons(self):
        self.buttons.append(Button(text='Menu', bold='True'))
        self.buttons.append(Button(text='Submit', bold='True'))
        self.buttons.append(Button(text='Restart', bold='True'))

    def update_bg(self):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.square_size = (int(self.width / 6), int(self.height / 13))
        # 13 rows and 2 vertical sections for the overall bg
        for i in range(13):
            line_height = i * self.square_size[1]
            self.horz_lines[i].points = [0, line_height, self.width, line_height]
        self.vert_lines[0].points = [2, 0, 2, self.height]
        self.vert_lines[1].points = [int(self.width / 5), int(self.height / 13) * 2, int(self.width / 5), self.height]
        self.vert_lines[2].points = [self.width - 2, 0, self.width - 2, self.height]
        # four color answer
        for i in range(4):
            self.answers[i].pos = int((self.width / 5) * (i + 1.1)) + 7, int(self.height - self.square_size[1]) + 7
            self.answers[i].size = self.square_size[0] - 10, self.square_size[1] - 10
        # four color guesses x 10 rows
        for i in range(10):
            for j in range(4):
                self.guesses[i][j].pos = int((self.width / 5) * (j + 1.1)) + 7, int(self.square_size[1]) * (i + 2) + 7
                self.guesses[i][j].size = self.square_size[0] - 10, self.square_size[1] - 10
                # four feedbacks each for 10 turns
        for i in range(10):
            for j in range(4):
                row = j // 2
                col = j % 2
                self.feedback[i][j].pos = int((self.width / 11) * col) + int((self.width / 11) * .25), \
                                          int((self.height / 13) * (i + 2)) + row * int((self.height / 13) * 0.4) + int(
                                              (self.height / 13) * .15)
                self.feedback[i][j].size = self.square_size[0] / 3, self.square_size[1] / 3
        # guess options - 6 ellipses showing 6 colors
        for i in range(6):
            if self.selected_color == i:
                self.selected.pos = int((self.width / 7)) * (i + 0.5) + 2, int(self.height / 13) + 2
                self.selected.size = self.square_size[0] - 4, self.square_size[1] - 4
            self.choices[i].pos = int((self.width / 7)) * (i + 0.5) + 7, int(self.height / 13) + 7
            self.choices[i].size = self.square_size[0] - 15, self.square_size[1] - 15
        # active rectangle to be drawn behind active turn
        self.active.size = (self.width, self.height / 13)
        self.active.pos = (0, (turn + 2) * int(self.height / 13) + 2)
        if not solved:
            self.answer_cover.pos = int(self.width / 5) + 2, int(self.height / 13) * 12 + 7
            self.answer_cover.size = int(self.width / 5 * 4) - 6, int(self.height / 13)
        else:
            self.answer_cover.pos = (int(self.width / 5) + 2, int(self.height / 13) * 12 + 9)
            self.answer_cover.size = 1, 1
        # add button logic here
        self.draw_buttons()
        # add the menu drawing here
        if self.menu:
            self.draw_menu()

    def draw_buttons(self):
        self.buttons[0].pos = (0, self.height - int(self.height / 13))
        self.buttons[0].size = (self.width / 5, self.height / 13)
        self.buttons[1].pos = (0, 0)
        self.buttons[1].size = (self.width / 2, self.height / 13)
        self.buttons[2].pos = (self.width / 2, 0)
        self.buttons[2].size = (self.width / 2, self.height / 13)

    def on_size(self, *args):
        self.update_bg()

    def on_touch_down(self, touch):
        global turn, guess_colors, answer_colors
        x_pos = touch.pos[0] / self.width * 100
        y_pos = touch.pos[1] / self.height * 100
        print(x_pos, y_pos)
        y_row = 100 / 13
        if not self.menu:
            # check if a color is selected from the color options row 7-93 in x pos is valid colors
            if y_row < y_pos < y_row * 2 and 7 <= x_pos <= 93:
                index = int((x_pos - 7) / 14.5)
                self.selected_color = index
            # check if submit is pressed and increment turn
            elif y_pos < y_row and x_pos < 50:
                if white not in guess_colors[turn]:
                    self.check_guess()
                    turn += 1
                    if turn >= 8:
                        print(answer_colors)
                    guess_colors[turn] = [white, white, white, white]
                    with self.canvas:
                        for i in range(4):
                            self.guesses[turn].insert(i, Ellipse(bg_color=Color(white[0], white[1], white[2])))
                            self.guesses[turn].pop(i + 1)
            # check if you clicked on a circle in the active turn to set it to selected color
            elif y_row * (turn + 2) < y_pos < y_row * (turn + 3) and 20 <= x_pos:
                index = int((x_pos - 20) / 20)
                guess_colors[turn][index] = self.selected_color
                color = choice_colors[self.selected_color]
                with self.canvas:
                    self.guesses[turn].insert(index, Ellipse(bg_color=Color(color[0], color[1], color[2])))
                    self.guesses[turn].pop(index + 1)
        # check if restart is pressed, if so, generate new answers and clear out board4
        if y_pos < y_row and x_pos > 50:
            self.menu = False
            new_answers = [random.choice(choice_colors), random.choice(choice_colors),
                           random.choice(choice_colors),
                           random.choice(choice_colors)]
            answer_colors = new_answers
            turn = 0
            self.redraw()
            self.init_bg()
        # check if menu is pressed and either display or put away the menu based on that click
        elif y_pos > 12 * y_row and x_pos < 20:
            if not self.menu:
                self.menu = True
            elif not solved:
                self.menu = False
                for i in range(len(self.menu_rects)):
                    self.menu_rects[i].size = (0, 0)
        self.update_bg()

    def draw_menu(self):
        self.menu_rects.append(Rectangle(bg_color=Color(.625, .165, .267)))
        self.menu_rects.append(Rectangle(bg_color=Color(.8, .665, .267)))
        self.menu_rects.append(Rectangle(bg_color=Color(.225, .165, .567)))
        with self.canvas:
            Color(.9, .8, .7)
        self.menu_rects[0].size = self.size[0]/2, self.size[1]/2
        self.menu_rects[0].pos = self.width / 4, self.height / 4
        self.canvas.add(self.menu_rects[0])
        with self.canvas:
            Color(.4, .8, .8)
        self.menu_rects[1].size = self.size[0]/2 - 10, self.size[1]/2 - 10
        self.menu_rects[1].pos = self.width / 4 + 5, self.height / 4 + 5
        self.canvas.add(self.menu_rects[1])
        with self.canvas:
            Color(1, 1, 1)
        self.menu_rects[2].size = self.size[0]/2 - 20, self.size[1]/2 - 20
        self.menu_rects[2].pos = self.width / 4 + 10, self.height / 4 + 10
        self.menu_rects[2].source = 'MASTERMIND.png'
        self.canvas.add(self.menu_rects[2])

    def check_guess(self):
        global solved
        last_turn = guess_colors[turn]
        responses = [gray, gray, gray, gray]
        response_index = 0
        for i in range(len(last_turn)):
            if choice_colors[last_turn[i]] == answer_colors[i]:
                responses[response_index] = red
                response_index += 1
                print(f'{last_turn[i]} is in the right spot')
            elif choice_colors[last_turn[i]] in answer_colors:
                guess_count = last_turn.count(last_turn[i])
                answer_count = answer_colors.count(choice_colors[last_turn[i]])
                # if this is the only one of this color in our guess, it's a white peg
                only_input = (guess_count == 1)
                # if there are more answers of that color than guesses, it's a white peg
                several_outputs = (answer_count >= guess_count)
                # if there are more guessed than in answer, only count if not a red and not a white already
                these_indexes = []
                answer_indexes = []
                for j in range(len(last_turn)):
                    if last_turn[j] == last_turn[i] and choice_colors[last_turn[j]] != answer_colors[j]:
                        these_indexes.append(j)
                    if answer_colors[j] == choice_colors[last_turn[i]] and choice_colors[last_turn[j]] != answer_colors[j]:
                        answer_indexes.append(j)
                print(these_indexes, answer_indexes)
                count_this = these_indexes.index(i) < len(answer_indexes)
                if only_input or several_outputs or count_this:
                    responses[response_index] = white
                    response_index += 1
                    print(f'{last_turn[i]} is in the answer but wrong spot')

        # shuffle the responses - most versions of the game allow random feedback
        random.shuffle(responses)
        for i in range(4):
            color = responses[i]
            with self.canvas:
                self.feedback[turn].insert(i, Ellipse(bg_color=Color(color[0], color[1], color[2])))
                self.feedback[turn].pop(i+1)
        if responses.count(red) == 4:
            solved = True
            print('solved!')
            self.menu = True
            self.update_bg()


# defining our base class of the kivy app - you could change your app name here
class MastermindApp(App):
    pass


# initialize the app and command the run method to execute, then start the app
if __name__ == '__main__':
    MastermindApp().run()
