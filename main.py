from tkinter import *


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
            self.velocity -= 5
            self.canvas.move(self.player_object, 0, self.velocity)
        self.canvas.update()

    def gravity(self):
        terminal_velocity = 25
        if self.velocity > terminal_velocity:
            self.velocity = terminal_velocity
        self.canvas.move(self.player_object, 0, self.velocity)

    def compile_movement(self):
        self.window.bind("<space>", self.jump)
        self.gravity()


def main():
    window = Tk()
    canvas = Canvas(window, width="800", height="800", background="sky blue")
    canvas.pack()
    bird = Bird(canvas=canvas, window=window)
    while True:
        canvas.after(1)
        bird.velocity += 0.8
        bird.compile_movement()
        canvas.update()


if __name__ == '__main__':
    main()
