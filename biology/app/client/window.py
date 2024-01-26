from ..math import Vector
from ..object import Frame

from threading import Thread
import tkinter
import CPPP
import base64
import pickle
from time import time
from copy import deepcopy

class SimulationWindow(tkinter.Tk):

    def __init__(self, x_res: int, y_res: int):
        super().__init__()

        # Config
        self.TITLE: str                 = 'Simulation'
        self.XRES: int                  = x_res
        self.YRES: int                  = y_res
        self.FRAME_MAX: int             = 60
        self.FRAME_BUFFER: list[Frame]  = [] # Add frame type
        self.TIME: float                = 0.0
        self.BAR: int                   = 30
        self.CLIENT: CPPP.Client        = CPPP.Client()

        # Flags
        self.loop_flag: bool         = True
        self.frame_buffer_flag: bool = True

        # Thread for populating framebuffer
        self.frame_buffer_thread: Thread = Thread(group = None,
                                                  target = self.frame_handler,
                                                  name = 'frame-buffer-thread',)
        self.frame_buffer_thread.start()

        # Setup
        self.title(self.TITLE)
        self.tk.call('tk', 'scaling', 2.0)
        self.geometry(f'{self.XRES}x{self.YRES + self.BAR}+0+0')
        self.resizable(0, 0)
        self.protocol('WM_DELETE_WINDOW', self.client_exit)
        self['bg'] = '#F5F1E3'

        # Debug
        print(f'Debug. Resolution: {self.XRES}px x {self.YRES}px')
        print(f'Debug. DPI: {self.winfo_pixels("1i")}')

        # Canvas
        cnf = {
            'background': '#138A36',
            'height': y_res,
            'width': x_res,  
        }
        self.canvas = tkinter.Canvas(master = self, cnf = cnf)
        self.canvas.render_offset = Vector(0, 0)
        self.canvas.global_offset = Vector(self.XRES / 2, self.YRES / 2)
        self.canvas.max = max(self.XRES, self.YRES)
        self.canvas.place(x = -1, y = -1)

        # Buttons
        cnf = {
            'border': 0,
            'background': '#08181A',
            'foreground': '#DDDBCB',
            'activebackground': '#050505',
            'activeforeground': '#DDDBCB',
        }
        self.quit_button = tkinter.Button(self, cnf = cnf, text = 'Quit', command = self.client_exit)
        self.quit_button.place(x = 0, y = self.YRES, height = 30, width = 90)

        self.next_button = tkinter.Button(self, cnf = cnf, text = 'Next', command = self.next_generation)
        self.next_button.place(x = 90, y = self.YRES, height = 30, width = 90)

    def mainloop(self, fps: int = 60):
        frame_time: float = 1 / fps
        accumulator: float = 0.0
        prev_stamp: float = time()

        while self.loop_flag:
            time_stamp: float = time()
            delta_time: float = time_stamp - prev_stamp
            prev_stamp: float = time_stamp

            accumulator += delta_time

            while accumulator > frame_time:
                self.canvas.delete('all')
                self.render_frame()
                self.update()
                accumulator -= frame_time

    # Get frame
    def frame_handler(self):
        while self.frame_buffer_flag:
            if len(self.FRAME_BUFFER) > self.FRAME_MAX: continue

            request  = CPPP.Message(head = {'method': 'GET-FRAME'}, body = b'')
            response = self.CLIENT.request('127.0.0.1', 8080, request)

            data = base64.b64decode(response.body)

            obj = pickle.loads(data)

            self.FRAME_BUFFER += obj

    # Draw frame
    def render_frame(self):
        if not self.FRAME_BUFFER:
            print('INFO. No frames in buffer')
            return
        frame = self.FRAME_BUFFER.pop(0)
        for obj in frame: 
            obj.draw(self.canvas)

    # Closes the client
    def client_exit(self):
        self.frame_buffer_flag = False
        self.loop_flag         = False

    def next_generation(self):
        request = CPPP.Message(head = {'method': 'NEXT-GENERATION'}, body = b'')
        response = self.CLIENT.request('127.0.0.1', 8080, request)