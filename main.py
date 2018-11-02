import ctypes, ctypes.wintypes
from ctypes import *
import threading

window = None

class Win32Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        mb = ctypes.cdll.LoadLibrary("node.dll")
        mb.wkeInitialize()

        global window
        window = mb.wkeCreateWebWindow(0, None, 0, 0, 1024, 768)

        mb.wkeSetWindowTitleW(window, "Miniblink Python Demo")

        mb.wkeOnWindowDestroy(window, self.handleWindowDestroy, 0)

        mb.wkeMoveToCenter(window)
        mb.wkeShowWindow(window, True)
        mb.wkeLoadURLW(window, "https://baidu.com/")

        msg = ctypes.wintypes.MSG()
        lpMsg = ctypes.byref(msg)

        while ctypes.windll.user32.GetMessageW(lpMsg, 0, 0, 0) > 0:
            ctypes.windll.user32.TranslateMessage(lpMsg)
            ctypes.windll.user32.DispatchMessageW(lpMsg)

    @CFUNCTYPE(c_bool, c_int, c_void_p)
    def handleWindowDestroy(webWindow, param):
        global window
        window = None
        ctypes.windll.user32.PostQuitMessage(0)

Win32 = Win32Thread()
Win32.start()