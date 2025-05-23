import numpy as np
import matplotlib.pyplot as plt

# Constants
N = 40
PI = np.pi
SamplingRate = 44100

# Generate the sinewave signal
phase = 0
step = 2 * PI / N
tbl = np.zeros(N)
x = np.zeros(N)
y = np.zeros(N)

for i in range(N):
    tbl[i] = np.sin(phase)
    phase += step

# Convert discrete indices to continuous time values
continuous_time_tbl = np.arange(N) / SamplingRate

# Create another array with every other sample and add 1 to the values
increment1 = (440/44100)*40
increment2 = (554/44100)*40
index1 = 0
index2 = 0
aux1 = 0
aux2 = 0
for i, _ in enumerate(tbl):
    x[i] = tbl[index1]
    y[i] = tbl[index2]
    aux1 += increment1
    aux2 += increment2
    index1 = round(aux1)
    index2 = round(aux2)
continuous_time_x = np.arange(0, N) / SamplingRate

# Plotting
plt.figure()
plt.step(continuous_time_tbl, tbl, 'r-',
         where='post', label='tbl[n]')  # red line
plt.step(continuous_time_x, x, 'b-', where='post', label='x[n]')  # blue line
plt.step(continuous_time_x, y, 'm-', where='post', label='y[n]')  # purple line

# Add red dots for tbl and blue dots for x
plt.plot(continuous_time_tbl, tbl, 'bo', marker=".")  # red dots
plt.plot(continuous_time_x, x, 'ro', marker=".")  # blue dots
plt.plot(continuous_time_x, y, 'mo', marker=".")  # purple dots

# Plot vertical lines at each point in tbl
for t, value in zip(continuous_time_tbl, tbl):
    plt.axvline(x=t, color='g', linestyle='-', linewidth=0.7)

plt.xlabel('Muestras (s)')
plt.ylabel('Amplitud')
plt.title(
    'tbl[n] vs x[n] [f0 = 440 Hz (Nota 69)] vs y[n] [f0 = 554 Hz (Nota 73)]')
plt.legend()
plt.show()
