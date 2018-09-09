

from options import RecorderOptions
from visualizer import SensorVisualizer, Painter
from sensor import Sensor
from filter import Filter
from recorder import Recorder

parser = RecorderOptions()
opt = parser.parse()

sensor = Sensor(opt.port, opt.freq)
sensor.flush()
filter = Filter(opt.n, opt.n)
visualizer = SensorVisualizer(repr = opt.repr)
painter = Painter(repr = opt.repr, display = opt.display, memorySize = opt.memorySize, ylim = opt.ylim )
recorder = Recorder(opt)

print("action: {}".format(opt.action))

def main():
    while True:
        data = sensor.read()
        data = filter.update(data)
        if recorder(data):
            exit()
        visualizer(data)
    
if(__name__ == '__main__'):
    raw_input('Waiting for start signal...')
    main()
