import tkinter, threading, time, math

class Vector2:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.x} {self.y}'

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __round__(self, n):
        return Vector2(round(self.x, n), round(self.y, n))

    def manhattan(self, other):
        return abs(self.x + other.x) + abs(self.y + other.y)

    def update(self, ctx: tkinter.Tk, dt: float):
        pass

    def diff(self): return (self.x, self.y)

    def draw(self, canvas: tkinter.Canvas):
        dx, dy = canvas.offset.diff()
        canvas.create_oval(self.x + dx, self.y + dy, self.x + dx, self.y + dy)

class Being:

    @staticmethod
    def time_coeff(t: float):
        return math.exp(-(4*t -2)**2)

    def __init__(self, position: Vector2, size: Vector2) -> None:
        self.position = position
        self.size = size
        self.velocity     = Vector2(0, 0) # px / second
        self.acceleration = Vector2(0, 0) # px / second**2
        self.force = Vector2(1,-1)  # [N]
        self.mass = 1 # [kg]

        self.since_flap: float = 1

    def draw(self, canvas: tkinter.Canvas):
        dx, dy = canvas.global_offset.diff() 
        if canvas.max > canvas.render_offset.manhattan(self.position):
            canvas.create_rectangle(self.position.x - self.size.x / 2 + dx,
                                    self.position.y - self.size.y / 2 + dy,
                                    self.position.x + self.size.x / 2 + dx,
                                    self.position.y + self.size.y / 2 + dy,
                                    fill = '#D68915')

    def make_decision(self, ctx: tkinter.Tk, dt: float):
        if self.since_flap > 1:
            self.since_flap = 0


    def update(self, ctx: tkinter.Tk, dt: float):
        self.make_decision(ctx, dt)

        self.force = Vector2(0, -220) * Being.time_coeff(self.since_flap) + Vector2(0, 90)

        prev_acceleration = self.acceleration
        self.acceleration = self.force / self.mass
        self.position += self.velocity * dt + .5 * prev_acceleration * dt ** 2
        self.velocity += .5 *(self.acceleration + prev_acceleration) * dt

        self.since_flap += dt

        print(f'acceleration: {round(self.acceleration, 3)}, {self.since_flap}')

class SimulationWindow(tkinter.Tk):

    def __init__(self: tkinter.Tk, x_res: int = 500 , y_res: int = 500) -> None:
        super().__init__()

        # Configuration
        self.XRES = x_res
        self.YRES = y_res
        self.objects = []
        self.time: float = 0.0

        # Set up the window
        self.title('Simulation')
        self.geometry(f'{x_res}x{y_res}')
        self.resizable(0, 0)
        self.bind('<KeyPress>', self.key_down)

        # Set up the canvas
        cfg = {
            'background': '#138A36',
            'height': y_res,
            'width': x_res,
        }
        self.canvas = tkinter.Canvas(self, cnf = cfg)
        self.canvas.render_offset = Vector2(0,0)
        self.canvas.global_offset = Vector2(x_res / 2, y_res / 2)
        self.canvas.max = max(x_res, y_res)
        self.canvas.place(x = -1, y = -1)
 
        # Set up the update thread
        self.update_thread = threading.Thread(target = self.update_loop, kwargs = {'ups': 60})
        self.update_thread.start()
        print('Started update thread')

    # Updating
    def update_loop(self, ups: int = 60):
        frame_time: float = 1 / ups 
        accumulator: float = 0.0
        prev_stamp: float = time.time()
        while True:
            time_stamp: float = time.time()
            delta_time: float = time_stamp - prev_stamp
            prev_stamp = time_stamp

            # Acumulate time over the loop
            accumulator += delta_time

            # If time of one ups is exceded update the simulation
            while accumulator > frame_time:
                self.update_frame(frame_time)
                accumulator -= frame_time
                self.time += frame_time

    def update_frame(self, dt) -> None:
        # Go through ever object and update it
        for obj in self.objects:
            obj.update(self, dt)

    # Rendering
    def mainloop(self) -> None:
        while True:
            self.render_frame()
            self.update()
            self.canvas.delete('all')

    def render_frame(self):
        # TODO: Cap frames
        for obj in self.objects:
            obj.draw(self.canvas)

    # Other
    def key_down(self, key):
        if key.char == 's':
            self.objects[0].position += Vector2(0, 1)
        elif key.char == 'a':
            self.objects[0].position += Vector2(-1, 0)
        elif key.char == 'd':
            self.objects[0].position += Vector2(1, 0)
        elif key.char == 'w':
            self.objects[0].position += Vector2(0, -1)

window = SimulationWindow()
window.objects = [Being(Vector2(0 , 0), Vector2(40, 40))]
window.mainloop()