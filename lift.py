import time
from random import Random
from threading import Timer
from threading import Thread

FLOOR_NUMBER = 22
LIFT_NUMBER = 6
UP_INTENT = 1
DOWN_INTENT = 2
NO_INTENT = 3

def test_lift_system():
    lift_sys = LiftSys(FLOOR_NUMBER, LIFT_NUMBER)

    floors = [Random.randint(0,FLOOR_NUMBER), range(30)]
    for rand_floor in floors:
        lift_sys.up_req(rand_floor)
        lift_sys.down_req(rand_floor)

def test_lift():
    lift = Lift(FLOOR_NUMBER)

    floors = [Random.randint(0,FLOOR_NUMBER), range(30)]
    for rand_floor in floors:
        lift.add_dest(rand_floor)
        lift.status()

def test_liftdoor():
    print("Test lift door")
    door = LiftDoor()
    while True:
        instr = input()

        if instr == 'q':
            return
        elif instr == 'o':
            door.open()
        elif instr == 'c':
            door.close()
        door.printstatus()

class LiftReq(object):
    def __init__(self, destfloor, direct_intent):
        self.dest = destfloor
        self.intent = direct_intent
        self.lift_assigned = None

class LiftDoor(object):

    """status:0-10, 0-closed, 10-opened
    """
    OPENING = 1
    CLOSING = 0
    OPENED = 10
    CLOSED = 0
    def __init__(self):
        self.status = 0
        self.action = LiftDoor.CLOSING
        self._timer = None

    def _start_timer(self, time = 0.5):
        if self._timer:
            self._timer.cancel()
        self._timer = Timer(time, self._process)
        self._timer.start()

    def _process(self):
        if self.action == LiftDoor.OPENING:
            if self.status<LiftDoor.OPENED:
                self.status += 1
                self._start_timer()
            else:  # close the door 2 secs after door opened
                self.action = LiftDoor.CLOSING
                self._start_timer(2)

        else:
            if self.status>LiftDoor.CLOSED:
                self.status -= 1
                self._start_timer()

    def open(self):
        self.action = LiftDoor.OPENING
        self._start_timer()

    def close(self):
        self.action = LiftDoor.CLOSING
        self._start_timer()
    def is_closed(self):
        return self.status == LiftDoor.CLOSED and self.action == LiftDoor.CLOSING

    def printstatus(self):
        print("status = %d" % self.status)

class Lift(Thread):
    """1.passenger in the lift can choose any floor to go
       2. passenger can send open/close  request when lift is at stop state
       3. """
    STOP = 0
    MOVE = 1


    def __init__(self, floor_number):
        Thread.__init__(self)
        self._total_floor = floor_number
        self._state = Lift.STOP
        self._cur_floor = 1
        self._door = LiftDoor()
        self._next = []
        self._intent = NO_INTENT

    def get_door_status(self):
        return self._door.status

    def get_cur_floor(self):
        return self._cur_floor

    def get_floor_count(self):
        return self._total_floor

    def subscribe_arrive(self, fn):
        self._arrive_callback = fn

    def add_inside_req(self, floor_num):
        if floor_num > self._cur_floor and self._intent != DOWN_INTENT :
            self._next.append((floor_num, NO_INTENT))
            self._intent = UP_INTENT
        elif floor_num < self._cur_floor and self._intent != UP_INTENT:
            self._next.append((floor_num, NO_INTENT))
            self._intent = DOWN_INTENT
            #ignore floor_num == self._cur_floor

    def add_outside_req(self, floor_num, intent):
        ret = True
        if self._state == Lift.STOP and self._cur_floor == floor_num and (self._intent == intent or self._intent == NO_INTENT):
            self.open_door()
            self._intent = intent
        elif self._intent == UP_INTENT and self._cur_floor < floor_num and intent == UP_INTENT:
            self._next.append((floor_num, intent))
            self._next.sort(key=lambda x: x[0])
        elif self._intent == DOWN_INTENT and self._cur_floor > floor_num and intent == DOWN_INTENT:
            self._next.append((floor_num, intent))
            self._next.sort(key=lambda x: x[0], reverse=True)
        else:
            ret = False
        return ret

    def response_to_req(self, floor_num, intent):
        ret = -1
        if self._state == Lift.STOP and self._cur_floor == floor_num and (self._intent == intent or self._intent == NO_INTENT):
            ret = 0
        elif self._intent == UP_INTENT and self._cur_floor < floor_num and intent == UP_INTENT:
            ret = floor_num - self._cur_floor
        elif self._intent == DOWN_INTENT and self._cur_floor > floor_num and intent == DOWN_INTENT:
            ret = self._cur_floor - floor_num

        return ret

    def close_door(self):
        if self._state == Lift.MOVE:
            return
        self._door.close()

    def open_door(self):
        if self._state == Lift.MOVE:
            return
        self._door.open()

    def process_next(self):
        # print("in process_next, _next len = %d, _state=%d, _cur_floor = %d" % (len(self._next), self._state, self._cur_floor))
        if len(self._next) == 0:
            return

        if self._cur_floor == self._next[0][0]:
            if len(self._next) == 1:
                self._intent = self._next[0][1]
            self._next = self._next[1:]
            self._state = Lift.STOP
            self._arrive_callback(self._cur_floor)
            self.open_door()
        elif self._door.is_closed():
            self._state = Lift.MOVE
            self._cur_floor += 1 if self._intent == UP_INTENT else -1
            time.sleep(1)

    def run(self):
        while True:
            time.sleep(0.1)
            self.process_next()







class LiftSys(object):
    def __init__(self, totalfloor, liftnumber ):
        self._lifts = [Lift(totalfloor) for i in range(liftnumber)]
        self._req = [[None, None] for i in range(totalfloor)]


    def up_req(self, floor_num):
        lift_req = LiftReq(floor_num, UP_INTENT)
        if not self._is_lift_ready(lift_req):
            self._req[floor_num -1][0] = lift_req

    def down_req(self, floor_num):
        lift_req = LiftReq(floor_num, DOWN_INTENT)
        if not self._is_lift_ready(lift_req):
            self._req[floor_num -1][1] = lift_req

    def _is_lift_ready(self, lift_req):
        for lift in self._lifts:
            if lift.is_ready_for(lift_req): return True
        return False

    def run(self):
        pass


def main():
    test_liftdoor()

if __name__ == '__main__':
    main()
