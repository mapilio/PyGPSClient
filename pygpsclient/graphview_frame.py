'''
Graphview frame class for PyGPSClient application.

This handles a frame containing a graph of current satellite reception.

Created on 14 Sep 2020

@author: semuadmin
'''

from tkinter import Frame, Canvas, font, BOTH, YES

from pygpsclient.globals import hsv2rgb, WIDGETU2, BGCOL, FGCOL

# Relative offsets of graph axes
AXIS_XL = 19
AXIS_XR = 10
AXIS_Y = 18
MAX_NUM_SATS = 17
MAX_SNR = 50


class GraphviewFrame(Frame):
    '''
    Frame inheritance class for plotting satellite view.
    '''

    def __init__(self, app, *args, **kwargs):
        '''
        Constructor.
        '''

        self.__app = app  # Reference to main application class
        self.__master = self.__app.get_master()  # Reference to root class (Tk)

        Frame.__init__(self, self.__master, *args, **kwargs)

        def_w, def_h = WIDGETU2
        self.width = kwargs.get('width', def_w)
        self.height = kwargs.get('height', def_h)
        self._bgcol = BGCOL
        self._fgcol = FGCOL
        self._body()

        self.bind("<Configure>", self._on_resize)

    def _body(self):
        '''
        Set up frame and widgets.
        '''

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.can_graphview = Canvas(self, width=self.width, height=self.height, bg=self._bgcol)
        self.can_graphview.pack(fill=BOTH, expand=YES)

    def init_graph(self):
        '''
        Initialise graph view
        '''

        w, h = self.width, self.height
        resize_font = font.Font(size=min(int(h / 25), 10))
        ticks = int(MAX_SNR / 10)
        self.can_graphview.delete("all")
        self.can_graphview.create_line(AXIS_XL, 5, AXIS_XL , h - AXIS_Y, fill=self._fgcol)
        self.can_graphview.create_line(w - AXIS_XR, 5 , w - AXIS_XR, h - AXIS_Y,
                                       fill=self._fgcol)
        for i in range(ticks, 0, -1):
            y = (h - AXIS_Y) * i / ticks
            self.can_graphview.create_line(AXIS_XL, y, w - AXIS_XR, y, fill=self._fgcol)
            self.can_graphview.create_text(10, y, text=str(MAX_SNR - (i * 10)), angle=90,
                                           fill=self._fgcol, font=resize_font)
        self.can_graphview.create_text(10, (h - AXIS_Y - 1) / 2, text="snr", angle=90,
                                       fill="cyan", font=resize_font)

    def update_graph(self, data):
        '''
        Plot satellites' elevation and azimuth position.
        '''

        w, h = self.width, self.height
        self.init_graph()

        offset = AXIS_XL + 1
        colwidth = (w - AXIS_XL - AXIS_XR) / MAX_NUM_SATS
        resize_font = font.Font(size=min(int(colwidth / 2), 10))
        for d in data:
            prn, _, _, snr = d
            if snr == '':
                snr = 1
            else:
                snr = int(snr)
            snr_y = int(snr) * (h - AXIS_Y - 1) / MAX_SNR
            self.can_graphview.create_rectangle(offset, h - AXIS_Y - 1, offset + colwidth,
                                                h - AXIS_Y - 1 - snr_y,
                                                fill=hsv2rgb(snr / 100, .8, .8))
            self.can_graphview.create_text(offset + colwidth / 2, h - 10, text=prn,
                                           fill=self._fgcol, font=resize_font)
            offset += colwidth

        self.can_graphview.update()

    def _on_resize(self, event):
        '''
        Resize frame
        '''

        self.width, self.height = self.get_size()

    def get_size(self):
        '''
        Get current canvas size.
        '''

        self.update_idletasks()  # Make sure we know about any resizing
        width = self.can_graphview.winfo_width()
        height = self.can_graphview.winfo_height()
        return (width, height)
