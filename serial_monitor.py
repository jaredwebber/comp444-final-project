from serial import Serial
from time import sleep
from enum import Enum


# matches Direction enum in ArduinoController
class Signal(Enum):
    READY = "1"
    CLOCKWISE = "2"
    COUNTER_CLOCKWISE = "3"


class SerialController:
    def __init__(self):
        # Raspi: /dev/ttyUSB0
        # Mac: /dev/tty.usbserial-10
        self.ser = Serial("/dev/ttyUSB0", 9600, timeout=7)
        # allow time for serial connection to be established
        # in case get_room_data called immediately following __init__
        sleep(1)

    def _signal_ready(self):
        sleep(1)
        self.ser.write(Signal.READY.value.encode())
        sleep(5)

    def get_room_data(self, direction: Signal) -> list[float]:
        self._signal_ready()
        self.ser.write(direction.value.encode())
        vals = []

        for _ in range(722):
            raw = self.ser.readline()
            try:
                val = float(raw.decode().rstrip())
                vals.append(val)
            except ValueError as e:
                print(e)

        return vals
