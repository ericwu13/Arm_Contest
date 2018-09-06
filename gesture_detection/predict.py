

import torch
from torch.autograd import Variable

from options import MainOptions
from sensor import Sensor
from filter import Filter
from visualizer import SensorVisualizer
from models import createModel
from utils import convert
from speech import Speech
from classifier_dtw import Classifier

parser = MainOptions()
opt = parser.parse()
sensor = Sensor(opt.port)
filter = Filter(opt.n, opt.n)
visualizer = SensorVisualizer(repr = opt.repr)
speech = Speech()
classifier = Classifier()

model = createModel(opt)
model.setup(opt)
model.eval()



def main():
    target = []
    while True:
        data = sensor.read()
        data = filter.update(data)
        x = Variable(convert(torch.FloatTensor(data)))
        signal = model.predict(x)
        if signal:
            operate = classifier.predict(target)
            print(operate)
            if operate != 'None':
                speech(operate)
                target = []
        else:
            print("Stop")
            target = []
        #visualizer(data)
    
if(__name__ == '__main__'):
    main()
