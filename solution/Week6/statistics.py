from math import e, factorial, exp, sqrt
from random import random, uniform, randint
import numpy as np

class Statistics():
    def __init__(self):
        self.iteration = 500000
        self.event = 0
        self.mean = 0
        self.variance = 0
        self.standardDeviation = 0

    def random(self, lam):
        return 0

    def pmf(self, lam, k):
        return 0

    def getSample(self, lam):
        return [self.random(lam) for i in range(self.iteration)]

class Poisson(Statistics):
    def __init__(self):
        self.sequence = 20
        return super(Poisson, self).__init__()

    def random(self, lam):
        count = 0
        _d = 1/self.sequence
        for x in range(lam*self.sequence):
            if(uniform(0, 1) < _d):
                count += 1
        return count

    def pmf(self, lam, k):
        if (k > 171):
            import decimal #Big number handler
        return ((lam**k)*(e**(-lam)))/factorial(k)

    def histogramPlot(self, lam, density=False):
        data = self.getSample(lam)
        _range = self.sequence*lam
        counts = [0 for i in range(_range)]

        self.mean = 0
        self.variance = 0

        for d in data:
            self.mean += d
            for i in range(1, _range+1):
                if(i == d):
                    counts[i-1] += 1
                    break

        his = [[], []] # x, y
        line = [[], []]
        self.mean /= self.iteration
        for i in range(_range):
            his[0].append(i+0.5)
            his[1].append(counts[i]/self.iteration)
            line[0].append(i)
            line[1].append(self.pmf(lam, i))
            self.variance += ((i+1 - self.mean)**2)*(counts[i]/self.iteration)

        return his, line

class Exponential(Statistics):
    def __init__(self):
        self.dataRange = 100
        return super(Exponential, self).__init__()

    def random(self, lam):
        return -np.log( uniform(0,1) ) / lam
    
    def pmf(self, lam, k):
        return lam * np.exp(-lam * k)
    
    def histogramPlot(self, lam, density=False):
        print(lam)
        data = self.getSample(lam)
        _range = self.dataRange
        _min = min(data)
        _max = max(data)
        _d = (_max - _min)/_range
        counts = [0 for i in range(_range)]

        self.mean = 0
        self.variance = 0

        for d in data:
            self.mean += d
            for i in range(1, _range+1):
                if(d <= (_d*i + _min)):
                    counts[i-1] += 1
                    break

        his = [[], []] # x, y
        line = [[], []]
        self.mean /= self.iteration
        for i in range(_range):
            his[0].append(_d*i+_min)
            his[1].append(counts[i]/(_d*self.iteration))
            line[0].append(i)
            line[1].append(self.pmf(lam, i))
            self.variance += ((_d*i+_min - self.mean)**2)*(counts[i]/self.iteration)

        return his, line

if __name__ == "__main__":
    # Test
    import matplotlib.pyplot as plt

    static = Exponential()
    static.iteration = 1000000
    _hist, _plot = static.histogramPlot(0.5)
    print(static.mean)
    print(static.variance)
    plt.bar(_hist[0], _hist[1])
    plt.plot(_plot[0], _plot[1], color="orange")
    plt.show()