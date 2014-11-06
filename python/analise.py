from scipy.fftpack import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
import numpy as np
import sys

y=np.loadtxt(sys.argv[1])
fisiologfile = open(sys.argv[1],'r')
freq = float(fisiologfile.readline().replace('\n', '').split('\t')[1])
# N"u"mero de sinais coletados
N = len(y)
# Espa"c"amento padr"a"o
T = 1.0 / freq
# Eixo X
x = np.linspace(0.0, N*T, N)
# Para teste
y = np.sin((2.0*np.pi*x))

# Transformadas
yf = fft(y)
xf = fftfreq(N, T)
xplot = fftshift(xf)
yplot = fftshift(yf)

# Plot
plt.subplot(211)
plt.plot(x, y)
plt.subplot(212)
plt.plot(xplot, (1.0/N) * np.abs(yplot))
plt.grid()
#plt.subplot(313)
#plt.plot(xf, 1.0/N * np.abs(yf))
#plt.grid()
plt.show()

