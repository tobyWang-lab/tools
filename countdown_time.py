import pygame
import sys
from datetime import datetime, timedelta
import subprocess
import webbrowser

# 初始化pygame
pygame.init()

# 設定視窗大小
screen_width, screen_height = 300, 150
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

# 設定視窗位置和透明度需要使用xprop和xwininfo
# 注意：這些命令在WSL下需要安裝並且確保有圖形介面支持

def set_window_position(x, y):
    win_id = pygame.display.get_wm_info()['window']
    subprocess.run(["xdotool", "windowsize", str(win_id), str(screen_width), str(screen_height)])
    subprocess.run(["xdotool", "windowmove", str(win_id), str(x), str(y)])

def set_window_opacity(opacity):
    win_id = pygame.display.get_wm_info()['window']
    subprocess.run(["xprop", "-id", str(win_id), "-f", "_NET_WM_WINDOW_OPACITY", "32c", "-set", "_NET_WM_WINDOW_OPACITY", str(opacity)])

# 設定視窗位置（右上角）
screen_width_full = 1920  # 你的螢幕解析度寬度，可以使用xdpyinfo查詢
screen_height_full = 1080  # 你的螢幕解析度高度，可以使用xdpyinfo查詢
x = screen_width_full - screen_width - 20  # 距離右邊界20像素
y = 20  # 距離上邊界20像素

# 設定視窗位置
set_window_position(x, y)

# 設定視窗透明度
alpha = 0.9  # 透明度值（0-1），這裡用比例值
set_window_opacity(int(alpha * 0xFFFFFFFF))

# 設定字體和大小
font = pygame.font.SysFont('simsun', 36)
message_font = pygame.font.SysFont('simsun', 36)

# 設定倒數計時的時間長度
countdown_duration = timedelta(hours=9)

# 設定開始時間為今天的早上09:12:30
# time_input=input("上班時間為何(format=HH:mm:SS)=").strip().split(":")
time_input = sys.argv[1].strip().split(":")

start_time = datetime.now().replace(hour=int(time_input[0]), minute=int(time_input[1]), second=int(time_input[2]), microsecond=0)
end_time = start_time + countdown_duration
print("Start time: " + start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("End time: " + end_time.strftime("%Y-%m-%d %H:%M:%S"))

# 設定顏色
background_color = (0, 0, 0)
text_color = (255, 255, 255)

def show_message_screen():
    message_screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    message_screen.fill(background_color)
    message_text = message_font.render("該下班了喔^_^", True, text_color)
    message_rect = message_text.get_rect(center=(screen_width // 2, screen_height // 2))
    message_screen.blit(message_text, message_rect)
    pygame.display.flip()
    pygame.time.wait(5000)  # 等待5秒
    pygame.quit()
    sys.exit()


def open_notion():
    url = "https://www.notion.so/16de0299c0f08045b512cce95719722f?pvs=4"
    webbrowser.get('chrome').open_new(url)


chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

open_notion()
# 主循環
running = True
ten_minutes = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit")
            running = False

    # 計算剩餘時間
    now = datetime.now()
    remaining_time = end_time - now
    # print(remaining_time.total_seconds())
    if ten_minutes:
        if remaining_time.total_seconds() <= 600:
            # print("剩餘10分鐘")
            ten_minutes = False
            open_notion()
    if remaining_time.total_seconds() <= 0:
        # print("Remaining time < 0")
        show_message_screen()

    # 格式化剩餘時間
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    # 清屏
    screen.fill(background_color)

    # 渲染文字
    text_surface = font.render(time_str, True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)

    # 更新顯示
    pygame.display.update()
    pygame.display.flip()

    # 設置幀率
    pygame.time.Clock().tick(1)

# 退出pygame
pygame.quit()
sys.exit()
