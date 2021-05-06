from tkinter import *
import random

""" 
To do
3) Make menu look good
3) Tidy up code, fix that break bs
4) Port to window
5) Public and Private variables
"""


class Bird:
    """The player class"""
    def __init__(self, canvas, window, game_over):
        self.canvas = canvas
        self.player_object = \
            self.canvas.create_rectangle(200, 0, 270, 70, fill="gold2")
        self.velocity = 0
        self.window = window
        self.game_over = game_over

    def jump(self, event):
        self.velocity = 0
        for x in range(7):
            self.canvas.after(2)
            self.velocity -= 1.8
            self.canvas.move(self.player_object, 0, self.velocity)
        self.canvas.update()

    def collide_with_ground(self):
        if self.canvas.coords(self.player_object)[3] > 800:
            return True

    def gravity(self):

        terminal_velocity = 30
        if self.velocity > terminal_velocity:
            self.velocity = terminal_velocity
        self.canvas.move(self.player_object, 0, self.velocity)

    def compile_movement(self):
        self.window.bind("<space>", self.jump)
        self.gravity()


class Pipe:
    def __init__(self, canvas, window, list_of_pipes, bird):
        self.canvas = canvas
        self.pipe_object_bottom = None
        self.pipe_object_top = None
        self.window = window
        self.list_of_pipes = list_of_pipes
        self.player = bird

    def spawn(self):
        self.list_of_pipes.append(self)
        x_location = random.randint(275, 750)
        self.pipe_object_bottom = \
            self.canvas.create_rectangle(810, x_location, 880,
                                         900, fill="green2")

        self.pipe_object_top = \
            self.canvas.create_rectangle(810, x_location - 270,
                                         880, 0, fill="green2")

    def move_pipe(self):
        self.canvas.move(self.pipe_object_top, -2, 0)
        self.canvas.move(self.pipe_object_bottom, -2, 0)

    def destroy_pipe(self):
        if self.canvas.coords(self.pipe_object_bottom)[2] < -44:
            self.canvas.delete(self.pipe_object_top,
                               self.pipe_object_bottom)
            self.list_of_pipes.pop(0)
            return True
        else:
            return False

    def collision(self):
        player_coords = self.canvas.coords(self.player.player_object)
        bottom_pipe_coords = self.canvas.coords(self.pipe_object_bottom)
        top_pipe_coords = self.canvas.coords(self.pipe_object_top)
        if player_coords[2] >= bottom_pipe_coords[0] and \
                player_coords[3] > bottom_pipe_coords[1] and \
                player_coords[0] < bottom_pipe_coords[2]:
            return True
        elif player_coords[2] > top_pipe_coords[0] and \
                player_coords[1] < top_pipe_coords[3] and \
                player_coords[0] < top_pipe_coords[2]:
            return True
        else:
            return False


class Score:
    def __init__(self, score_value, canvas, bird, pipes):
        self.score_value = score_value
        self.canvas = canvas
        self.bird = bird
        self.pipe = pipes
        self.text = self.canvas.create_text(400, 60,
                                            fill="white",
                                            font="Times 100",
                                            text=f"{self.score_value}")

    def update(self):
        if self.canvas.coords(self.bird.player_object)[0] == \
                self.canvas.coords(self.pipe[0].pipe_object_top)[2]:
            self.score_value += 1
            self.canvas.itemconfigure(self.text,
                                      text=f"{self.score_value}")


class Game:
    def __init__(self, window):
        self.window = window
        self.canvas = None
        self.list_of_pipes = []
        self.player = None
        self.pipe_counter = 0
        self.score_value = 0
        self.game_over = False
        self.score = None

    def create_canvas(self):
        self.canvas = Canvas(self.window, width="800", height="800",
                             background="sky blue")
        self.canvas.pack()

    def create_player(self):
        self.player = Bird(canvas=self.canvas, window=self.window, game_over=self.game_over)

    def create_score(self):
        self.score = Score(score_value=self.score_value, canvas=self.canvas,
                           bird=self.player, pipes=self.list_of_pipes)

    def initialize_pipes(self):
        self.pipe_counter += 1
        if self.pipe_counter == 200:
            new_pipe = Pipe(canvas=self.canvas, window=self.window,
                            bird=self.player,
                            list_of_pipes=self.list_of_pipes)
            new_pipe.spawn()
            self.pipe_counter = 0
            self.canvas.tag_raise(self.score.text)
        for i in range(len(self.list_of_pipes)):
            if len(self.list_of_pipes) > 0 and \
                    self.list_of_pipes[i].collision():
                self.game_over = True
            self.list_of_pipes[i].move_pipe()
            if self.list_of_pipes[i].destroy_pipe():
                break  # wildly inappropriate

    def initialize_player(self):
        if self.player.collide_with_ground():
            self.game_over = True
        self.player.velocity += 0.8
        self.player.compile_movement()

    def initialize_game(self):
        self.create_canvas()
        self.create_player()
        self.create_score()
        while not self.game_over:
            if len(self.list_of_pipes) > 0:
                self.score.update()
            self.initialize_pipes()
            self.initialize_player()
            self.canvas.after(7)
            self.canvas.update()
        self.canvas.delete(all)
        self.canvas.destroy()


class Menu:
    def __init__(self):
        self.window = None
        self.new_game = None
        self.restart_button = None
        self.exit_button = None

    def create_window(self):
        self.window = Tk()
        self.window.geometry("800x800")

    def start_new_game(self):
        self.restart_button.pack_forget()
        self.exit_button.pack_forget()
        self.new_game = Game(window=self.window)
        self.new_game.initialize_game()
        self.restart_button.pack()
        self.exit_button.pack()

    def render_menu(self):
        self.restart_button = Button(self.window, text="Play",
                                     height=3, width=10,
                                     command=self.start_new_game)
        self.exit_button = Button(self.window, text="Exit", height=3,
                                  width=10, command=self.window.destroy)
        self.restart_button.pack()
        self.exit_button.pack()


def main():
    program = Menu()
    program.create_window()
    program.render_menu()
    program.window.mainloop()


if __name__ == '__main__':
    main()
