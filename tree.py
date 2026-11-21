import math, time, os, random

# 終端機 ANSI 色彩代碼
RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
BROWN = "\033[33m"
WHITE = "\033[97m"
GIFT_COLORS = ["\033[91m", "\033[94m", "\033[95m", "\033[96m"]
LIGHT_COLORS = ["\033[91m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]

def render_tree():
    # 在 Windows 命令提示字元中啟用 ANSI 顏色支援
    if os.name == 'nt':
        os.system('')

    width, height = 64, 30
    angle = 0
    frame = 0
    # 初始化 35 片隨機飄落的雪花座標 [x, y]
    snowflakes = [[random.randint(0, width - 1), random.randint(0, height - 1)] for _ in range(35)]

    # 隱藏游標讓動畫更流暢
    print("\033[?25l", end="")

    try:
        while True:
            buffer = [[' ' for _ in range(width)] for _ in range(height)]
            zbuffer = [[-999.0 for _ in range(width)] for _ in range(height)]

            # 1. 更新並繪製背景飄雪
            for flake in snowflakes:
                sx, sy = flake
                if 0 <= sx < width and 0 <= sy < height:
                    buffer[sy][sx] = f"{WHITE}*{RESET}" if (sx + sy) % 2 == 0 else f"{WHITE}.{RESET}"
                flake[1] += 1  # 往下飄
                flake[0] += random.choice([-1, 0, 0, 1])  # 微微左右搖晃
                if flake[1] >= height:
                    flake[1] = 0
                    flake[0] = random.randint(0, width - 1)

            # 2. 繪製底部禮物盒（放在地面兩側）
            gifts = [
                (int(width / 2) - 11, 26, GIFT_COLORS[0]),
                (int(width / 2) - 7,  27, GIFT_COLORS[1]),
                (int(width / 2) + 5,  27, GIFT_COLORS[2]),
                (int(width / 2) + 9,  26, GIFT_COLORS[3]),
            ]
            for gx, gy, gcolor in gifts:
                if 0 <= gx < width - 2 and 0 <= gy < height - 1:
                    buffer[gy][gx]     = f"{gcolor}[{RESET}"
                    buffer[gy][gx + 1] = f"{YELLOW}+{RESET}"
                    buffer[gy][gx + 2] = f"{gcolor}]{RESET}"

            # 3. 繪製 3D 螺旋聖誕樹本體與閃爍彩燈
            for y_step in range(200):
                h = y_step / 200.0
                radius = h * 17.0
                theta = y_step * 0.35 + angle

                x = radius * math.cos(theta)
                z = radius * math.sin(theta)
                y = h * 22.0

                screen_x = int(width / 2 + x * 1.6)
                screen_y = int(3 + y)

                if 0 <= screen_x < width and 0 <= screen_y < height:
                    if z > zbuffer[screen_y][screen_x]:
                        zbuffer[screen_y][screen_x] = z
                        if y_step % 11 == 0:
                            # 彩燈隨時間閃爍變色
                            lcolor = LIGHT_COLORS[(y_step + frame // 3) % len(LIGHT_COLORS)]
                            buffer[screen_y][screen_x] = f"{lcolor}●{RESET}"
                        elif z > 0:
                            buffer[screen_y][screen_x] = f"{BRIGHT_GREEN}*{RESET}"
                        else:
                            buffer[screen_y][screen_x] = f"{GREEN}.{RESET}"

            # 4. 繪製樹幹
            for ty in range(25, 28):
                for tx in range(int(width / 2) - 2, int(width / 2) + 3):
                    buffer[ty][tx] = f"{BROWN}#{RESET}"

            # 5. 繪製頂端發光大星星
            star_x = int(width / 2)
            buffer[2][star_x] = f"{YELLOW}★{RESET}"

            # 將游標移回左上角覆蓋畫面（比 clear 更不會閃屏）
            print("\033[H" + '\n'.join(''.join(row) for row in buffer))

            angle += 0.12
            frame += 1
            time.sleep(0.06)

    except KeyboardInterrupt:
        pass
    finally:
        # 恢復顯示游標
        print("\033[?25h" + RESET + "\n🎄 聖誕快樂！動畫已停止。")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    render_tree()
