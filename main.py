"""
Tkinter Flappy Bird Game.

Date Finished: 07/05/21

Author: James Pirie
"""

# FIX BREAK!!!!

import tkinter
import random


class Bird:
    """The player class for a Bird."""

    # coordinates for the Bird's starting position
    _BIRD_X_COORDS_LEFT_CORNER = 200
    _BIRD_Y_COORDS_LEFT_CORNER = 0
    _BIRD_X_COORDS_RIGHT_CORNER = 270
    _BIRD_Y_COORDS_RIGHT_CORNER = 70

    _BIRD_COLOUR = "gold2"

    _NUMBER_OF_TIMES_TO_ACCELERATE_UPWARDS = 7
    _MILLISECONDS_BEFORE_REFRESH = 2
    _JUMP_ACCELERATION = 1.8
    _BOTTOM_OF_SCREEN_COORDINATES = 800
    __BIRD_Y_COORDS_RIGHT_CORNER_INDEX = 3
    _VELOCITY_BEFORE_JUMP = 0
    _STARTING_VELOCITY = 0
    _TERMINAL_VELOCITY = 30
    _Y_AXIS_MOVEMENT = 0

    def __init__(self, canvas, window, game_over):
        """Initialize the Bird attributes.

        Attributes:
            canvas: (Canvas) The Tkinter Canvas, on which the game
            will be rendered on.

            window: The Tkinter window, where the canvas and menu will
            be displayed.

            game_over: (bool) A boolean to determine when the game is
            over.

            player_object: (rectangle) The Tkinter canvas object of the
            player.

            velocity: (int) The vector value of the birds velocity
            downwards.
        """
        self.canvas = canvas
        self.player_object = \
            self.canvas.create_rectangle(Bird._BIRD_X_COORDS_LEFT_CORNER,
                                         Bird._BIRD_Y_COORDS_LEFT_CORNER,
                                         Bird._BIRD_X_COORDS_RIGHT_CORNER,
                                         Bird._BIRD_Y_COORDS_RIGHT_CORNER,
                                         fill=Bird._BIRD_COLOUR)
        self.velocity = Bird._STARTING_VELOCITY
        self.window = window
        self.game_over = game_over

    def jump(self, event):
        """Cause the bird to jump, by changing the velocity upwards.

        :param event: The key press to trigger the jump.
        """
        self.velocity = Bird._VELOCITY_BEFORE_JUMP
        for x in range(Bird._NUMBER_OF_TIMES_TO_ACCELERATE_UPWARDS):
            self.canvas.after(Bird._MILLISECONDS_BEFORE_REFRESH)
            self.velocity -= Bird._JUMP_ACCELERATION
            self.canvas.move(self.player_object,
                             Bird._Y_AXIS_MOVEMENT, self.velocity)
        self.canvas.update()

    def collide_with_ground(self):
        """Return a bool to detect when the player hits the ground."""
        if self.canvas.coords(self.player_object)[Bird.__BIRD_Y_COORDS_RIGHT_CORNER_INDEX] > \
                Bird._BOTTOM_OF_SCREEN_COORDINATES:
            return True

    def gravity(self):
        """Constantly set the players velocity to self.velocity."""
        if self.velocity > Bird._TERMINAL_VELOCITY:
            self.velocity = Bird._TERMINAL_VELOCITY
        self.canvas.move(self.player_object,
                         Bird._Y_AXIS_MOVEMENT, self.velocity)

    def compile_movement(self):
        """Compile the gravity and jump to work together."""
        self.window.bind("<space>", self.jump)
        self.gravity()


class Pipe:
    """Represents the Pipe objects the bird will fly through."""

    _RANDOM_PIPE_GAP_UPPER_MAX = 275
    _RANDOM_PIPE_GAP_LOWER_MIN = 740

    _UPPER_PIPE_X_COORD_LEFT_CORNER = 810
    _UPPER_PIPE_X_COORD_RIGHT_CORNER = 880
    _UPPER_PIPE_Y_COORD_RIGHT_CORNER = 900

    _LOWER_PIPE_X_COORD_LEFT_CORNER = 810
    _LOWER_PIPE_X_COORD_RIGHT_CORNER = 880
    _LOWER_PIPE_Y_COORD_RIGHT_CORNER = 0
    _PIPE_GAP_SIZE = 270

    _RANDOM_Y_LOCATION = random.randint(_RANDOM_PIPE_GAP_UPPER_MAX,
                                        _RANDOM_PIPE_GAP_LOWER_MIN)

    _PIPE_COLOUR = "green2"
    _PIPE_VELOCITY_X = -2
    _PIPE_VELOCITY_Y = 0

    _PIPE_Y_RIGHT_CORNER_COORDS_INDEX = 2
    _OFF_SCREEN_COORDS = -44
    _OLDEST_PIPE_INDEX = 0

    _PLAYER_COORDS_X_LEFT_INDEX = 0
    _PLAYER_COORDS_Y_LEFT_INDEX = 1
    _PLAYER_COORDS_X_RIGHT_INDEX = 2
    _PLAYER_COORDS_Y_RIGHT_INDEX = 3

    _PIPE_COORDS_X_LEFT_INDEX = 0
    _PIPE_COORDS_Y_LEFT_INDEX = 1
    _PIPE_COORDS_X_RIGHT_INDEX = 2
    _PIPE_COORDS_Y_RIGHT_INDEX = 3

    def __init__(self, canvas, window, list_of_pipes, bird):
        """Initialize the Pipe attributes.

        Attributes:
            :param canvas: (Canvas) The Tkinter Canvas, on which the
            game will be rendered on.

            :param window: (Tk) The Tkinter window, where the canvas and
            menu will be displayed.

            :param list_of_pipes: (list) A list of every active pipe, so
            that they can be iterated through.

            :param bird: (Bird) The player bird object.

            pipe_object_bottom: (rectangle) The bottom half of the pipe.

            pipe_object_top: (rectangle) The top half of the pipe.

            list_of_pipes: (list) a list of every existing pipe, so they
            can be iterated through.
        """
        self.canvas = canvas
        self.pipe_object_bottom = None
        self.pipe_object_top = None
        self.window = window
        self.list_of_pipes = list_of_pipes
        self.player = bird

    def spawn(self):
        """Create and renders two rectangle objects for pipes."""
        self.list_of_pipes.append(self)
        self.pipe_object_bottom = \
            self.canvas.create_rectangle(Pipe._UPPER_PIPE_X_COORD_LEFT_CORNER,
                                         Pipe._RANDOM_Y_LOCATION,
                                         Pipe._UPPER_PIPE_X_COORD_RIGHT_CORNER,
                                         Pipe._UPPER_PIPE_Y_COORD_RIGHT_CORNER,
                                         fill=Pipe._PIPE_COLOUR)

        self.pipe_object_top = \
            self.canvas.create_rectangle(Pipe._LOWER_PIPE_X_COORD_LEFT_CORNER,
                                         Pipe._RANDOM_Y_LOCATION -
                                         Pipe._PIPE_GAP_SIZE,
                                         Pipe._LOWER_PIPE_X_COORD_RIGHT_CORNER,
                                         Pipe._LOWER_PIPE_Y_COORD_RIGHT_CORNER,
                                         fill=Pipe._PIPE_COLOUR)

    def move_pipe(self):
        """Set the pipes velocity to move to the left at 2."""
        self.canvas.move(self.pipe_object_top,
                         Pipe._PIPE_VELOCITY_X, Pipe._PIPE_VELOCITY_Y)
        self.canvas.move(self.pipe_object_bottom,
                         Pipe._PIPE_VELOCITY_X, Pipe._PIPE_VELOCITY_Y)

    def destroy_pipe(self):
        """If the pipe is off the left side of the screen, delete it."""
        if self.canvas.coords(self.pipe_object_bottom)[Pipe._PIPE_Y_RIGHT_CORNER_COORDS_INDEX] \
                < Pipe._OFF_SCREEN_COORDS:
            self.canvas.delete(self.pipe_object_top,
                               self.pipe_object_bottom)
            self.list_of_pipes.pop(Pipe._OLDEST_PIPE_INDEX)
            return True
        else:
            return False

    def collision(self):
        """If the player makes contact with the pipe return True."""
        player_coords = self.canvas.coords(self.player.player_object)
        bottom_pipe_coords = self.canvas.coords(self.pipe_object_bottom)
        top_pipe_coords = self.canvas.coords(self.pipe_object_top)
        if player_coords[Pipe._PLAYER_COORDS_X_RIGHT_INDEX]\
                >= bottom_pipe_coords[Pipe._PIPE_COORDS_X_LEFT_INDEX] and \
                player_coords[Pipe._PLAYER_COORDS_Y_RIGHT_INDEX] > \
                bottom_pipe_coords[Pipe._PIPE_COORDS_Y_LEFT_INDEX] and \
                player_coords[Pipe._PLAYER_COORDS_X_LEFT_INDEX] < \
                bottom_pipe_coords[Pipe._PIPE_COORDS_X_RIGHT_INDEX]:
            return True
        elif player_coords[Pipe._PLAYER_COORDS_X_RIGHT_INDEX] > \
                top_pipe_coords[Pipe._PIPE_COORDS_X_LEFT_INDEX] and \
                player_coords[Pipe._PLAYER_COORDS_Y_LEFT_INDEX] < \
                top_pipe_coords[Pipe._PIPE_COORDS_Y_RIGHT_INDEX] and \
                player_coords[Pipe._PLAYER_COORDS_X_LEFT_INDEX] < \
                top_pipe_coords[Pipe._PIPE_COORDS_X_RIGHT_INDEX]:
            return True
        else:
            return False


class Score:
    """The score every time the player passes through a pipe."""

    _TEXT_COORDS_X = 400
    _TEXT_COORDS_Y = 60
    _TEXT_COLOUR = "white"
    _TEXT_FONT = "Times 100"
    _PLAYER_COORDS_X_LEFT_INDEX = 0
    _PIPE_COORDS_X_RIGHT_INDEX = 2
    _SCORE_INCREMENT = 1

    def __init__(self, score_value, canvas, bird, pipes):
        """Initialize the Score attributes.

        Attributes:
            :param score_value: (int) A numerical variable to keep track
            of the score.

            :param canvas: (Canvas) The Tkinter Canvas, on which the game
            will be rendered on.

            :param bird: (Bird) The player Bird object.

            :param pipes: (Pipes) The pipe class obstacle object.
            text:
        """
        self.score_value = score_value
        self.canvas = canvas
        self.bird = bird
        self.pipe = pipes
        self.text = self.canvas.create_text(Score._TEXT_COORDS_X,
                                            Score._TEXT_COORDS_Y,
                                            fill=Score._TEXT_COLOUR,
                                            font=Score._TEXT_FONT,
                                            text=f"{self.score_value}")

    def update(self):
        """If the player has passed the pipe, update the score."""
        if self.canvas.coords(self.bird.player_object)[Score._PLAYER_COORDS_X_LEFT_INDEX] == \
                self.canvas.coords(self.pipe[Score._PLAYER_COORDS_X_LEFT_INDEX].pipe_object_top)[Score._PIPE_COORDS_X_RIGHT_INDEX]:
            self.score_value += Score._SCORE_INCREMENT
            self.canvas.itemconfigure(self.text,
                                      text=f"{self.score_value}")


class Game:
    """Render and restart the whole game in an object."""

    _STARTING_NUMBER_FOR_PIPE_COUNTER = 0
    _STARTING_SCORE = 0
    _CANVAS_WIDTH = "800"
    _CANVAS_HEIGHT = 800
    _CANVAS_COLOUR = "sky blue"
    _PIPE_INCRIMENT_RATE = 1
    _PIPE_SPAWN_ON_VALUE = 200
    _EMPTY_PIPE_LIST_LENGTH = 0
    _ACCELERATION_DUE_TO_GRAVITY = 0.8
    _GAME_REFRESH_RATE_MILLISECONDS = 7

    def __init__(self, window):
        """Initialize the Game attributes.

        Attributes:
            :param window: (Tk) The Tkinter window, where the canvas and
            menu will be displayed.

            canvas: (Canvas) The Tkinter Canvas, on which the game will
            be rendered on.

            list_of_pipes: (list) A list of every active pipe, so
            that they can be iterated through.

            player: (Bird) Player bird object.

            pipe_counter: (int) Integer to keep track of when to spawn
            a new pipe.

            score_value: (int) An Integer to keep track of the score.
            game_over score.
        """
        self.window = window
        self.canvas = None
        self.list_of_pipes = []
        self.player = None
        self.pipe_counter = Game._STARTING_NUMBER_FOR_PIPE_COUNTER
        self.score_value = Game._STARTING_SCORE
        self.game_over = False
        self.score = None

    def create_canvas(self):
        """Create a canvas for the game to be rendered."""
        self.canvas = tkinter.Canvas(self.window, width=Game._CANVAS_WIDTH,
                                     height=Game._CANVAS_HEIGHT,
                                     background=Game._CANVAS_COLOUR)
        self.canvas.pack()

    def create_player(self):
        """Create a Bird player object."""
        self.player = Bird(canvas=self.canvas, window=self.window,
                           game_over=self.game_over)

    def create_score(self):
        """Create a Score object, to store the score."""
        self.score = Score(score_value=self.score_value, canvas=self.canvas,
                           bird=self.player, pipes=self.list_of_pipes)

    def initialize_pipes(self):
        """Create, move and delete pipes when needed."""
        self.pipe_counter += Game._PIPE_INCRIMENT_RATE
        if self.pipe_counter == Game._PIPE_SPAWN_ON_VALUE:
            new_pipe = Pipe(canvas=self.canvas, window=self.window,
                            bird=self.player,
                            list_of_pipes=self.list_of_pipes)
            new_pipe.spawn()
            self.pipe_counter = Game._STARTING_NUMBER_FOR_PIPE_COUNTER
            self.canvas.tag_raise(self.score.text)
        for i in range(len(self.list_of_pipes)):
            if len(self.list_of_pipes) > Game._EMPTY_PIPE_LIST_LENGTH and \
                    self.list_of_pipes[i].collision():
                self.game_over = True
            self.list_of_pipes[i].move_pipe()
            if self.list_of_pipes[i].destroy_pipe():
                break  # wildly inappropriate

    def initialize_player(self):
        """Change the players velocity and check for collisions."""
        if self.player.collide_with_ground():
            self.game_over = True
        self.player.velocity += Game._ACCELERATION_DUE_TO_GRAVITY
        self.player.compile_movement()

    def initialize_game(self):
        """Compile all the methods to run the game."""
        self.create_canvas()
        self.create_player()
        self.create_score()
        while not self.game_over:
            if len(self.list_of_pipes) > Game._EMPTY_PIPE_LIST_LENGTH:
                self.score.update()
            self.initialize_pipes()
            self.initialize_player()
            self.canvas.after(Game._GAME_REFRESH_RATE_MILLISECONDS)
            self.canvas.update()
        self.canvas.delete(all)
        self.canvas.destroy()


class Menu:
    """Main menu Class."""

    _BUTTON_HEIGHT = 3
    _BUTTON_WIDTH = 10
    _EXIT_BUTTON_TEXT = "Exit"
    _PLAY_BUTTON_TEXT = "Play"

    def __init__(self):
        """Initialize the Menu attributes.

        Attributes:
            window: (Tk) The Tkinter window, where the canvas and menu
            will be displayed.

            new_game: (Game) A game object, for every new game.

            restart_button: (Button) A button to start a new game.

            exit_button: (Button) A button to close the program.
        """
        self.window = None
        self.new_game = None
        self.restart_button = None
        self.exit_button = None

    def create_window(self):
        """Create a new Tk window with an 800x800 resolution."""
        self.window = tkinter.Tk()
        self.window.geometry("800x800")

    def start_new_game(self):
        """Create a new Game, by creating a new Game object."""
        self.restart_button.pack_forget()
        self.exit_button.pack_forget()
        self.new_game = Game(window=self.window)
        self.new_game.initialize_game()
        self.restart_button.pack()
        self.exit_button.pack()

    def render_menu(self):
        """Create all the buttons for the main menu."""
        self.restart_button = tkinter.Button(self.window,
                                             text=Menu._PLAY_BUTTON_TEXT,
                                             height=Menu._BUTTON_HEIGHT,
                                             width=Menu._BUTTON_WIDTH,
                                             command=self.start_new_game)
        self.exit_button = tkinter.Button(self.window,
                                          text=Menu._EXIT_BUTTON_TEXT,
                                          height=Menu._BUTTON_HEIGHT,
                                          width=Menu._BUTTON_WIDTH,
                                          command=self.window.destroy)
        self.restart_button.pack()
        self.exit_button.pack()


def main():
    """Main function, to initialize the program."""
    program = Menu()
    program.create_window()
    program.render_menu()
    program.window.mainloop()


if __name__ == '__main__':
    main()
