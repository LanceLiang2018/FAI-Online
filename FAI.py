import random
import copy
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
import threading
import time
import requests
import json
# ●○•


# 算法部分
class FAI:
    def __init__(self, w: int, h: int, P1='●○•'):
        self.CODE_P1 = '●'
        self.CODE_P2 = '○'
        self.CODE_BLANK = '　'
        self.P1 = 1
        self.P2 = 2
        self.BLANK = 0
        # self.CODE_P1 = ' 1 '
        # self.CODE_P2 = ' 2 '
        # self.CODE_BLANK = ' 0 '
        # self.CODE_P1 = '●'
        # self.CODE_P2 = '○'
        # self.CODE_BLANK = '.'
        self.CODE = {0: self.CODE_BLANK, 1: self.CODE_P1, 2: self.CODE_P2}
        self.w = w
        self.h = h
        # 五子棋
        self.WIN_COUNT = 5

        # 奇怪的数组定义方式...Python的对象是直接拷贝使用的
        self.map = [[0 for i in range(w)] for i in range(h)]

        # 定义计算权值的时候用的

        self.weights = {
            self.P1: {
                " 1 ": 1,
                " 11 ": 2,
                " 111 ": 3,
                " 1111 ": 3,
                " 12": 0,
                " 112": 1,
                " 1112": 2,
                " 11112": 3,
            },
            self.P2: {
                " 2 ": 1,
                " 22 ": 2,
                " 222 ": 3,
                " 2222 ": 3,
                " 21": 0,
                " 221": 1,
                " 2221": 2,
                " 22221": 3,
            },
        }

    def __str__(self):
        res = self.CODE_BLANK * self.w + self.CODE_BLANK * 2 + '\n'
        for y in self.map:
            res = res + self.CODE_BLANK
            for x in y:
                res = res + self.CODE[x]
            res = res + self.CODE_BLANK + '\n'
        res = res + self.CODE_BLANK * self.w + self.CODE_BLANK * 2
        return res

    def get_char(self, x=0, y=0):
        try:
            res = self.CODE[self.map[y][x]]
        except KeyError as e:
            res = self.CODE[0]
            print('get_char ERR:', y, x)
            print(self.map)
        return res

    def put(self, x: int, y: int, val: int):
        if self.map[y][x] == self.P1 or self.map[y][x] == self.P2:
            return False
        self.map[y][x] = val
        return True

    # 检测哪位玩家赢了
    def win(self, player=0):
        if player == 0:
            if self.win(player=self.P1) is True:
                return self.P1
            if self.win(player=self.P2) is True:
                return self.P2
            # 没有分出胜负
            return 0

        # 检查横行
        for y in self.map:
            # 十分低效率的检查方式
            if player not in y:
                continue
            for i in range(len(y)):
                if y[i] == player:
                    check = y[i:i + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        # 检查列
        for i in range(self.w):
            x = []
            for y in self.map:
                x.append(y[i])
            # 十分低效率的检查方式*2
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        # 检查"\\"列，从左上角开始
        for i in range(self.w):
            x = []
            for yi in range(len(self.map)):
                if i + yi < self.w:
                    x.append(self.map[yi][i + yi])
            # 十分低效率的检查方式*3
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        # 检查"\\"列，从左上角开始（到左下角）
        for i in range(self.h):
            x = []
            for xi in range(self.w):
                if i + xi < self.h:
                    x.append(self.map[i][i + xi])
            # 十分低效率的检查方式*4
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        # 检查"//"列，从左上角开始
        for i in range(self.w):
            x = []
            for yi in range(len(self.map)):
                if 0 <= i - yi < self.w:
                    x.append(self.map[yi][i - yi])
            # 十分低效率的检查方式*5
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        # 检查"//"列，从左上角开始（到左下角）
        for i in range(self.h):
            x = []
            for xi in range(self.w):
                if 0 <= i - xi < self.h:
                    x.append(self.map[i][i - xi])
            # 十分低效率的检查方式*6
            if player not in x:
                continue
            for j in range(len(x)):
                if x[j] == player:
                    check = x[j:j + 5]
                    if self.BLANK not in check:
                        if player == self.P1 and self.P2 not in check and len(check) == 5:
                            return True
                        if player == self.P2 and self.P1 not in check and len(check) == 5:
                            return True

        return False

    def play(self, player: int):
        weights = [[0 for i in range(self.w)] for i in range(self.h)]
        maps = self.__str__().split('\n')

        # for iy in range(len(maps)):
        #     # 检查横向，从左到右
        #     y = maps[iy]
        #     for ix in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[ix:].startswith(k):
        #                 weights[iy - 1][ix + 1] = weights[iy - 1][ix + 1] + self.weights[player][k]
        #     # 检查横向，从右到左
        #     y = maps[iy][::-1]
        #     for ix in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[ix:].startswith(k):
        #                 weights[iy - 1][self.w - (ix + 2)] = weights[iy - 1][self.w - (ix + 2)] + self.weights[player][k]
        #
        # for ix in range(len(maps[0])):
        #     y = ''
        #     for iy in range(len(maps)):
        #         y = y + maps[iy][ix]
        #
        #     # 检查竖向，从上到下
        #     for iy in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[iy:].startswith(k):
        #                 weights[iy - 1][ix - 1] = weights[iy - 1][ix - 1] + self.weights[player][k]
        #
        #     y = y[::-1]
        #     # 检查竖向，从下到上
        #     for iy in range(len(y)):
        #         for k in self.weights[player]:
        #             if y[iy:].startswith(k):
        #                 weights[self.h - (iy - 0)][ix - 1] = weights[self.h - (iy - 0)][ix - 1] + self.weights[player][k]

        # \\斜向，从左上角到右上角
        for ix in range(len(maps[0])):
            y = ''
            for iy in range(len(maps)):
                if ix + iy < len(maps[0]):
                    y = y + maps[iy][ix + iy]

            # 检查\\向，从上到下
            for iy in range(len(y)):
                for k in self.weights[player]:
                    if y[iy:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[iy - 1][ix + iy - 1] = weights[iy - 1][ix + iy - 1] + self.weights[player][k]

            y = y[::-1]
            # 检查竖向，从下到上
            for iy in range(len(y)):
                for k in self.weights[player]:
                    if y[iy:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] = weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] \
                                                                            + self.weights[player][k]

        # \\斜向，从左上角到左下角
        for iy in range(len(maps)):
            y = ''
            for ix in range(len(maps[0])):
                if ix + iy < len(maps[0]):
                    y = y + maps[iy][ix + iy]

            # 检查\\向，从上到下
            for ix in range(len(y)):
                for k in self.weights[player]:
                    if y[ix:].startswith(k):
                        if ix + iy < len(maps[0]):
                            weights[iy - 1][ix + iy - 1] = weights[iy - 1][ix + iy - 1] + self.weights[player][k]

            # y = y[::-1]
            # # 检查竖向，从下到上
            # for iy in range(len(y)):
            #     for k in self.weights[player]:
            #         if y[iy:].startswith(k):
            #             if ix + iy < len(maps[0]):
            #                 weights[self.h - (iy - 0)][self.w - (ix + iy + 0)] = weights[self.h - (iy - 0)][
            #                                                                          self.w - (ix + iy + 0)] \
            #                                                                      + self.weights[player][k]

        for w in weights:
            print(w)


class FAINetwork:
    def __init__(self):
        self.API_MAIN = 'https://lance-go-online.herokuapp.com/'
        self.API1 = 'https://lance-go-online.herokuapp.com/play/'
        self.API2 = 'https://lance-go-online.herokuapp.com/playing/'

    def wakeup(self, timeout: float = 30):
        try:
            r = requests.get(self.API_MAIN, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            return False
        if r.status_code != 200:
            return False
        return True

    def get_data(self, code: str):
        r = requests.get(self.API2 + code)
        if r.status_code != 200:
            return ''
        return r.text

    def get_result(self, code: str):
        r = requests.get(self.API2 + code)
        if r.status_code != 200:
            return {"code": code, "data": "", "error": "Server Error", "status": 0, "uptime": 0, "winner": 0}
        try:
            js = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            return {"code": code, "data": "", "error": "Server Error", "status": 0, "uptime": 0, "winner": 0}
        return js

    def post_result(self, code: str, player: int, action: str = 'put', winner: int = 0, size: str = None):
        params = {'action': action, 'player': player, 'winner': winner}
        if size is not None:
            params['size'] = size
        r = requests.post(self.API1 + code, data=params)
        if r.status_code != 200:
            return {'code': -1, 'message': "Server Error."}
        try:
            js = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            return {"code": code, "data": "", "error": "Server Error", "status": 0, "uptime": 0, "winner": 0}
        return js


# UI部分
class FaiUi:
    def __init__(self, _root, w: int, h: int):
        self.fai = FAI(w, h)
        self.net = FAINetwork()

        self.root = _root
        self.root.resizable(width=False, height=False)
        self.root.attributes('-alpha', 0.9)
        self.root.title("FAI - 在线五子棋对战程序")

        self.w, self.h = w, h
        self.started = False
        self.stopped = False

        self.time_p1, self.time_p2 = 0, 0
        self.var_p1, self.var_p2 = StringVar(), StringVar()
        self.message = StringVar()

        self.player = 1

        self.song = tkFont.Font(family='宋体', size=12, weight=tkFont.BOLD)

        self.frame_p1 = Frame(self.root)
        # self.button = Button(self.root, text='新开一局', command=lambda: (self.root.destroy(), init_ui()))
        self.message.set("新开一局")
        self.button = Button(self.root, textvariable=self.message, command=lambda: self.init_data(w, h), relief='groove')
        self.frame_p2 = Frame(self.root)

        Label(self.frame_p1, text="P1").grid(row=0, column=0)
        Label(self.frame_p1, text="●", font=self.song).grid(row=0, column=1)
        Label(self.frame_p1, textvariable=self.var_p1).grid(row=1, columnspan=3)

        Label(self.frame_p2, text="P2").grid(row=0, column=0)
        Label(self.frame_p2, text="○", font=self.song).grid(row=0, column=1)
        Label(self.frame_p2, textvariable=self.var_p2).grid(row=1, columnspan=3)

        self.frame = Frame(self.root)

        self.map = [[None for i in range(w)] for i in range(h)]
        self.click = [[None for i in range(w)] for i in range(h)]
        self.vars = [[StringVar() for i in range(w)] for i in range(h)]

        for y in range(h):
            for x in range(w):
                self.click[y][x] = FaiUiClick(self, fai=self.fai, w=w, h=h, x=x, y=y)

        for y in range(self.h):
            for x in range(self.w):
                self.vars[y][x].set(self.fai.get_char(x=x, y=y))

        self.refresh_time()

        for y in range(h):
            for x in range(w):
                self.map[y][x] = Button(self.frame,
                                        command=self.click[y][x].run,
                                        # text=self.fai.CODE[self.fai.map[y][x]])
                                        textvariable=self.vars[y][x],
                                        font=self.song,
                                        relief='groove',
                                        bd=1)
                self.map[y][x].grid(row=y, column=x)

        self.frame_p1.grid(row=0, column=0)
        self.button.grid(row=0, column=1)
        self.frame_p2.grid(row=0, column=2)
        self.frame.grid(row=1, columnspan=3)

        self.thread = None

    def init_data(self, w: int, h: int):
        self.w, self.h = w, h
        self.time_p1, self.time_p2 = 0, 0
        self.player = 1
        self.started = False
        self.stopped = False
        self.message.set("新开一局")

        self.fai = FAI(w, h)

        self.refresh_time()

        for i in self.map:
            for j in i:
                j.grid_forget()

        self.map = [[None for i in range(w)] for i in range(h)]
        self.click = [[None for i in range(w)] for i in range(h)]
        self.vars = [[StringVar() for i in range(w)] for i in range(h)]

        for y in range(h):
            for x in range(w):
                self.click[y][x] = FaiUiClick(self, fai=self.fai, w=w, h=h, x=x, y=y)

        for y in range(self.h):
            for x in range(self.w):
                self.vars[y][x].set(self.fai.get_char(x=x, y=y))

        for y in range(h):
            for x in range(w):
                self.map[y][x] = Button(self.frame,
                                        command=self.click[y][x].run,
                                        # text=self.fai.CODE[self.fai.map[y][x]])
                                        textvariable=self.vars[y][x],
                                        font=self.song,
                                        relief='groove',
                                        bd=1)
                self.map[y][x].grid(row=y, column=x)

        if self.thread is not None:
            self.started = False
            self.thread.join()
            self.thread = None

    def update_time(self):
        if self.player == 1:
            self.time_p1 = self.time_p1 + 0.25
        if self.player == 2:
            self.time_p2 = self.time_p2 + 0.25
        # 如果是整数才刷新
        if self.time_p1 - int(self.time_p1) == 0 or self.time_p2 - int(self.time_p2) == 0:
            self.refresh_time()

    def refresh_time(self):
        m, s = divmod(int(self.time_p1), 60)
        self.var_p1.set("%02d:%02d" % (m, s))
        m, s = divmod(int(self.time_p2), 60)
        self.var_p2.set("%02d:%02d" % (m, s))
        if self.player == 1:
            self.var_p1.set(self.var_p1.get() + " 执棋")
        if self.player == 2:
            self.var_p2.set(self.var_p2.get() + " 执棋")

    def update_loop(self):
        while True:
            time.sleep(0.25)
            if self.started is False:
                return
            self.update_time()

    def start(self):
        self.started = True
        # if self.thread is not None:
        #     self.thread.stop()
        self.update_time()
        self.thread = threading.Thread(target=self.update_loop)
        # 守护进程：主线程结束自己也结束
        self.thread.setDaemon(True)
        self.thread.start()

    def refresh(self):
        for y in range(self.h):
            for x in range(self.w):
                self.vars[y][x].set(self.fai.get_char(x=x, y=y))

        m, s = divmod(self.time_p1, 60)
        self.var_p1.set("%02d:%02d" % (m, s))
        m, s = divmod(self.time_p2, 60)
        self.var_p2.set("%02d:%02d" % (m, s))

        if self.player == 1:
            self.var_p1.set(self.var_p1.get() + " 执棋")
        if self.player == 2:
            self.var_p2.set(self.var_p2.get() + " 执棋")

# if __name__ == '__main__':
#     fai = FAI(8, 8)
#     # fai.put(0, 4, fai.P2)
#     # fai.put(0, 5, fai.P1)
#     # fai.put(0, 6, fai.P1)
#     # fai.put(0, 7, fai.P1)
#     # fai.put(0, 8, fai.P1)
#     #
#     # fai.put(1, 0, fai.P1)
#     # fai.put(2, 0, fai.P2)
#     # fai.put(3, 0, fai.P2)
#     # fai.put(4, 0, fai.P2)
#     # fai.put(5, 0, fai.P2)
#
#     # fai.put(6, 1, fai.P1)
#     # fai.put(5, 2, fai.P1)
#     # fai.put(4, 3, fai.P1)
#     # fai.put(3, 4, fai.P1)
#     # fai.put(2, 5, fai.P1)
#
#     # fai.put(2, 2, fai.P1)
#     # fai.put(2, 3, fai.P1)
#     # fai.put(2, 4, fai.P1)
#     # fai.put(2, 5, fai.P1)
#     # fai.put(2, 6, fai.P1)
#
#     fai.put(0, 1, fai.P1)
#
#     fai.play(fai.P1)
#     print(fai)
#     print("Player", fai.win(), 'is winner')


# 点击的函数专门设置一个类（浪费内存行为）
class FaiUiClick:
    def __init__(self, _ui: FaiUi, fai, x=0, y=0, w=0, h=0):
        self.ui = _ui
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.fai = fai

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def run(self):
        if self.ui.stopped is True:
            return
        print('clicked:', 'x:', self.x, 'y:', self.y, 'player:', self.ui.player)
        res = self.fai.put(self.x, self.y, self.ui.player)
        # self.fai.put(self.x, self.y, random.randint(0, 2))

        if res:
            if self.ui.player == 1:
                self.ui.player = 2
            elif self.ui.player == 2:
                self.ui.player = 1

        if self.ui.started is False:
            self.ui.start()

        self.ui.refresh()

        win = self.fai.win()
        if win != 0:
            self.ui.message.set("P%d获胜" % win)
            self.ui.stopped = True
            self.ui.started = False

#
# def ui_refresh():
#     global ui
#     for y in range(ui.h):
#         for x in range(ui.w):
#             ui.vars[y][x].set(ui.fai.get_char(x=x, y=y))
#
#     m, s = divmod(ui.time_p1, 60)
#     ui.var_p1.set("%02d:%02d" % (m, s))
#     m, s = divmod(ui.time_p2, 60)
#     ui.var_p2.set("%02d:%02d" % (m, s))
#
#     if ui.player == 1:
#         ui.var_p1.set(ui.var_p1.get() + " 执棋")
#     if ui.player == 2:
#         ui.var_p2.set(ui.var_p2.get() + " 执棋")


# def init_ui(w, h):
#     global ui
#     ui = FaiUi(Tk(), w, h)


class FAIConfig:
    def __init__(self, _root):
        self.root = _root
        self.root.resizable(width=False, height=False)
        self.frame = Frame(self.root)

        Label(self.frame, text="房间").grid(row=0, column=0)
        self.code = Entry(self.frame)
        self.code.grid(row=0, column=1, sticky=W+E)

        self.frame_wh = LabelFrame(self.frame, text='新房间')

        self.w = Entry(self.frame_wh, width=8)
        self.h = Entry(self.frame_wh, width=8)
        self.w.insert(0, "15")
        self.h.insert(0, "15")
        self.w.configure(state=DISABLED)
        self.h.configure(state=DISABLED)
        Label(self.frame_wh, text="宽度").grid(row=2, column=0)
        Label(self.frame_wh, text="高度").grid(row=2, column=2)
        self.w.grid(row=2, column=1)
        self.h.grid(row=2, column=3)

        self.frame_wh.grid(row=1, columnspan=3, sticky=W+E)

        self.var_check = BooleanVar()
        self.var_player = IntVar()
        self.var_player.set(1)

        Checkbutton(self.frame, text="建立新房间", variable=self.var_check,
                    command=self.check_fun)\
            .grid(row=2, columnspan=3)

        self.frame_player = LabelFrame(self.frame, text='玩家')
        Radiobutton(self.frame_player, value=1, variable=self.var_player, text='P1').grid(row=0, column=0)
        Radiobutton(self.frame_player, value=2, variable=self.var_player, text='P2').grid(row=0, column=1)
        Radiobutton(self.frame_player, value=0, variable=self.var_player, text='围观').grid(row=0, column=2)
        self.frame_player.grid(row=3, columnspan=3, sticky=W+E)

        self.var_message = StringVar()
        self.var_message.set('开始')

        Button(self.frame, textvariable=self.var_message, command=self.done)\
            .grid(row=40, columnspan=2, sticky=W + E)
        self.frame.grid()

        self.ui = None
        self.waiting = False

    def check_fun(self):
        if self.var_check.get() is True:
            self.w.configure(state=NORMAL)
            self.h.configure(state=NORMAL)
        else:
            self.w.configure(state=DISABLED)
            self.h.configure(state=DISABLED)

    def run_thread(self):
        net = FAINetwork()
        self.var_message.set('等待服务器响应...')
        res = net.wakeup(timeout=30)
        if res is False:
            self.var_message.set("网络错误/服务器响应错误")
            tkinter.messagebox.showerror("网络错误", "服务器响应错误")
            return
        self.var_message.set('服务器响应...OK')
        w, h = int(self.w.get()), int(self.h.get())
        self.frame.destroy()
        self.ui = FaiUi(self.root, w, h)
        # 不需要mainloop
        # self.ui.root.mainloop()
        self.waiting = False

    def done(self):
        if self.waiting is True:
            return
        print('done', self.var_check.get(), self.var_player.get(), self.w.get(), self.h.get())
        if self.code.get() == '':
            tkinter.messagebox.showerror("房间错误", "房间名为空")
            return

        self.waiting = True
        t = threading.Thread(target=self.run_thread)
        t.start()


if __name__ == '__main__':
    # init_ui(12, 12)
    # ui.root.mainloop()
    config = FAIConfig(Tk())
    config.root.mainloop()
