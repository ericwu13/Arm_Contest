
import os.path
import numpy as np

class Recorder():
    def __init__(self, opt):
        self.X = []
        self.Y = []
        self.opt = opt
        self.counter = 0

    def __call__(self, data):
        self.labeling(data)
        # handle dumping data
        self.counter +=1
        if self.counter % self.opt.recordInterval == 0:
            self.dump_data()
            return True
        else:
            return False

    def labeling(self, data):
        if self.opt.action == 'stop':
            self.X.append(data)
            self.Y.append(0)
        elif self.opt.action == 'move':
            self.X.append(data)
            self.Y.append(1)

    def dump_data(self):
        index = 0
        path = os.path.join(self.opt.splitDir, '{}.npy'.format(index))
        while os.path.exists(path):
            path = os.path.join(self.opt.splitDir, '{}.npy'.format(index))
            index += 1
        np.save(path, np.array([self.X, self.Y]))
        self.X = []
        self.Y = []
        print('saved data to {}...'.format(path))
        raw_input()
