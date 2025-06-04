import random, copy
from utils.connect_db import users


def sgn(x):
    """부호 함수"""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


class Sensor:
    def __init__(self, sensor_id, def_input=[]):
        self.id = sensor_id
        self.def_input = def_input
        self.input = copy.deepcopy(def_input)
        self.prev_input = copy.deepcopy(def_input)
        self.ignore_sgn = False

    def update(self):
        """센서 값 업데이트"""
        self.prev_input = copy.deepcopy(self.input)
        self.input = self.inputs()

    def inputs(self):
        """센서 값 생성"""
        return self.def_input

    def get_sgn(self):
        return sgn(self.get_diff())

    def is_valid(self):
        """센서 값 유효성 검사"""
        return True

    def get_diff(self):
        """센서 값 차이 계산"""
        return 0


class BedPressureSensor(Sensor):
    def __init__(self, sensor_id):
        def_input = [[0, 0, 0] for _ in range(6)]
        super().__init__(sensor_id, def_input)

    def get_diff(self, absolute=False):
        diff = 0
        for i in range(len(self.input)):
            for j in range(len(self.input[i])):
                diff += (
                    abs(self.input[i][j] - self.prev_input[i][j])
                    if absolute
                    else self.input[i][j] - self.prev_input[i][j]
                )
        return diff

    def is_valid(self):
        return self.get_diff(True) > 7

    def inputs(self):
        return [[random.random() for _ in range(3)] for _ in range(6)]


class FingerSensor(Sensor):
    def __init__(self, sensor_id):
        def_input = 0
        super().__init__(sensor_id, def_input)
        self.ignore_sgn = True

    def get_diff(self):
        return self.input - self.prev_input

    def is_valid(self):
        return self.get_diff() != 0 and self.input != 0

    def inputs(self):
        user = list(users.aggregate([{"$sample": {"size": 1}}]))[0]
        return random.choice([0] * 20 + [int(user["email"][:5])])


class WindowSensor(Sensor):
    def __init__(self, sensor_id):
        def_input = 0
        super().__init__(sensor_id, def_input)

    def get_diff(self):
        return self.input - self.prev_input

    def is_valid(self):
        return self.get_diff() != 0

    def inputs(self):
        return random.choice([0] * 5 + [1])


class SwitchSensor(Sensor):
    def __init__(self, sensor_id):
        def_input = 0
        super().__init__(sensor_id, def_input)

    def get_diff(self):
        return self.input - self.prev_input

    def is_valid(self):
        return self.get_diff() != 0

    def inputs(self):
        return random.choice([0] * 4 + [1])
