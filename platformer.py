import tkinter as tk

class Game:
    def __init__(self):
        self.root = tk.Tk()                # This OPENS the window
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self.canvas.pack()

        self.player = Player(self.canvas)
        self.run()

    def run(self):
        self.player.update()
        self.root.after(16, self.run)

    def start(self):
        self.root.mainloop()

class Entity:
    def __init__(self, canvas):
        self.canvas = canvas

class Player(Entity):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprite = canvas.create_rectangle(50, 50, 100, 100, fill="red")

    def update(self):
        self.canvas.move(self.sprite, 2, 0)   # simple movement, placeholder

game = Game()
game.start()