import tkinter, time, threading
from typing import Self
from ..CPPP.CPPP import send_request, CPPPMessage
from ..utils.math import Vector
from ..utils.graphics import RenderBeing

SERVER = '127.0.0.1'
#SERVER = '129.151.213.44'
PORT = 8080

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
        self.frame_buffer_flag = True

        self.frame_buffer_thread: threading.Thread = threading.Thread(group = None, 
                                                                      target = self.frame_handler,
                                                                      name = 'frame_buffer_thread')
        self.frame_buffer_thread.start()

        # Setup
        self.title(self.TITLE)
        self.geometry(f'{x_res}x{y_res + 30}')
        self.resizable(0, 0)
        self.protocol('WM_DELETE_WINDOW', self.client_exit)
        self['bg'] = '#F5F1E3'

        # Set up the canvas
        cfg = {
            'background': '#138A36',
            'height': y_res,
            'width': x_res,
        }
        self.canvas = tkinter.Canvas(self, cnf = cfg)
        self.canvas.render_offset = Vector(0,0)
        self.canvas.global_offset = Vector(x_res / 2, y_res / 2)
        self.canvas.max = max(x_res, y_res)
        self.canvas.place(x = -1, y = -1)

        cfg = {
            'border': 0,
            'background': '#08181A',
            'foreground': '#DDDBCB',
            'activebackground': '#050505',
            'activeforeground': '#DDDBCB',
        }

        # Next gen
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'NEXT', command = self.signal_next_generation)
        self.next_button.place(x = 0, y = y_res, height = 30, width = 50)
        
        # Regenerate the whole simulation
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'REGENERATE', command = self.signal_simulation_reset)
        self.next_button.place(x = x_res - 110, y = y_res, height = 30, width = 110)

    # Keeps the frame buffer filled with frames
    def frame_handler(self):
        while self.frame_buffer_flag:
            if len(self.FRAME_BUFFER) < self.FRAME_MAX:
                response = send_request(SERVER, PORT, CPPPMessage(body = b'get'))
                for frame in response.body: 
                    self.FRAME_BUFFER.append([RenderBeing.fromDict(being) for being in frame])
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
        try: current = self.FRAME_BUFFER.pop(0)
        except: current = []
        print(len(self.FRAME_BUFFER))
        for obj in current:
            obj.draw(self.canvas)

    def client_exit(self):
        self.frame_buffer_flag = False
        self.loop_flag = False

    def signal_next_generation(self):
        send_request(SERVER, PORT, CPPPMessage(body = 'next_gen'))

    def signal_simulation_reset(self):
        send_request(SERVER, PORT, CPPPMessage(body = 'regenerate'))

if __name__ == '__main__':
    window = SimulationWindow(1000, 1000)
    window.mainloop(fps = 60)