# module imports
import matplotlib.pyplot as plt
import numpy as np
import random

xmax = 15 * 60
xstep = 1
hit_prob = [0.1]
dmg_prob = [0.6, 0.8, 1.0]

x = np.arange(0.0, xmax, xstep)
y = np.full((xmax), 3, dtype=int)

t = 0
lastx = 0
while t < xmax:
    if t > lastx + 4:
        roll_hit = random.random()
        hit = hit_prob[0] > roll_hit
        if hit:
            roll_dmg = random.random()
            dmg = 1
            if roll_dmg < dmg_prob[0]:
                dmg = 1
            elif roll_dmg < dmg_prob[1]:
                dmg = 2
            elif roll_dmg < dmg_prob[2]:
                dmg = 3
            else:
                dmg = 1

            lastx = t
            y[t:t+4] = -3
            y[t+4:t+8] = -2

    t = t + xstep

fig, (ax) = plt.subplots(1, 1, sharex=True)
plt.ylim(-5, 5)
plt.xticks(np.arange(0, xmax+1, 30, dtype=int))
ax.plot(x, y, color='black')
ax.fill_between(x, y, where=y > 0, facecolor='green', interpolate=True)
ax.fill_between(x, y, where=y < 0, facecolor='red', interpolate=True)

subplots = []
fig2, subplots = plt.subplots(1, 4)

for i in range(0, 4, 1):
    # window size
    ws = 100
    slice_start = (i)*ws
    slice_end = (i+1)*ws

    sliced_x = x[slice_start:slice_end]
    sliced_y = y[slice_start:slice_end]

    subplots[i].plot(sliced_x, sliced_y, color='black')
    subplots[i].fill_between(sliced_x, sliced_y, where=sliced_y >
                             0, facecolor='green', interpolate=True)
    subplots[i].fill_between(sliced_x, sliced_y, where=sliced_y <
                             0, facecolor='red', interpolate=True)

    plt.ylim(-5, 5)
    plt.xticks(np.arange(slice_start, slice_end, 8), rotation='vertical')
    plt.grid(b=True, which='major', axis='x')

plt.show()
