from tkinter import *
import random


class Bird:
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.player_object = self.canvas.create_rectangle(200, 0, 270, 70,
                                                          fill="gold2")
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
        terminal_velocity = 30
        if self.velocity > terminal_velocity:
            self.velocity = terminal_velocity
        self.canvas.move(self.player_object, 0, self.velocity)

    def compile_movement(self):
        self.collide_with_ground()
        self.window.bind("<space>", self.jump)
        self.gravity()


class Pipe:
    def __init__(self, canvas, window, bird):
        self.canvas = canvas
        self.window = window
        self.player = bird
        self.pipe_object_top = None
        self.pipe_object_bottom = None

    def spawn(self):
        self.pipe_object_top = self.canvas.create_rectangle(700, 810, 770, 500,
                                                            fill="green2")
        self.pipe_object_bottom = self.canvas.create_rectangle(700, 270, 770, 0,
                                                               fill="green2")

    def move_pipe(self):
        self.canvas.move(self.pipe_object_bottom, -2, 0)
        self.canvas.move(self.pipe_object_top, -2, 0)


def main():
    window = Tk()
    canvas = Canvas(window, width="800", height="800", background="sky blue")
    canvas.pack()
    bird = Bird(canvas=canvas, window=window)
    pipe = Pipe(canvas=canvas, window=window,
                bird=bird)
    pipe.spawn()
    pipe.move_pipe()
    while True:
        canvas.after(1)
        bird.velocity += 0.8
        bird.compile_movement()

        canvas.update()


if __name__ == '__main__':
    main()
