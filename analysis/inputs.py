from analysis.sensor import WindowSensor, FingerSensor, BedPressureSensor, SwitchSensor
from enum import IntEnum


# 센서 유형 및 고유 ID 정의
class SensorType(IntEnum):
    WINDOW: int = 1
    FINBED1: int = 2
    FINBED2: int = 3
    FINBED3: int = 4
    FINWIN: int = 5
    FINDESK1: int = 6
    FINDESK2: int = 7
    FINDESK3: int = 8
    FINSWITCH: int = 9
    BEDPRESS1: int = 10
    BEDPRESS2: int = 11
    BEDPRESS3: int = 12
    SWIDESK1: int = 13
    SWIDESK2: int = 14
    SWIDESK3: int = 15
    SWISWITCH: int = 16


# 센서 ID를 유형별로 분류한 리스트
window_inputs = [1]
finger_inputs = [2, 3, 4, 5, 6, 7, 8, 9]
bed_pressure_inputs = [10, 11, 12]
switch_inputs = [13, 14, 15, 16]

# 센서 ID 리스트를 기반으로 각 센서 객체 생성
window_sensors = [WindowSensor(inp) for inp in window_inputs]
finger_sensors = [FingerSensor(inp) for inp in finger_inputs]
bed_pressure_sensors = [BedPressureSensor(inp) for inp in bed_pressure_inputs]
switch_sensors = [SwitchSensor(inp) for inp in switch_inputs]

# 모든 센서 객체를 하나의 리스트로 결합
sensors = window_sensors + finger_sensors + bed_pressure_sensors + switch_sensors
