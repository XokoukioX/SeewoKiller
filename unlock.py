import webbrowser  # 导入webbrowser模块，用于打开网页
import threading  # 导入threading模块，用于多线程处理
import time  # 导入time模块，用于时间控制
import datetime  # 导入datetime模块，用于日期时间操作
import win32api  # 导入win32api模块，用于Windows API调用
import win32gui  # 导入win32gui模块，用于Windows图形用户界面操作
import win32con  # 导入win32con模块，用于Windows常量定义
import winreg  # 导入winreg模块，用于Windows注册表操作
import os  # 导入os模块，用于操作系统相关功能
import pystray  # 导入pystray模块，用于创建系统托盘图标
from pystray import MenuItem as item, Menu  # 从pystray中导入MenuItem和Menu
from PIL import Image, ImageDraw  # 从PIL导入Image和ImageDraw，用于图像处理
import ctypes  # 导入ctypes模块，用于调用C函数库
import sys  # 导入sys模块，用于系统特定的参数和函数
from win10toast import ToastNotifier

# 获取当前脚本的文件名
current_file = os.path.basename(__file__)
def show_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=4)

# 检查是否以管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 如果没有管理员权限，则重新启动脚本并请求管理员权限
if is_admin():
    print("管理员身份启动成功")
    print("当前文件名:", current_file)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
    sys.exit(0)

# 获取窗口大小
def getsize(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return width, height

windows = []  # 存储符合条件的窗口句柄
desk = win32gui.GetDesktopWindow()  # 获取桌面窗口句柄
w1, h1 = getsize(desk)  # 获取桌面窗口大小
path = os.path.abspath("") + "\\" + "unlock_usb.exe"  # 获取unlock_usb.exe的绝对路径

# 枚举所有窗口，并找到名为“希沃管家”的窗口
def getwindows(hwnd, mouse):
    w2, h2 = getsize(hwnd)
    if win32gui.GetWindowText(hwnd) == "希沃管家" and abs(h1 - h2) < 100 and abs(w1 - w2) < 100:
        windows.append(hwnd)

# 隐藏符合条件的窗口，并记录日志
def unlock():
    on = True
    while True:
        windows.clear()
        try:
            win32gui.EnumWindows(getwindows, 0)
            for win in windows:
                win32gui.SetWindowPos(win, win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_HIDEWINDOW | win32con.SWP_NOOWNERZORDER)
                if on:
                    show_notification('(`ゥ´)', '已经绕过锁屏')
                    with open("log.txt", "a") as f:
                        f.write("unlock at " + str(datetime.datetime.now()) + "\n")
                    on = False
                    AutoRun("open")
        except Exception:
            pass
        time.sleep(1)
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

# 检查注册表键是否存在
def Judge_Key(key_name, reg_root=win32con.HKEY_CURRENT_USER, reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"):
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        feedback = 0
    except FileNotFoundError:
        feedback = 1
    except PermissionError:
        feedback = 2
    except Exception:
        feedback = 3
    return feedback

# 添加或删除注册表中的自启动项
def AutoRun(switch, current_file):
    judge_key = Judge_Key(current_file)
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == "open":
        try:
            if judge_key == 0:
                win32api.MessageBox(0, "已经开启了，无需再开启", "提示", win32con.MB_OK)
            elif judge_key == 1:
                win32api.RegSetValueEx(key, current_file, 0, win32con.REG_SZ, path)
                win32api.RegCloseKey(key)
                win32api.MessageBox(0, "开机自启动添加成功！", "提示", win32con.MB_OK)
        except:
            win32api.MessageBox(0, '添加失败', "提示", win32con.MB_OK)
    elif switch == "close":
        try:
            if judge_key == 0:
                win32api.RegDeleteValue(key, current_file)
                win32api.RegCloseKey(key)
            elif judge_key == 1:
                win32api.MessageBox(0, "键不存在,按右上角关闭键进行添加", "提示", win32con.MB_OK)
            elif judge_key == 2:
                win32api.MessageBox(0, "权限不足", "提示", win32con.MB_OK)
            else:
                win32api.MessageBox(0, '出现错误！', "提示", win32con.MB_OK)
        except:
            win32api.MessageBox(0, "删除失败", "提示", win32con.MB_OK)

# 从文件加载图像并清理ICC配置文件
def create_image_from_file(file_path):
    image = Image.open(file_path)
    image.info.pop('icc_profile', None)  # 删除ICC配置文件以避免警告
    return image

# 获取自启动权限
def get():
    AutoRun("close", current_file)
    AutoRun("open", current_file)

# 取消自启动
def q():
    AutoRun("close", current_file)

def update_raw():
    webbrowser.open("https://www.123pan.com/s/00ErVv-OpxJ.html")

def author_github_repository():
    webbrowser.open("https://github.com/XokoukioX/SeewoKiller")

def author_github_repository_nuaa_cf():
    webbrowser.open("https://hub.nuaa.cf/XokoukioX/SeewoKiller")

# 打开更新页面

# 打开开发者的B站空间
def gotobrowser():
    webbrowser.open("https://space.bilibili.com/544645801")

# 显示开发者信息
def author_github_homepage():
    webbrowser.open("https://github.com/XokoukioX")

update = Menu(
    item('原作者通道', update_raw),
    item('修改版通道', author_github_repository),
    item('修改版通道(打不开时用这个)', author_github_repository_nuaa_cf)
)

# 关于开发者二级菜单
about_menu = Menu(
    item('原作者:主播潘丽娟', gotobrowser),
    item('修改者:Kawakaze', author_github_homepage)
)

# 退出托盘图标并要求输入密码
def quit_window(icon, item):
    icon.stop()

# 启动隐藏窗口线程
threading._start_new_thread(unlock, ())

# 从文件加载自定义图标
icon_image_path = "./icon.png"  # 替换为你的图标文件路径
image = create_image(64, 64, 'black', 'white')

# 创建托盘图标和菜单
menu = Menu(
    item('关于开发者', about_menu),
    item("启用开机自启动", get),
    item("取消开机自启动", q),
    item("获取更新", update),
    item('退出', quit_window)
)

icon = pystray.Icon("name", image, "SeewoKiller-希沃锁屏杀手", menu)
icon.run()
