import tkinter as tk

WIDTH = 1200
HEIGHT = 1200
class Game(object):
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.person = Person(self.canvas)
        self.person.create_person()
        self.platforms = [Platform(self.canvas, 200, 700, 500, 60)]
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.update_game()
        self.root.mainloop()
    def on_key_press(self, event):
        if event.keysym == "Left":
            self.person.vx = -5
        elif event.keysym == "Right":
            self.person.vx = 5
        elif event.keysym == "space" and self.person.can_jump:
            self.person.vy = -15
            self.person.can_jump = False

    def on_key_release(self, event):
        if event.keysym in ("Left", "Right"):
            self.person.vx = 0
    def update_game(self):
        self.person.update(self.platforms)
        self.root.after(16, self.update_game)
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
                obj.can_jump = True

class Person(Physics):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.width = 50
        self.height = 50
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.can_jump = False
    def create_person(self):
        self.rect = self.canvas.create_rectangle(self.x,self.y,self.x + self.width, self.y + self.height, fill ='red')
    def update(self, platforms):
        self.apply_gravity()
        self.move(self)
        self.check_collision(self, platforms)
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)


class Platform(Physics):
    def __init__(self, canvas, x, y,width,height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = canvas.create_rectangle(self.x,self.y, self.x + self.width, self.y + self.height ,fill = 'green')
        
game = Game()