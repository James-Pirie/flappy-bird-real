from tkinter import *
import random


class Bird:
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.player_object = \
            self.canvas.create_rectangle(200, 0, 270, 70, fill="gold2")
        self.velocity = 0
        self.window = window

    def jump(self, event):
        self.velocity = 0
        for x in range(7):
            self.canvas.after(2)
            self.velocity -= 1.8
            self.canvas.move(self.player_object, 0, self.velocity)
        self.canvas.update()

    def collide_with_ground(self):
        if self.canvas.coords(self.player_object)[3] > 800:
            self.velocity = 0

    def gravity(self):
        self.collide_with_ground()
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
        if player_coords[2] > top_pipe_coords[0] and \
                player_coords[1] < top_pipe_coords[3] and \
                player_coords[0] < top_pipe_coords[2]:
            return True
        else:
            return False


class Score:
    def __init__(self, score, canvas, bird, pipes):
        self.score = score
        self.canvas = canvas
        self.bird = bird
        self.pipe = pipes
        self.text = self.canvas.create_text(400, 60,
                                            fill="white",
                                            font="Times 100",
                                            text=f"{self.score}")

    def update(self):
        if self.canvas.coords(self.bird.player_object)[0] == \
                self.canvas.coords(self.pipe[0].pipe_object_top)[2]:
            self.score += 1
            self.canvas.itemconfigure(self.text,
                                      text=f"{self.score}")


def main():
    window = Tk()
    canvas = Canvas(window, width="800", height="800",
                    background="sky blue")
    canvas.pack()
    list_of_pipes = []
    pipe_hit_list = []
    player = Bird(canvas=canvas, window=window)
    pipe_counter = 0
    score_value = 0
    score = Score(score=score_value, canvas=canvas,
                  bird=player, pipes=list_of_pipes)
    while True:
        if len(list_of_pipes) > 0:
            score.update()
        # ==================== pipes ====================

        pipe_counter += 1
        if pipe_counter == 200:
            new_pipe = Pipe(canvas=canvas, window=window, bird=player,
                            list_of_pipes=list_of_pipes)
            new_pipe.spawn()
            pipe_counter = 0
            canvas.tag_raise(score.text)
        for i in range(len(list_of_pipes)):
            list_of_pipes[i].collision()
            list_of_pipes[i].move_pipe()
            if list_of_pipes[i].destroy_pipe():
                pipe_hit_list.append(list_of_pipes[i])
                break  # wildly inappropriate

        # ==================== player ====================

        player.velocity += 0.8
        player.compile_movement()

        # ==================== general ====================

        canvas.after(7)
        canvas.update()


if __name__ == '__main__':
    main()
