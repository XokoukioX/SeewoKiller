import webbrowser
import threading
import time
import datetime
import win32api
import win32gui
import win32con
import winreg
import os
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
   print("yes") 
else:
    ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable,"", None, 1)
    sys.exit(0)
def getsize(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    widgh = right - left
    height = bottom - top
    return widgh,height

windows = [] 
desk = win32gui.GetDesktopWindow()
w1, h1 = getsize(desk)
path = os.path.abspath("") + "\\" + "unlock_usb.exe"

def getwindows(hwnd, mouse):
    w2, h2 = getsize(hwnd)
    if win32gui.GetWindowText(hwnd) == "希沃管家" and abs(h1 - h2) < 100 and abs(w1 - w2) < 100:
        windows.append(hwnd)
def unlock():
    on = True
    while True:
        windows.clear()
        try:
            win32gui.EnumWindows(getwindows, 0)
            for win in windows:
                win32gui.SetWindowPos(win,win32con.HWND_BOTTOM,0,0,0,0,win32con.SWP_HIDEWINDOW | win32con.SWP_NOOWNERZORDER)
                if on:
                    show_notification('希沃杀手', '已经绕过锁屏')
                    with open("log.txt", "a") as f:
                        f.write("unlock at " + str(datetime.datetime.now()) + "\n")
                    on = False
            time.sleep(1)
        except Exception:
            time.sleep(1)

def Judge_Key(key_name,
              reg_root=win32con.HKEY_CURRENT_USER,
              reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
              ):
    
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        feedback=0
    except FileNotFoundError as e:
        feedback =1
    except PermissionError as e:
        feedback = 2
    except Exception:
        feedback = 3
    return  feedback

def AutoRun(switch,
            zdynames,
            current_file,
            path,on):
    judge_key = Judge_Key(reg_root=win32con.HKEY_CURRENT_USER,
                          reg_path=r"Software\Microsoft\Windows\CurrentVersion\Run",  
                          key_name=current_file)
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == "open":
        
        try:
            if judge_key==0:
                win32api.MessageBox(0,"已经开启了，无需再开启","提示",win32con.MB_OK)
            elif judge_key==1:
                win32api.RegSetValueEx(key, current_file, 0, win32con.REG_SZ, path)
                win32api.RegCloseKey(key)
                win32api.MessageBox(0,"开机自启动添加成功！","提示",win32con.MB_OK)

        except:
            win32api.MessageBox(0,'添加失败',"提示",win32con.MB_OK) 
    elif switch =="close":
        try:
            if judge_key==0:
                win32api.RegDeleteValue(key, current_file)  
                win32api.RegCloseKey(key)
                if on:
                    win32api.MessageBox(0,'成功删除键！',"提示",win32con.MB_OK) 
            elif judge_key==1 and on:
                win32api.MessageBox(0,"键不存在","提示",win32con.MB_OK)
        
            elif judge_key==2 and on:
                win32api.MessageBox(0,"权限不足","提示",ArithmeticErrorwin32con.MB_OK)
            elif on:
                win32api.MessageBox(0,'出现错误！',"提示",win32con.MB_OK)
        except:
            win32api.MessageBox(0,"删除失败","提示",win32con.MB_OK)

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def get():
    AutoRun("close", "unlock.exe", "unlock", path, 0)
    AutoRun("open", "unlock.exe", "unlock", path, 1)

def q():
    AutoRun("close", "unlock.exe", "unlock", path, 1)      

def update():
    webbrowser.open("https://www.123pan.com/s/00ErVv-OpxJ.html")
    
def gotobrowser():
    webbrowser.open("https://space.bilibili.com/544645801")

def about():
    gotobrowser()
    
def quit_window(icon, item):
   icon.stop()

threading._start_new_thread(unlock,())
image = create_image(64, 64, 'black', 'white')
menu=(item('退出', quit_window), item('关于开发者', about), item("获取自启动权限",get), item("取消开机自启动",q), item("获取更新", update))
icon=pystray.Icon("name", image, "yynb", menu)
icon.run()
