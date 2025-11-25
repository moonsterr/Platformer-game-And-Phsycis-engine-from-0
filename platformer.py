import tkinter as tk

WIDTH = 800
HEIGHT = 800
class Game(object):
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.root.mainloop()

class Physics(object):
    GRAVITY = 1
    def __init__(self):
        self.vx = 0
        self.vy = 0
    def apply_gravity(self):
        self.vy += self.GRAVITY
    def move(self, obj):
        obj.x += self.vx
        obj.y += self.vy
    def check_collision(self, obj, platforms):
        for plat in platforms:
            if (obj.x + obj.width > plat.x and obj.x < plat.x + plat.width and
                obj.y + obj.height > plat.y and obj.y < plat.y + plat.height):
                obj.y = plat.y - obj.height
                self.vy = 0

class Person(Physics):
    def __init__(self, canvas):
        self.canvas = canvas
        self.player_width = 50
        self.player_height = 50
        self.player_x = WIDTH//2
        self.player_y = HEIGHT // 2

class Platform(Physics):
    WIDTH = 125
    HEIGHT = 60
    def __init__(self, canvas, x, y,width,height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.rect = canvas.create_rectangle(self.x,self.y, self.x + self.width, self.y + self.height ,fill = 'green')
        
game = Game()