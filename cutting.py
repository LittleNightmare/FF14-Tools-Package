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
    new = [67.5, 11.25, 45, 22.5, 33.75, 56.5, 78.75]
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
    if status >= 0.9:
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
                    print('Down:\t' + str(white_line))
                    mouse.left()
                    break
            if red_line[0] < 200:
                if white_line in range(red_line[0] + bias + dely, red_line[1] - bias + dely + 1) and white_line < wp:
                    print('Up:\t' + str(white_line))
                    mouse.left()
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
        # 下面砍树进度条，一条线
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
        MOVE_AEX = 30
        rounds = 0
        while 1:

            if IF_START == 0: break
            # 砍树按钮
            mouse.move(480, 915)

            find_list = []
            green = find_green(get_screen_arry(CUT_TREE_LINE))
            current_degree = 0
            last_degree = 0
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
                    if status != 0: break
                pos_record.append(current_degree)
                pos_status.append(status)
            print('Green:\t' + str(green))
            count_not_success = 0
            adjust = MOVE_AEX
            for i in range(len(pos_status), 10):
                # green = find_green(get_screen_arry(CUT_TREE_LINE))
                print("回合：" + str(i))
                print("pos_record" + str(pos_record))
                print("pos_status" + str(pos_status))

                # 根据上一次的结果判定
                if IF_START == 0 or time.time() - START > 65 or pos_status[i - 1] == 3:
                    break
                elif pos_status[i - 1] == pos_status[i - 2] and pos_status[i - 1] != 0:
                    current_degree = (pos_record[i - 1] + pos_record[i - 2]) / 2
                elif pos_status[i - 1] != 0:
                    # 上一次不失败
                    if pos_record[i - 1] <= 45:
                        # 上一次位于下面
                        current_degree = pos_record[i - 1] + adjust / pos_status[i - 1]
                    else:
                        current_degree = pos_record[i - 1] - adjust / pos_status[i - 1]
                else:
                    for j in pos_status, pos_record:
                        if j[0] == max(pos_status):
                            current_degree = j[1]
                            break
                    current_degree = abs(current_degree - pos_record)

                axe(current_degree, dely, bias)
                pos_record.append(current_degree)
                time.sleep(3)
                green = find_green(get_screen_arry(CUT_TREE_LINE))
                if green <= 0.1: break
                pos_status.append(get_last_success_status(old_green, green))
                old_green = green
                adjust = abs(pos_record[i] - pos_record[i - 1])
                print("END " + str(i) + "Current Green: " + str(green) + "current_degree:" + str(current_degree))

            # 接下来开始第二次。。。。
            # while 1:
            #     status = get_last_success_status(old_green, green)
            #     if IF_START == 0: break
            #     if time.time() - START > 65: break
            #     if try_times >= 10: break
            #     if status == 3: break
            #     if status <= 2:
            #         # 有手感了，或连续两次大角度失败
            #         if status == 1 or count_not_success >= 2:
            #             count_not_success = 0
            #             if last_degree - move_aex >= 45:
            #                 current_degree = last_degree + move_aex / 2
            #                 # last_degree = current_degree
            #                 # count_not_success = 0
            #             else:
            #                 current_degree = current_degree - move_aex / 2
            #                 # last_degree = current_degree
            #                 # count_not_success = 0
            #         else:
            #             count_not_success += 1
            #             # 失败的情况
            #             if last_degree >= 45:
            #                 # 上一次在上面和中间
            #                 # 往下走
            #                 current_degree = last_degree + move_aex
            #             else:
            #                 current_degree = last_degree - move_aex
            #     else:
            #         move_aex = last_degree - current_degree
            #         count_not_success = 0
            #         current_degree = last_degree
            #     print("current_degree:{0}; last_degree:{1}; move_aex:{2}; old_green:{3}; green:{4}".
            #           format(current_degree,
            #                  last_degree,
            #                  move_aex,
            #                  old_green,
            #                  green))
            #     axe(current_degree, dely, bias)
            #     last_degree = current_degree
            #     print('Adjust Pos:\t' + str(current_degree))
            #     time.sleep(3)
            #     old_green = green
            #     green = find_green(get_screen_arry(CUT_TREE_LINE))
            #     try_times += 1
            print('Time:\t' + str(time.time() - START))
            print('Rounds:\t' + str(rounds + 1))
            if rounds >= 5: break
            if time.time() - START <= 45 or (time.time() - START > 45 and rounds < 2):
                if IF_START == 0: break
                time.sleep(2.35)
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
