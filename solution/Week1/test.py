import numpy as np
import matplotlib.pyplot as plt

def f(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        return eval("1/x")

fx_name = r'$f(x)=\frac{1}{x}$'

x=np.linspace(-10,10,101)
y=f(x)
plt.plot(x, y, label=fx_name)
plt.legend(loc='upper left')
plt.show()