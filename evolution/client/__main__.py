import tkinter, time, threading
from typing import Self
from CPPP import CPPPMessage, send_request

from ..utils.math import Vector
from ..utils.graphics import RenderBeing, PointOfInterest

LAP = ( 800,  800)
_4K = (3000, 2000)
DEF = (1000, 1000)

RESOLUTION = LAP

SERVER = '127.0.0.1'
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
        self.tk.call('tk', 'scaling', 2.0)
        self.geometry(f'{x_res}x{y_res + 30}+0+0')
        self.resizable(0, 0)
        self.protocol('WM_DELETE_WINDOW', self.client_exit)
        self['bg'] = '#F5F1E3'

        print(f'Debug. Resolution: {x_res}px x {y_res}px')
        print(f'Debug. DPI: {self.winfo_pixels("1i")}')
        print(f'Debug. Server: {SERVER}:{PORT}')

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

        # Close app
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'Quit', command = self.client_exit)
        self.next_button.place(x = 0, y = y_res, height = 30, width = 100)

        # Next gen
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'Next', command = self.signal_next_generation)
        self.next_button.place(x = 100, y = y_res, height = 30, width = 100)
        
        # Regenerate the whole simulation
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'Regenerate', command = self.signal_simulation_reset)
        self.next_button.place(x = 200, y = y_res, height = 30, width = 100)

        # Regenerate the whole simulation
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'Genome', command = self.request_genome)
        self.next_button.place(x = 300, y = y_res, height = 30, width = 100)

        # Gene editor
        self.next_button = tkinter.Button(self, cnf = cfg, text = 'Enter', command = self.edit_genome)
        self.next_button.place(x = 400, y = y_res, height = 30, width = 100)

    # Keeps the frame buffer filled with frames
    def frame_handler(self):
        while self.frame_buffer_flag:
            if len(self.FRAME_BUFFER) < self.FRAME_MAX:
                response = send_request(SERVER, PORT, CPPPMessage(header = {'method': 'GET'}))
                for frame in response.body:
                    new_frame = []
                    for obj in frame:
                        match obj['type']:
                            case 'Being':
                                new_frame += [RenderBeing.fromDict(obj),]
                            case 'PointOfInterest':
                                new_frame += [PointOfInterest.fromDict(obj)]
                    self.FRAME_BUFFER.append(new_frame)
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

    def client_exit(self):
        self.frame_buffer_flag = False
        self.loop_flag = False

    def signal_next_generation(self):
        message = CPPPMessage(header = {'method': 'NEXT_GENERATION'})
        send_request(SERVER, PORT, message)

    def signal_simulation_reset(self):
        message = CPPPMessage(header = {'method': 'SIMULATION_RESET'})
        send_request(SERVER, PORT, message)

    def request_genome(self):
        message = CPPPMessage(header = {'method': 'REQUEST'}, body = 'genome')
        response = send_request(SERVER, PORT, message)
        print(response)

    def edit_genome(self):
        text_editor = tkinter.Toplevel(self)
        text_editor.title('Gene editor')
        gene_matrix = {}

        def command_generator(row, column):
            def action():
                gene_matrix[(row, column)].destroy()
                gene_matrix[(row, column)] = tkinter.Entry(text_editor, text = 'Hello')
                gene_matrix[(row, column)].grid(row = row, column = column)
                gene_matrix[(row, column + 1)] = tkinter.Button(text_editor, text = f'+', command = command_generator(row, column + 1))
                gene_matrix[(row, column + 1)].grid(row = row, column = column + 1)
            return action

        for row in range(1, 11):
            gene_matrix[(row, 0)] = tkinter.Button(text_editor, text = f'+', command = command_generator(row, 0))

        for index, obj in gene_matrix.items(): obj.grid(row = index[0], column = index[1])

        def send():
            for row in range(10):
                for column in range(10):
                    print(gene_matrix.get((row, column), None))

        done_button = tkinter.Button(text_editor, text='Done', command = send)
        done_button.grid(row = 0, column = 0)

if __name__ == '__main__':
    window = SimulationWindow(RESOLUTION[0], RESOLUTION[1])
    window.mainloop(fps = 60)