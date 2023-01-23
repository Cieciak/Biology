import tkinter, time, threading
from typing import Self

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
        dx, dy = canvas.global_offset.diff()
        canvas.create_oval(self.x + dx, self.y + dy, self.x + dx, self.y + dy)

print('Baking frames')
BAKED_FRAMES = [[Vector2((x) % 1000 - 500, (x ** .5) % 1000 - 500) for y in range(400)] for x in range(1000)]
print('Done')


class SimulationWindow(tkinter.Tk):

    def __init__(self, x_res: int, y_res: int):
        super().__init__()

        # Config
        self.TITLE = 'Simulation'
        self.XRES = x_res
        self.YRES = y_res
        self.FRAME_MAX: int = 60
        self.FRAME_BUFFER = []
        self.TIME: float = 0.0
        self.loop_flag = True

        self.frame_buffer_thread: threading.Thread = threading.Thread(group = None, 
                                                                      target = self.frame_handler,
                                                                      name = 'frame_buffer_thread')
        self.frame_buffer_thread.start()

        # Setup
        self.title(self.TITLE)
        self.geometry(f'{x_res}x{y_res + 30}')
        self.resizable(0, 0)
        self['bg'] = '#F5F1E3'

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

    # Keeps the frame buffer filled with frames
    def frame_handler(self):
        while True:
            if len(self.FRAME_BUFFER) < self.FRAME_MAX:
                self.FRAME_BUFFER.append(BAKED_FRAMES.pop(0))
            else:
                time.sleep(1 / 30)


    # Rendering
    def mainloop(self, fps: int = 60) -> None:
        frame_time: float = 1 / fps
        accumulator: float = 0.0
        prev_stamp: float = time.time()
        while self.loop_flag:
            time_stamp = time.time()
            delta_time = time_stamp - prev_stamp
            prev_stamp = time_stamp

            accumulator += delta_time

            while accumulator > frame_time:
                self.canvas.delete('all')
                self.render_frame()
                self.update()
                accumulator -= frame_time

    def render_frame(self):
        current = self.FRAME_BUFFER.pop(0)
        for obj in current:
            obj.draw(self.canvas)

if __name__ == '__main__':
    window = SimulationWindow(1000, 1000)

    window.mainloop(fps = 60)