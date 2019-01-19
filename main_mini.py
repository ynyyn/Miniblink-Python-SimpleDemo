import ctypes, ctypes.wintypes
from ctypes import *
import threading

webview = mb = None


class Win32Thread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        global webview, mb

        mb = ctypes.cdll.LoadLibrary("node.dll")
        mb.wkeInitialize()

        webview = mb.wkeCreateWebWindow(
            0, # WKE_WINDOW_TYPE_POPUP
            None, 0, 0,
            1024, 768 # width, height
        )
        mb.wkeMoveToCenter(webview)

        mb.wkeSetWindowTitleW(webview, "Miniblink Python Demo")

        mb.wkeOnWindowDestroy(webview, handleWindowDestroy, 0)

        mb.wkeShowWindow(webview, True)

        mb.wkeLoadURLW(webview, "https://baidu.com/")

        msg = ctypes.wintypes.MSG()
        lpMsg = ctypes.byref(msg)

        while ctypes.windll.user32.GetMessageW(lpMsg, 0, 0, 0) > 0:
            ctypes.windll.user32.TranslateMessage(lpMsg)
            ctypes.windll.user32.DispatchMessageW(lpMsg)

        mb.wkeFinalize()


@CFUNCTYPE(None, c_int, c_void_p)
def handleWindowDestroy(webView, param):
    """Callback: Window has been destroyed.
    """
    global webview
    webview = None
    # break the Win32 message loop to exit after window being destroyed.
    ctypes.windll.user32.PostQuitMessage(0)


if __name__ == '__main__':
    Win32 = Win32Thread()
    Win32.start()