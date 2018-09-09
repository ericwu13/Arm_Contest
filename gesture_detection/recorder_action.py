
import torch
from torch.autograd import Variable


from options import TrainOptions
from visualizer import SensorVisualizer
from sensor import Sensor
from filter import Filter
from recorder import Recorder
from utils import convert
from models import createModel

parser = TrainOptions()
opt = parser.parse()

i = raw_input("Enter to start")
sensor = Sensor(opt.n, opt.port, opt.freq)
filter = Filter(opt.n, opt.n)
visualizer = SensorVisualizer(repr = opt.repr)
recorder = Recorder(opt)

print("action: {}".format(opt.action))

model = createModel(opt)
model.setup(opt)
model.eval()

def main(i):
    #lastSignal = False
    moveCount = 0
    stopCount = 0
    while True:
        data = sensor.read()
        data = filter.update(data)
        x = Variable(convert(torch.FloatTensor(data), opt.n))
        signal = model.predict(x)
        recorder.label(data)
        recorder.dump_action_id(i)
        '''
        if signal:
            moveCount += 1
            print('move', moveCount)
            #recorder.label(data)
        else:
            stopCount += 1
            print('stop', stopCount)
            if lastSignal == True:
                recorder.dump_action()
        '''
        #lastSignal = signal
        #visualizer(data)
    
if(__name__ == '__main__'):
    main(i)
