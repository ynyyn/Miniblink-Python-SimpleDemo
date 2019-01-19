import ctypes, ctypes.wintypes
from ctypes import *
import threading

webview = window_handle = mb = None


class Win32Thread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        global webview, window_handle, mb

        mb = ctypes.cdll.LoadLibrary("node.dll")

        mb.wkeInitialize()
        webview = mb.wkeCreateWebWindow(
            0, # WKE_WINDOW_TYPE_POPUP
            None, 0, 0,
            1024, 768 # width, height
        )
        mb.wkeMoveToCenter(webview)

        window_handle = mb.wkeGetWindowHandle(webview)

        mb.wkeSetWindowTitleW(webview, "Miniblink Python Demo")

        mb.wkeOnNavigation(webview, handleNavigation, 0)
        mb.wkeOnTitleChanged(webview, handleTitleChanged, 0)
        mb.wkeOnDocumentReady(webview, handleDocumentReady, 0)
        mb.wkeOnWindowClosing(webview, handleWindowClosing, 0)
        mb.wkeOnWindowDestroy(webview, handleWindowDestroy, 0)

        mb.wkeSetDebugConfig(webview, "drawMinInterval".encode(), "1".encode())
        mb.wkeSetDebugConfig(webview, "wakeMinInterval".encode(), "1".encode())
        mb.wkeSetDebugConfig(webview, "antiAlias".encode(), "1".encode())

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
    global webview, window_handle
    print("[Event]", "Window has been destroyed.")

    webview = window_handle = None

    # break the Win32 message loop to exit after window being destroyed.
    ctypes.windll.user32.PostQuitMessage(0)


@CFUNCTYPE(c_bool, c_int, c_void_p)
def handleWindowClosing(webView, param):
    """Callback: Window's close button clicked.\n
    Return True to allow closing or False to reject.
    """
    global mb, webview, window_handle
    print("[Event]", "Close button clicked.")

    msgbox_title = "Miniblink Python Demo"
    msgbox_head = "Are you sure you want to exit?"
    msgbox_content = "(from callback <handleWindowClosing>)"
    try:
        nButtonPressed = c_int()
        ret = ctypes.windll.Comctl32.TaskDialog(
            window_handle, None,
            msgbox_title, msgbox_head, msgbox_content,
            2 | 4 | 8, # TDCBF_*_BUTTON *(YES|NO|CANCEL)
            65533, # TD_INFORMATION_ICON
            ctypes.byref(nButtonPressed)
        )
        assert (ret == 0)
        ret = nButtonPressed.value
    except:
        ret = ctypes.windll.user32.MessageBoxW(
            window_handle,
            msgbox_head + "\n" + msgbox_content, msgbox_title,
            4 | 32 # MB_YESNO=4 | MB_ICONQUESTION=32
        )

    return ret == 6 # IDYES=6


@CFUNCTYPE(c_bool, c_int, c_void_p, c_int, c_void_p)
def handleNavigation(webView, param, navigationType, url_p):
    """Callback: Webview start navigation.\n
    NOTE: All frames involved.
    """
    global mb
    url = c_wchar_p(mb.wkeGetStringW(url_p)).value
    print("[Event]", "Webview navigate:", url, "| TrigType:", navigationType)

    return True


@CFUNCTYPE(None, c_int, c_void_p, c_void_p)
def handleTitleChanged(webView, param, title_p):
    """Callback: Webview title changed.
    """
    global mb
    title = c_wchar_p(mb.wkeGetStringW(title_p)).value
    print("[Event]", "Webview title changed:", title)

    mb.wkeSetWindowTitleW(webView, "Miniblink Python Demo" + " - " + title)


@CFUNCTYPE(None, c_int, c_void_p)
def handleDocumentReady(webView, param):
    """Callback: Document ready.
    """
    global mb
    print("[Event]", "DocumentReady.")


if __name__ == '__main__':
    Win32 = Win32Thread()
    Win32.start()