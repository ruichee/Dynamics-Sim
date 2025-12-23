import numpy as np
import matplotlib.pyplot as plt

################ Lorenz Attractor ################

# constants
sigma = 10
rho = 28
beta = 8/3
dt = 0.005
steps = 10000

# 2 sets of initial conditions 
x1, x2 = 2, 2.001
y1, y2 = 1, 1
z1, z2 = 1, 1

# Lorenz system governing equations
dxdt = lambda x,y,z: sigma*(y-x)
dydt = lambda x,y,z: x*(rho-z)-y
dzdt = lambda x,y,z: x*y-beta*z

# path values
x1_lst, x2_lst = [x1], [x2]
y1_lst, y2_lst = [y1], [y2]
z1_lst, z2_lst = [z1], [z2]

# semi implicit euler
for n in range(steps):

    dx1 = dxdt(x1,y1,z1) * dt
    dy1 = dydt(x1,y1,z1) * dt
    dz1 = dzdt(x1,y1,z1) * dt
    x1 = x1 + dx1
    y1 = y1 + dy1
    z1 = z1 + dz1
    x1_lst.append(x1)
    y1_lst.append(y1)
    z1_lst.append(z1)

    dx2 = dxdt(x2,y2,z2) * dt
    dy2 = dydt(x2,y2,z2) * dt
    dz2 = dzdt(x2,y2,z2) * dt
    x2 = x2 + dx2
    y2 = y2 + dy2
    z2 = z2 + dz2
    x2_lst.append(x2)
    y2_lst.append(y2)
    z2_lst.append(z2)


# set plot style to dark, axis to alpha=0.3
plt.style.use('dark_background')
plt.rcParams["grid.color"] = (0.5, 0.5, 0.5, 0.3)

# define figure and axis
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# set axis background to transparent
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# plot values
ax.plot(x1_lst, y1_lst, z1_lst, lw=0.5, color="#51FFF9")
ax.plot(x2_lst, y2_lst, z2_lst, lw=0.5, color="#FFEE51")
plt.show()