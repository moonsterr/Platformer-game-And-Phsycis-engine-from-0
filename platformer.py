import tkinter as tk
import random

WIDTH = 1200
HEIGHT = 1200
STEP = 1
PLATFORM_COUNT = 10
PLATFORM_MIN_WIDTH = 100
PLATFORM_MAX_WIDTH = 400
PLATFORM_MIN_HEIGHT = 20
PLATFORM_MAX_HEIGHT = 60
PLATFORM_VERTICAL_GAP = 100

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.platforms = [
            Platform(self.canvas, 0, HEIGHT - 300, WIDTH, 120)
        ]
        self.generate_platforms(PLATFORM_COUNT)

        ground = self.platforms[0]
        start_x = ground.x + ground.width // 2 - 25
        start_y = ground.y - 50
        self.person = Person(self.canvas, start_x, start_y)
        self.person.create_person()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.update_game()
        self.root.mainloop()

    def generate_platforms(self, count):
        attempts = 0
        while count > 0 and attempts < 500:
            width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
            height = random.randint(PLATFORM_MIN_HEIGHT, PLATFORM_MAX_HEIGHT)
            x = random.randint(0, WIDTH - width)
            y = random.randint(100, HEIGHT - 200) 

            new_plat = Platform(self.canvas, x, y, width, height)

          
            if not any(self.check_overlap(new_plat, plat) for plat in self.platforms):
                self.platforms.append(new_plat)
                count -= 1
            else:
                self.canvas.delete(new_plat.rect)  

            attempts += 1

    @staticmethod
    def check_overlap(p1, p2):
        return (p1.x + p1.width > p2.x - 50 and p1.x < p2.x + p2.width + 50 and
                p1.y + p1.height > p2.y - PLATFORM_VERTICAL_GAP and p1.y < p2.y + p2.height + PLATFORM_VERTICAL_GAP)

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
    def __init__(self, canvas, x, y):
        super().__init__()
        self.canvas = canvas
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
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
