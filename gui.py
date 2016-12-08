from time import *
from tkinter import *
from random import randint
from lift import *


class LiftSysV(Canvas):
    def __init__(self, parent, floor_count=6, lift_count=3):
        Canvas.__init__(self, parent, borderwidth=1)
        self._floor_count = floor_count
        self._lift_count = lift_count

        self._liftsys = LiftSys(floor_count, lift_count)
        up_down = UpDownBtn(self, floor_count, self._liftsys)

        up_down.pack()
        self.create_window(2, 10, window=up_down, anchor='nw')

        self._liftvs = []
        for i, lift in enumerate(self._liftsys._lifts):
            liftv = LiftV(self, lift)
            liftv.pack()
            self.create_window(50 + (LiftV.WIDTH + 2) * i, 10, window=liftv, anchor='nw')
            self._liftvs.append(liftv)

        self.configure(width=50 + (LiftV.WIDTH + 2) * 3, height=10 + LiftV.HEIGHT * floor_count)

        self._liftsys.run()

class UpDownBtn(Canvas):
    def __init__(self, parent, floor_count, liftsys):
        Canvas.__init__(self, parent, borderwidth=1)
        self._floor_count = floor_count
        self.configure(width=40, height=LiftV.HEIGHT * floor_count)

        pts_up = (0, 15, 8, 0, 16, 15)
        pts_down = (0, 0, 16, 0, 8, 15)

        add_offset = lambda x, offset: tuple(
            val + offset[0] if index % 2 == 0 else val + offset[1] for index, val in enumerate(x))
        pts_up = add_offset(pts_up, (2, LiftV.HEIGHT / 2))
        pts_down = add_offset(pts_down, (22, LiftV.HEIGHT / 2))
        self.up_downs = []
        self._liftsys = liftsys
        liftsys.subscribe_clear_req(self.clear_req)
        for i in range(floor_count):
            self.up_downs.append((self.create_polygon(pts_up, fill='green'),
                                  self.create_polygon(pts_down, fill='green')))
            pts_up = add_offset(pts_up, (0, LiftV.HEIGHT))
            pts_down = add_offset(pts_down, (0, LiftV.HEIGHT))

        self.bind("<Button-1>", self.click)

    def click(self, event):
        item = self.find_withtag(CURRENT)
        if item:
            floor_num = (self._floor_count * 2 - item[0]) // 2 + 1
            upordown = (self._floor_count * 2 - item[0]) % 2  # 0-down 1-up
            self._liftsys.move_req(floor_num, upordown)
            self.itemconfig(CURRENT, fill='red')

    def clear_req(self, floor_num, upordown):
        self.itemconfig((self._floor_count - floor_num + 1) * 2 - upordown, fill='green')


class LiftV(Canvas):
    WIDTH = 80
    HEIGHT = 50

    def __init__(self, parent, lift):
        Canvas.__init__(self, parent, borderwidth=1)

        self.lift = lift
        floor_count = lift.get_floor_count()
        self.configure(width=LiftV.WIDTH, height=LiftV.HEIGHT * floor_count)

        self.floor_text = []
        for i in range(floor_count):
            self.floor_text.append(
                self.create_text(5, (floor_count - i - 0.5) * LiftV.HEIGHT, text=str(i + 1), anchor='nw'))

        self._prev_floor = self.lift.get_cur_floor()
        shift_y = (floor_count - self.lift.get_cur_floor()) * LiftV.HEIGHT
        self.floor = self.create_rectangle(10, 10 + shift_y, LiftV.WIDTH, LiftV.HEIGHT + shift_y, fill='red')
        self.bind("<Button-1>", self.click)

        lift.subscribe_arrive(self.floor_arrive)
        lift.start()

        self.run()

    def floor_arrive(self, floor_num, intent):
        self.itemconfig(self.floor_text[floor_num - 1], fill='black')

    def click(self, event):
        item = self.find_withtag(CURRENT)
        if item and int(item[0] != self.lift.get_cur_floor()):
            if self.lift.add_inside_req(int(item[0])):
                self.itemconfig(CURRENT, fill="blue")
                self.update_idletasks()
                self.after(200)
                self.itemconfig(CURRENT, fill="red")

    def update(self):
        while True:
            shift_y = (self._prev_floor - self.lift.get_cur_floor()) * LiftV.HEIGHT
            self._prev_floor = self.lift.get_cur_floor()
            self.move(self.floor, 0, shift_y)

            color_g = color_r = self.lift.get_door_status() * 25
            color = "#%02x%02x%s" % (color_g, color_r, "ff")
            self.itemconfig(self.floor, fill=color)
            sleep(0.3)

    def run(self):
        Thread(target=self.update).start()

    def move_ball(self):
        deltax = randint(0, 10) - 5
        deltay = randint(0, 10) - 5
        self.move(self.ball, deltax, deltay)
        self.after(50, self.move_ball)


def testall():
    # initialize root Window and canvas
    root.title("Balls")
    root.resizable(False, False)
    canvas = Canvas(root, width=600, height=600)
    canvas.pack()

    liftsysv = LiftSysV(canvas, 8)
    liftsysv.pack()
    canvas.create_window(2, 10, window=liftsysv, anchor='nw')

    root.mainloop()


def win_deleted():
    print("1111")
    root.destroy()
    print("2222222")
    sys.exit()


root = Tk()
root.protocol("WM_DELETE_WINDOW", win_deleted)


def test_liftv():
    # initialize root Window and canvas
    root.title("test")
    root.resizable(False, False)
    liftv = LiftV(root, Lift(8))
    liftv.pack()

    root.mainloop()
    print("closing.................")
    sys.exit()


# test_liftv()
testall()
# create two ball objects and animate them
# ball1 = Ball(canvas, 10, 10, 30, 30)
# ball2 = Ball(canvas, 60, 60, 80, 80)
#
# ball1.move_ball()
# ball2.move_ball()
