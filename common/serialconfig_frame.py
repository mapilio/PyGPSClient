"""
Generic serial port configuration Frame subclass
for use in tkinter applications which require a
serial port configuration facility.

Created on 24 Dec 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from tkinter import (
    Frame,
    Listbox,
    Scrollbar,
    Spinbox,
    Checkbutton,
    Button,
    Label,
    IntVar,
    DoubleVar,
    StringVar,
    N,
    S,
    E,
    W,
    LEFT,
    VERTICAL,
    HORIZONTAL,
    NORMAL,
    DISABLED,
)

from serial.tools.list_ports import comports
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE


ADVOFF = "\u25bc"
ADVON = "\u25b2"
READONLY = "readonly"
PARITIES = {
    "None": PARITY_NONE,
    "Even": PARITY_EVEN,
    "Odd": PARITY_ODD,
    "Mark": PARITY_MARK,
    "Space": PARITY_SPACE,
}
# These ranges can be overridden via keyword arguments:
# (the default value will be the first in the range)
BAUDRATE_RNG = (9600, 19200, 38400, 57600, 115200, 4800)
DATABITS_RNG = (8, 5, 6, 7)
STOPBITS_RNG = (1, 1.5, 2)
PARITY_RNG = list(PARITIES.keys())
TIMEOUT_RNG = ("None", "0", "1", "2", "5", "10", "20")
BGCOL = "azure"


class SerialConfigFrame(
    Frame
):  # pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    Serial port configuration frame class.
    """

    def __init__(self, container, *args, **kwargs):
        """
        Constructor.

        :param tkinter.Frame container: reference to container frame
        :param args: optional args to pass to Frame parent class
        :param kwargs: optional kwargs for value ranges, or to pass to Frame parent class
        """

        self._baudrate_rng = kwargs.pop("baudrates", BAUDRATE_RNG)
        self._databits_rng = kwargs.pop("databits", DATABITS_RNG)
        self._stopbits_rng = kwargs.pop("stopbits", STOPBITS_RNG)
        self._parity_rng = kwargs.pop("parities", PARITY_RNG)
        self._timeout_rng = kwargs.pop("timeouts", TIMEOUT_RNG)
        self._preselect = kwargs.pop("preselect", ())
        self._readonlybg = kwargs.pop("readonlybackground", BGCOL)

        Frame.__init__(self, container, *args, **kwargs)

        self._show_advanced = False
        self._noports = True
        self._ports = ()
        self._port = StringVar()
        self._port_desc = StringVar()
        self._baudrate = IntVar()
        self._databits = IntVar()
        self._stopbits = DoubleVar()
        self._parity = StringVar()
        self._rtscts = IntVar()
        self._xonxoff = IntVar()
        self._timeout = StringVar()

        self._body()
        self._do_layout()
        self._get_ports()
        self._attach_events()
        self.reset()

    def _body(self):
        """
        Set up widgets.
        """

        self._frm_basic = Frame(self)
        self._lbl_port = Label(self._frm_basic, text="Port")
        self._lbx_port = Listbox(
            self._frm_basic,
            border=2,
            relief="sunken",
            bg=self._readonlybg,
            width=28,
            height=5,
            justify=LEFT,
            exportselection=False,
        )
        self._scr_portv = Scrollbar(self._frm_basic, orient=VERTICAL)
        self._scr_porth = Scrollbar(self._frm_basic, orient=HORIZONTAL)
        self._lbx_port.config(yscrollcommand=self._scr_portv.set)
        self._lbx_port.config(xscrollcommand=self._scr_porth.set)
        self._scr_portv.config(command=self._lbx_port.yview)
        self._scr_porth.config(command=self._lbx_port.xview)
        self._lbl_baudrate = Label(self._frm_basic, text="Baud rate")
        self._spn_baudrate = Spinbox(
            self._frm_basic,
            values=self._baudrate_rng,
            width=8,
            state=READONLY,
            readonlybackground=self._readonlybg,
            wrap=True,
            textvariable=self._baudrate,
        )
        self._btn_toggle = Button(
            self._frm_basic, text=ADVOFF, width=3, command=self._on_toggle_advanced
        )

        self._frm_advanced = Frame(self)
        self._lbl_databits = Label(self._frm_advanced, text="Data Bits")
        self._spn_databits = Spinbox(
            self._frm_advanced,
            values=self._databits_rng,
            width=3,
            state=READONLY,
            readonlybackground=self._readonlybg,
            wrap=True,
            textvariable=self._databits,
        )
        self._lbl_stopbits = Label(self._frm_advanced, text="Stop Bits")
        self._spn_stopbits = Spinbox(
            self._frm_advanced,
            values=self._stopbits_rng,
            width=3,
            state=READONLY,
            readonlybackground=self._readonlybg,
            wrap=True,
            textvariable=self._stopbits,
        )
        self._lbl_parity = Label(self._frm_advanced, text="Parity")
        self._spn_parity = Spinbox(
            self._frm_advanced,
            values=self._parity_rng,
            width=6,
            state=READONLY,
            readonlybackground=self._readonlybg,
            wrap=True,
            textvariable=self._parity,
        )
        self._chk_rts = Checkbutton(
            self._frm_advanced, text="RTS/CTS", variable=self._rtscts
        )
        self._chk_xon = Checkbutton(
            self._frm_advanced, text="Xon/Xoff", variable=self._xonxoff
        )
        self._lbl_timeout = Label(self._frm_advanced, text="Timeout (s)")
        self._spn_timeout = Spinbox(
            self._frm_advanced,
            values=self._timeout_rng,
            width=4,
            state=READONLY,
            readonlybackground=self._readonlybg,
            wrap=True,
            textvariable=self._timeout,
        )

    def _do_layout(self):
        """
        Layout widgets.
        """

        self._frm_basic.grid(column=0, row=0, columnspan=4, sticky=(W, E))
        self._lbl_port.grid(column=0, row=0, sticky=(W))
        self._lbx_port.grid(column=1, row=0, sticky=(W, E), padx=3, pady=3)
        self._scr_portv.grid(column=2, row=0, sticky=(N, S))
        self._scr_porth.grid(column=1, row=1, sticky=(E, W))
        self._lbl_baudrate.grid(column=0, row=2, sticky=(W))
        self._spn_baudrate.grid(column=1, row=2, sticky=(W), padx=3, pady=3)
        self._btn_toggle.grid(column=2, row=2, sticky=(E))

        self._frm_advanced.grid_forget()
        self._lbl_databits.grid(column=0, row=0, sticky=(W))
        self._spn_databits.grid(column=1, row=0, sticky=(W), padx=3, pady=3)
        self._lbl_stopbits.grid(column=2, row=0, sticky=(W))
        self._spn_stopbits.grid(column=3, row=0, sticky=(W), padx=3, pady=3)
        self._lbl_parity.grid(column=0, row=1, sticky=(W))
        self._spn_parity.grid(column=1, row=1, sticky=(W), padx=3, pady=3)
        self._chk_rts.grid(column=2, row=1, sticky=(W))
        self._chk_xon.grid(column=3, row=1, sticky=(W), padx=3, pady=3)
        self._lbl_timeout.grid(column=0, row=2, sticky=(W))
        self._spn_timeout.grid(column=1, row=2, sticky=(W), padx=3, pady=3)

    def _attach_events(self):
        """
        Bind events to widgets.
        """

        self._lbx_port.bind("<<ListboxSelect>>", self._on_select_port)

    def _get_ports(self):
        """
        Populate list of available serial ports using pyserial comports tool.

        Attempt to automatically select a serial device matching
        a list of 'preselect' devices (only works on platforms
        which parse UART device desc or HWID e.g. Posix).
        """

        self._ports = sorted(comports())
        init_idx = 0
        port = ""
        desc = ""
        if len(self._ports) > 0:
            for idx, (port, desc, _) in enumerate(self._ports, 1):
                self._lbx_port.insert(idx, port + ": " + desc)
                for dev in self._preselect:
                    if dev in desc:
                        init_idx = idx
                        break
            self._noports = False
        else:
            self._noports = True
            self.enable_controls(True)
        self._lbx_port.activate(init_idx)
        self._port.set(port)
        self._port_desc.set(desc)

    def _on_select_port(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Get selected port from listbox and set global variable.
        """

        idx = self._lbx_port.curselection()
        if idx == "":
            idx = 0
        port_orig = self._lbx_port.get(idx)
        port = port_orig[0: port_orig.find(":")]
        desc = port_orig[port_orig.find(":") + 1:]
        if desc == "":
            desc = "device"
        self._port.set(port)
        self._port_desc.set(desc)

    def _on_toggle_advanced(self):
        """
        Toggle advanced serial port settings panel on or off.
        """

        self._show_advanced = not self._show_advanced
        if self._show_advanced:
            self._frm_advanced.grid(column=0, row=1, columnspan=3, sticky=(W, E))
            self._btn_toggle.config(text=ADVON)
        else:
            self._frm_advanced.grid_forget()
            self._btn_toggle.config(text=ADVOFF)

    def enable_controls(self, disabled: bool=False):
        """
        Enable or disable controls (e.g. to prevent
        changes when serial device is connected).

        :param bool disabled: disable controls flag
        """

        for widget in (
            self._lbl_port,
            self._lbl_baudrate,
            self._lbl_databits,
            self._lbl_stopbits,
            self._lbl_parity,
            self._lbl_timeout,
            self._chk_rts,
            self._chk_xon,
            self._lbx_port,
        ):
            widget.configure(state=(DISABLED if disabled else NORMAL))
        for widget in (
            self._spn_baudrate,
            self._spn_databits,
            self._spn_stopbits,
            self._spn_parity,
            self._spn_timeout,
        ):
            widget.configure(state=(DISABLED if disabled else READONLY))

    def reset(self):
        """
        Reset settings to defaults (first value in range).
        """

        self._baudrate.set(self._baudrate_rng[0])
        self._databits.set(self._databits_rng[0])
        self._stopbits.set(self._stopbits_rng[0])
        self._parity.set(self._parity_rng[0])
        self._rtscts.set(False)
        self._xonxoff.set(False)
        self._timeout.set(self._timeout_rng[0])

    @property
    def noports(self) -> bool:
        """
        Getter for noports flag, which indicates if there are
        no serial ports available.

        :return: noports flag (True/False)
        :rtype: bool
        """

        return self._noports

    @property
    def port(self) -> str:
        """
        Getter for port.

        :return: selected port
        :rtype: str
        """

        return self._port.get()

    @property
    def port_desc(self) -> str:
        """
        Getter for port description.

        :return: selected port description
        :rtype: str
        """

        return self._port_desc.get()

    @property
    def baudrate(self) -> int:
        """
        Getter for baudrate.

        :return: selected baudrate
        :rtype: int
        """

        return self._baudrate.get()

    @property
    def databits(self) -> int:
        """
        Getter for databits.

        :return: selected databits
        :rtype: int
        """

        return self._databits.get()

    @property
    def stopbits(self) -> float:
        """
        Getter for stopbits.

        :return: selected stopbits
        :rtype: float
        """

        return self._stopbits.get()

    @property
    def parity(self) -> str:
        """
        Getter for parity.

        :return: selected parity
        :rtype: str
        """

        return PARITIES[self._parity.get()]

    @property
    def rtscts(self) -> bool:
        """
        Getter for rts/cts.

        :return: selected rts/cts
        :rtype: bool
        """

        return self._rtscts.get()

    @property
    def xonxoff(self) -> bool:
        """
        Getter for xon/xoff.

        :return: selected xon/xoff
        :rtype: bool
        """

        return self._xonxoff.get()

    @property
    def timeout(self) -> float:
        """
        Getter for timeout.

        :return: selected timeout
        :rtype: float (or None)
        """

        if self._timeout.get() == "None":
            return None
        return float(self._timeout.get())
