
import threading as td

from visualizer import Visualizer
from painter import Painter
from sensor import Sensor
from filter import Filter

sensor = Sensor("/dev/cu.usbmodem1413")
filter = Filter(9,9)
visualizer = Visualizer()
painter = Painter()

def main():
    while True:
        data = filter.update(sensor.read())
        visualizer(data)
        painter(data)

td.Thread(target=main).start()
painter.plot()
