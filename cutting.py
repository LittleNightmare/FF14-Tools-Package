# -*- coding: utf-8 -*-  

# import numpy as np
import math
import time

import sys

import lib.mouse as mouse
# import lib.key as key
from lib.catch import *
# from tkinter import *
from lib.listen_key import *
from lib.play_mp3 import play_mp3
from threading import Thread
import os


def transpose(array):
    array_T = np.zeros((len(array[0]), len(array))).tolist()
    for i in range(0, len(array)):
        for j in range(0, len(array[0])):
            array_T[j][i] = array[i][j]
    return array_T


def blue_pos(a_im):
    pos = [0] * 2
    for y in range(START_POINT[1], END_Y + 1):
        x = pow(pow(START_POINT[0] - SHAPE_CENTER[0], 2) + pow(START_POINT[1] - SHAPE_CENTER[1], 2) - pow(
            y - SHAPE_CENTER[1], 2), 0.5) + \
            SHAPE_CENTER[0]
        x = round(x)
        x = x - SHAPE_CROP[0]
        y = y - SHAPE_CROP[1]
        if a_im[x][y][0] < 100 and a_im[x][y][1] < 100 and a_im[x][y][2] > 100:
            pos[0] = x + SHAPE_CROP[0]
            pos[1] = y + SHAPE_CROP[1]
            return pos
    # print(str(x+CROP[0])+','+str(y++CROP[1])+' '+str(a_im[y][x]))
    return pos


def white_pos(a_im):
    pos = [0] * 2
    for y in range(START_POINT[1], END_Y + 1):
        x = pow(pow(START_POINT[0] - SHAPE_CENTER[0], 2) + pow(START_POINT[1] - SHAPE_CENTER[1], 2) - pow(
            y - SHAPE_CENTER[1], 2), 0.5) + \
            SHAPE_CENTER[0]
        x = round(x)
        x = x - SHAPE_CROP[0]
        y = y - SHAPE_CROP[1]
        if a_im[x][y][0] > 150 and a_im[x][y][1] > 150 and a_im[x][y][2] > 150:
            pos[0] = x + SHAPE_CROP[0]
            pos[1] = y + SHAPE_CROP[1]
            return pos
    return pos


# print(str(x)+','+str(y)+' '+str(a_im[y][x]))


def radian(c, o1, o2):
    arc = pow(pow(o1[0] - o2[0], 2) + pow(o1[1] - o2[1], 2), 0.5) / pow(pow(o1[0] - c[0], 2) + pow(o1[1], c[1], 2),
                                                                        0.5) / 2
    if arc > 1: arc = 1
    if arc < -1: arc = -1
    return math.degrees(math.asin(arc))


def pos_r(pos):
    if pos[0] == 0 and pos[1] == 0:
        return 0
    return radian(SHAPE_CENTER, START_POINT, pos)


def find_white(a_im):
    # loction(490,403,515,803)
    LINE = 10
    for i in range(len(a_im)):
        if int(a_im[i][LINE][0]) + int(a_im[i][LINE][1]) + int(a_im[i][LINE][2]) > 480:
            return i
    return 0


def find_red(a_im):
    # loction(490,403,515,803)
    LINE = 8  # 8
    red_line = []
    for i in range(len(a_im)):
        # if a_im[i][LINE][1]<80:
        if a_im[i][LINE][0] > 100 and a_im[i][LINE][2] < 80 and a_im[i][LINE][1] > 80:
            red_line.append(i)
    return [red_line[0], red_line[-1]]


def find_pos(old):
    new = [TOTAL_DEGREE * 6 / 8,
           TOTAL_DEGREE * 1 / 8,
           TOTAL_DEGREE * 4 / 8,
           TOTAL_DEGREE * 7 / 8,
           TOTAL_DEGREE * 2 / 8,
           TOTAL_DEGREE * 3 / 8,
           TOTAL_DEGREE * 6 / 8,
           0,
           TOTAL_DEGREE]
    # num = len(old)
    # if old:
    #     step = old[0] / 2
    #     for i in old:
    #         new.append(i - step)
    #         new.append(i + step)
    # else:
    #     new.append(TOTAL_DEGREE / 2)
    return new


def find_green(a_im):
    LINE = 0
    for i in range(len(a_im)):
        if a_im[i][LINE][1] < 100:
            return i / (len(a_im) - 1)
    return 1


def get_last_success_status(old, current):
    status = old - current
    print("Status:" + str(status))
    if status >= 0.90:
        # perfect 直接清空
        return 3
    elif status >= 0.15:
        # great 少40
        return 2
    elif status >= 0.05:
        # normal 少10
        return 1
    else:
        # fail
        return 0


def axe(i, dely, bias):
    DELY2 = 0.25  # 0.2
    rp = 0
    while 1:
        if IF_START == 0: break
        if time.time() - START > 65: break
        r = pos_r(white_pos(get_screen_arry(SHAPE_CROP)))
        if i >= TOTAL_DEGREE / 2 and r >= i - dely - bias and r <= i - dely + bias and r > rp:
            print('Down:\t' + str(r))
            mouse.left()
            return [r, 1]
        if i <= TOTAL_DEGREE / 2 and r >= i + dely * DELY2 - bias and r <= i + dely * DELY2 + bias and r < rp:
            print('Up:\t' + str(r))
            mouse.left()
            return [r, 2]
        rp = r


def start_cutting():
    global IF_START
    global START_POINT
    global SHAPE_CENTER
    global END_Y
    global TOTAL_DEGREE
    global SHAPE_CROP
    global START

    while 1:
        if IF_START == 0: break

        mouse.move(965, 380)
        mouse.left()
        time.sleep(0.05)
        mouse.right()
        time.sleep(1)
        # 砍树开始选择难度的条
        Difficult_Selection = [417, 497, 472, 900]

        try:
            red_line = find_red(transpose(get_screen_arry(Difficult_Selection)))
        except:
            continue
        if IF_START == 0: break
        # 是
        mouse.move(970, 580)
        mouse.left()
        time.sleep(0.05)
        # 选择难度按钮
        mouse.move(440, 910)
        time.sleep(2)

        wp = 0
        print(red_line)

        # dis_list=[]
        # for i in range(20):
        # 	if IF_START==0:break
        # 	dis=find_white(transpose(get_screen_arry(CROP0)))
        # 	dis=abs(find_white(transpose(get_screen_arry(CROP0)))-dis)
        # 	dis_list.append(dis)
        # dis=np.argmax(np.bincount(dis_list))

        dis = 13
        dely = int(round(dis * 4.75))
        bias = 6
        START = time.time()
        while 1:
            if IF_START == 0: break
            if time.time() - START > 10: break
            white_line = find_white(transpose(get_screen_arry(Difficult_Selection)))
            if red_line[0] >= 200:
                if white_line in range(red_line[0] + bias - dely, red_line[1] - bias - dely + 1) and white_line > wp:
                    mouse.left()
                    print('Down:\t' + str(white_line))
                    break
            if red_line[0] < 200:
                if white_line in range(red_line[0] + bias + dely, red_line[1] - bias + dely + 1) and white_line < wp:
                    mouse.left()
                    print('Up:\t' + str(white_line))
                    break
            wp = white_line
        if time.time() - START > 10:
            mouse.move(1010, 625)
            mouse.left()
            time.sleep(1.6)
            continue

        if IF_START == 0: break
        # CROP = [520, 520, 605, 825]
        # CENTER = [396, 676]
        # START_POINT = [536, 532]
        # END_Y = 813
        # 转盘，两个扇形端点
        SHAPE_CROP = [545, 545, 625, 850]
        # 这个扇形的顶点
        SHAPE_CENTER = [421, 701]
        # ？滑块开始
        START_POINT = [561, 557]
        # ？滑块结束
        END_Y = 838
        END_X = round(
            pow(pow(START_POINT[0] - SHAPE_CENTER[0], 2) + pow(START_POINT[1] - SHAPE_CENTER[1], 2) - pow(
                END_Y - SHAPE_CENTER[1], 2),
                0.5) + SHAPE_CENTER[0])
        TOTAL_DEGREE = pos_r([END_X, END_Y])
        # 下面砍树进度条，一条线, 似乎可以完全等于绿色
        CUT_TREE_LINE = [337, 879, 661, 880]
        time.sleep(3)
        START = time.time()
        dis_list = []

        # for i in range (10):
        # 	if IF_START==0:break
        # 	dis=pos_r(white_pos(get_screen_arry(CROP)))
        # 	dis=abs(pos_r(white_pos(get_screen_arry(CROP)))-dis)
        # 	if dis!=0:dis_list.append(dis)
        # dis=np.median(dis_list)
        dis = 6.2
        print('Speed:\t' + str(dis))
        dely = 5 * dis  # 4.5
        bias = 3  # 3
        # MOVE_AEX = 30
        rounds = 0
        while 1:

            if IF_START == 0: break
            # 砍树按钮
            mouse.move(480, 915)

            find_list = []
            green = find_green(get_screen_arry(CUT_TREE_LINE))
            current_degree = 0
            old_green = green
            pos_record = []
            pos_status = []

            # 砍树开始
            status = 0
            while status == 0:
                # 砍第一次，直到砍成功一次
                old_green = green
                if IF_START == 0: break
                if time.time() - START > 65: break
                find_list = find_pos(find_list)

                for current_degree in find_list:
                    if IF_START == 0: break
                    print('Current Pos:\t' + str(current_degree))
                    axe(current_degree, dely, bias)
                    time.sleep(3)
                    green = find_green(get_screen_arry(CUT_TREE_LINE))
                    status = get_last_success_status(old_green, green)
                    pos_record.append(current_degree)
                    pos_status.append(status)
                    if status != 0: break
            print('Green:\t' + str(green))

            for i in range(len(pos_status), 10):
                # green = find_green(get_screen_arry(CUT_TREE_LINE))
                print("回合：" + str(i))
                print("pos_record" + str(pos_record))
                print("pos_status" + str(pos_status))
                strategy = "未选择策略"
                # 根据上一次的结果判定
                if IF_START == 0 or time.time() - START > 65 or pos_status[i - 1] == 3 or green <= 0.05:
                    print("END\n")
                    break
                elif pos_status[i - 1] == 2:
                    strategy = "保持原来角度"
                    current_degree = pos_record[i - 1]
                elif pos_status[i - 1] == 1:
                    normal_adjust = TOTAL_DEGREE / 8
                    if pos_record[i - 1] <= TOTAL_DEGREE / 4:
                        strategy = "向下移动"+str(normal_adjust)
                        current_degree = pos_record[i - 1] + normal_adjust
                    elif pos_record[i - 1] <= TOTAL_DEGREE / 2:
                        strategy = "向上移动" + str(normal_adjust)
                        current_degree = pos_record[i - 1] - normal_adjust
                    elif pos_record[i - 1] <= TOTAL_DEGREE * 3 / 4:
                        strategy = "向下移动" + str(normal_adjust)
                        current_degree = pos_record[i - 1] + normal_adjust
                    else:
                        strategy = "向上移动" + str(normal_adjust)
                        current_degree = pos_record[i - 1] - normal_adjust

                    if len(pos_status) >= 3:
                        if pos_status[i - 1] == pos_status[i - 3] and pos_record[i - 1] == pos_record[i - 3]:
                            if pos_record[i - 1] <= TOTAL_DEGREE / 4:
                                # 反转，策略出现问题
                                strategy = "向上移动" + str(normal_adjust)
                                current_degree = pos_record[i - 1] - normal_adjust
                            elif pos_record[i - 1] <= TOTAL_DEGREE / 2:
                                strategy = "向下移动" + str(normal_adjust)
                                current_degree = pos_record[i - 1] + normal_adjust
                            elif pos_record[i - 1] <= TOTAL_DEGREE * 3 / 4:
                                strategy = "向上移动" + str(normal_adjust)
                                current_degree = pos_record[i - 1] - normal_adjust
                            else:
                                strategy = "向下移动" + str(normal_adjust)
                                current_degree = pos_record[i - 1] + normal_adjust
                else:
                    stable = True
                    if max(pos_status) == 2:
                        best_records = []
                        lower_records = []
                        for history_index in range(len(pos_status)):
                            if pos_status[history_index] == max(pos_status):
                                best_records.append(pos_record[history_index])
                            if pos_status[history_index] < max(pos_status):
                                lower_records.append(pos_status[history_index])

                        if min(best_records) == max(best_records):
                            for low_record in lower_records:
                                if low_record in best_records:
                                    stable = False
                                    break
                                current_degree = best_records[0]
                                strategy = "选择最佳历史" + str(current_degree)
                        else:
                            print("记录出现波动，更换策略")
                            stable = False

                    if max(pos_status) != 2 or not stable:
                        strategy = "移动方向错误，从" + str(pos_record[i - 2])+"到" + str(pos_record[i - 1]) + ", "
                        change_pos = pos_record[i - 1] - pos_record[i - 2]
                        if change_pos >= 0:
                            strategy += "向上移动"+str(abs(change_pos))
                            current_degree = pos_record[i - 2] - abs(change_pos)
                        else:
                            strategy += "向下移动" + str(abs(change_pos))
                            current_degree = pos_record[i - 2] + abs(change_pos)
                # 防止超出上线
                if current_degree < 0:
                    current_degree = 0
                elif current_degree > TOTAL_DEGREE:
                    current_degree = TOTAL_DEGREE

                axe(current_degree, dely, bias)
                print(strategy)
                pos_record.append(current_degree)
                time.sleep(3)
                green = find_green(get_screen_arry(CUT_TREE_LINE))
                pos_status.append(get_last_success_status(old_green, green))
                old_green = green
                print(
                    "END " + str(i) + ";Current Green: " + str(green) + ";current_degree:" + str(current_degree) + "\n")
            # 一回合结束了，开始决定是继续还是放弃
            print('Time:\t' + str(time.time() - START))
            print('Rounds:\t' + str(rounds + 1))
            if rounds >= 5: break
            if time.time() - START <= 45 or (time.time() - START > 45 and rounds < 2):
                if IF_START == 0: break
                time.sleep(2.35)
                if len(pos_record) >= 10:
                    break
                # 继续游戏的是
                mouse.move(906, 630)
                mouse.left()
                time.sleep(0.25)
                START += 5
                rounds += 1
            else:
                if IF_START == 0: break
                time.sleep(2.2)
                # 继续游戏的否
                mouse.move(1015, 630)
                mouse.left()
                time.sleep(1.6)
                break


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        relative_path = 'lib/' + relative_path
    return os.path.join(base_path, relative_path)


def on_press(key):
    global IF_START
    try:
        if key._name_ == 'f12':
            return False

        if key._name_ == 'caps_lock' and IF_START == 0:
            play_mp3(resource_path('start.mp3'))
            print('START CUTTING')
            IF_START = 1
            Thread(target=start_cutting).start()
        elif key._name_ == 'caps_lock':
            play_mp3(resource_path('end.mp3'))
            IF_START = 0
            time.sleep(4)
            print('END CUTTING')
    except:
        pass


print('Press Caps to Start...')
IF_START = 0
start_listen(on_press)
