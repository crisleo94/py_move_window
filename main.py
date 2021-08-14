import ctypes
import time
from ctypes import wintypes

from simple_chalk import chalk

user32 = ctypes.windll.user32

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(
    ctypes.c_int),     ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
rect = wintypes.RECT()

titles = []
matched_titles = []
terminal = '@crist'  # if you have ur powershell profile modified be sure to include the username here, otherwise just powershell
navigator = 'Mozilla Firefox'  # the browser you want to match
editor = 'Visual Studio Code'  # the editor/ide you want to match
matched_terminal = ''
matched_navigator = ''
matched_editor = ''


def foreach_window(hwnd, lParam):

    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if navigator in buff.value or editor in buff.value or terminal in buff.value:
            matched_titles.append(buff.value)
        titles.append(buff.value)
    return titles


EnumWindows(EnumWindowsProc(foreach_window), 0)

for title in matched_titles:
    if terminal in title:
        matched_terminal = title
    elif navigator in title:
        matched_navigator = title
    elif editor in title:
        matched_editor = title

time.sleep(1)
print(chalk.green(f'Terminal value found: {matched_terminal}'))
time.sleep(1)
print(chalk.green(f'Navigator value found: {matched_navigator}'))
time.sleep(1)
print(chalk.green(f'Editor value found: {matched_editor}'))
time.sleep(1)

# get handle for Notepad window
# non-zero value for handle should mean it found a window that matches
wterminal = user32.FindWindowW(None, matched_terminal)
wnavigator = user32.FindWindowW(None, matched_navigator)
weditor = user32.FindWindowW(None, matched_editor)
time.sleep(2)
ff = user32.GetWindowRect(wterminal, ctypes.pointer(rect))
print(chalk.blue(
    f'Coords for terminal, X:{rect.left}, Y: {rect.top}, HEIGHT: {rect.right}, WIDTH: {rect.bottom}'))

time.sleep(2)
ff2 = user32.GetWindowRect(wnavigator, ctypes.pointer(rect))
print(chalk.blue(
    f'Coords for Browser, X:{rect.left}, Y: {rect.top}, HEIGHT: {rect.right}, WIDTH: {rect.bottom}'))

time.sleep(2)
ff3 = user32.GetWindowRect(weditor, ctypes.pointer(rect))
print(chalk.blue(
    f'Coords for Editor, X:{rect.left}, Y: {rect.top}, HEIGHT: {rect.right}, WIDTH: {rect.bottom}'))

# meaning of 2nd parameter defined here
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx
# minimize window using handle
# user32.ShowWindow(handle, 6)
# maximize window using handle
# user32.ShowWindow(handle, 9)

# move window using handle
# MoveWindow(handle, x, y, height, width, repaint(bool))
if wterminal and wnavigator and weditor != 0:
    time.sleep(2)
    print(chalk.yellowBright('Moving window...'))
    time.sleep(2)
    user32.MoveWindow(wterminal, -5, 713, 972, 340, True)
    print(chalk.yellowBright('Moving window...'))
    time.sleep(2)
    user32.MoveWindow(wnavigator, 955, 0, 960, 1045, True)
    print(chalk.yellowBright('Moving window...'))
    time.sleep(2)
    user32.MoveWindow(weditor, 0, 0, 963, 714, True)
    time.sleep(2)
    print(chalk.green('Specified windows have been moved!'))
else:
    print(chalk.red('No windows found!'))
