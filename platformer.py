import tkinter as tk

WIDTH = 1200
HEIGHT = 1200
STEP = 1 
class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.person = Person(self.canvas)
        self.person.create_person()

        self.platforms = [
            Platform(self.canvas, 0, 1000 - 60, 1200, 60),
            Platform(self.canvas, 100, 700, 500, 50)
        ]

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


class Physics:
    GRAVITY = 0.5

    def __init__(self):
        self.vx = 0
        self.vy = 0

    def apply_gravity(self):
        self.vy += self.GRAVITY

    def move_with_collision(self, obj, platforms):
        dx = self.vx
        while dx != 0:
            step = STEP if dx > 0 else -STEP
            if abs(dx) < STEP:
                step = dx
            obj.x += step
            for plat in platforms:
                if self.check_overlap(obj, plat):
                    if step > 0:
                        obj.x = plat.x - obj.width
                    else:  
                        obj.x = plat.x + plat.width
                    self.vx = 0
            dx -= step


        dy = self.vy
        obj.can_jump = False  
        while dy != 0:
            step = STEP if dy > 0 else -STEP
            if abs(dy) < STEP:
                step = dy
            obj.y += step
            for plat in platforms:
                if self.check_overlap(obj, plat):

                    if step > 0:  
                        obj.y = plat.y - obj.height
                        obj.vy = 0
                        obj.can_jump = True
                    else: 
                        obj.y = plat.y + plat.height
                        obj.vy = 0
            dy -= step

    @staticmethod
    def check_overlap(obj, plat):
        return (obj.x + obj.width > plat.x and obj.x < plat.x + plat.width and
                obj.y + obj.height > plat.y and obj.y < plat.y + plat.height)


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
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill='red'
        )

    def update(self, platforms):
        self.apply_gravity()
        self.move_with_collision(self, platforms)
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)


class Platform:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill='green'
        )


game = Game()
