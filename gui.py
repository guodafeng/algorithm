from time import *
from tkinter import *
from random import randint
from lift import *

class LiftSysV(Canvas):
    pass


class LiftV(Canvas):
    WIDTH = 80
    HEIGHT = 50

    def __init__(self, parent, lift=Lift(6)):
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

    def floor_arrive(self, floor_num):
        self.itemconfig(self.floor_text[floor_num - 1], fill='black')

    def click(self, event):
        item = self.find_withtag(CURRENT)
        if item and int(item[0] != self.lift.get_cur_floor()):
            self.itemconfig(CURRENT, fill="blue")
            self.update_idletasks()
            self.after(200)
            self.itemconfig(CURRENT, fill="red")
            self.lift.add_inside_req(int(item[0]))

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
    root = Tk()
    root.title("Balls")
    root.resizable(False, False)
    canvas = Canvas(root, width=600, height=600)
    canvas.pack()
    for in range(8):
        canvas.create_polygon()

    canvas.create_text(20, 20, text='Ham')  # draw some text

    for i in range(3):
        lift = Lift(8)
        liftv = LiftV(canvas, lift)
        liftv.pack()
        canvas.create_window(50 + (LiftV.WIDTH + 2) * i, 10, window=liftv, anchor='nw')

    root.mainloop()


def test_liftv():
    # initialize root Window and canvas
    root = Tk()
    root.title("test")
    root.resizable(False, False)
    liftv = LiftV(root, Lift(8))
    liftv.pack()
    root.mainloop()
    sys.exit()


#test_liftv()
testall()
# create two ball objects and animate them
# ball1 = Ball(canvas, 10, 10, 30, 30)
# ball2 = Ball(canvas, 60, 60, 80, 80)
#
# ball1.move_ball()
# ball2.move_ball()