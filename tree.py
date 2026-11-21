import math, time, os

def render_tree():
    angle = 0
    while True:
        # 畫面大小設定
        width, height = 60, 28
        buffer = [[' ' for _ in range(width)] for _ in range(height)]
        zbuffer = [[-999.0 for _ in range(width)] for _ in range(height)]

        # 畫頂端星星
        star_x = int(width / 2)
        buffer[1][star_x] = '★'

        # 畫 3D 螺旋聖誕樹本體與燈飾
        for y_step in range(180):
            h = y_step / 180.0  # 高度比例 0 ~ 1
            radius = h * 16.0   # 越往下越寬
            theta = y_step * 0.35 + angle

            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            y = h * 22.0

            # 3D 投影到 2D 螢幕
            screen_x = int(width / 2 + x * 1.6)
            screen_y = int(2 + y)

            if 0 <= screen_x < width and 0 <= screen_y < height:
                if z > zbuffer[screen_y][screen_x]:
                    zbuffer[screen_y][screen_x] = z
                    # 根據前後景深與位置決定符號（燈泡或樹葉）
                    if y_step % 11 == 0:
                        buffer[screen_y][screen_x] = '●'  # 裝飾燈球
                    elif z > 0:
                        buffer[screen_y][screen_x] = '*'  # 亮面樹葉
                    else:
                        buffer[screen_y][screen_x] = '.'  # 暗面樹葉

        # 畫樹幹
        for ty in range(24, 27):
            for tx in range(int(width/2) - 2, int(width/2) + 3):
                buffer[ty][tx] = '#'

        # 清空終端機並印出畫面
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n'.join(''.join(row) for row in buffer))
        
        angle += 0.12
        time.sleep(0.06)

if __name__ == '__main__':
    try:
        render_tree()
    except KeyboardInterrupt:
        print("\n動畫已停止！")
