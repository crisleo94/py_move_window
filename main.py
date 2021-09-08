import ctypes
from ctypes import wintypes
from tkinter import Tk, ttk

user32 = ctypes.windll.user32
root = Tk()

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(
    ctypes.c_int), ctypes.POINTER(ctypes.c_int))

win_titles = []
win_handles = []
win_coords = []


def main_layout():
    root.title('Window Reminder')
    root.geometry('500x500')
    ttk.Button(root, text='Find Windows', command=show,
               width=50, padding=2).grid()
    ttk.Labelframe()
    root.mainloop()


def show():
    print('Button clicked!!')


def foreach_window(hwnd, lParam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if buff.value != '':
            win_titles.append(buff.value)
            print(buff.value)
    return win_titles


def find_window(window_list):
    for window in window_list:
        found_window = user32.FindWindowW(None, window)
        user32.ShowWindow(found_window, 9)


def find_window_location(window_list):
    rect = wintypes.RECT()
    for window in window_list:
        window_position = user32.GetWindowRect(window, ctypes.pointer(rect))
    return window_position.left, window_position.right, window_position.top, window_position.bottom

# non-zero value for handle should mean it found a window that matches
# Bring window to front

# Get info with rect(rect.left, rect.right, rect.top, rect.bottom)

# move window using handle
# MoveWindow(handle, x, y, height, width, repaint(bool))


if __name__ == '__main__':
    print('Running...')
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    main_layout()
