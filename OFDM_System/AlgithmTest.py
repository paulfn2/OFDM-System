import numpy as np
from numpy import cos, sin, pi, ndarray, fft
import matplotlib.pyplot as plt

## Test Math behind komplex Bandpass / Baseband Signals

fsig = 1000
N = 1000
fa = 5e3
T = 1 / fa
n = np.arange(N)
x = cos(2 * pi * fsig * n * T)
x_h = sin(2 * pi * fsig * n * T)
x_analytic = []
# transform x to analytic signal with Single Band Spectrum

for i in range(N):
    x_analytic.append(complex(x[i], x_h[i]))

x_analytic_conj = np.flip(x_analytic)
x_analytic_conj = np.conj(x_analytic_conj)

y = list(x_analytic) + [0] + list(x_analytic_conj[:N-1])
print("LEN Y: ", len(y))
# Output Signal DMT Modulator
Y = fft.fftshift(fft.ifft(y))

Y_abs = abs(Y)
spectrum_axis = np.arange(-N / 2, N / 2)
print(len(spectrum_axis))
X = fft.fftshift(1 / N * fft.fft(x_analytic))
X_abs = abs(X)
x_new = N * fft.fftshift(fft.ifft(fft.fftshift(X)))


n = np.arange(1024)
fsig = 1e3
fa = 5e3

x_cos = np.cos(2*np.pi*fsig*n*1/fa)
x_cos_exp2 = x_cos*x_cos
X = fft.fftshift(1 / N * abs(fft.fft(x_cos)))
X2 = fft.fftshift(1 / N * abs(fft.fft(x_cos_exp2)))

plt.figure(1)
plt.plot(X)
plt.plot(X2)
#plt.figure(3)
#plt.plot(Y_abs)
plt.show()
