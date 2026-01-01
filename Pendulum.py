import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# for single pendulum with non-small angle: F(tangential) = ma 
# -mgsinθ - cω = mrα, where r = L
# d2θ/dt2 + dθ/dt + gsinθ/L = 0


############################### Numerical Computation ###############################


# ode derived from first principles
ode = lambda theta, omega: -g*np.sin(theta)/L - c*omega

# parameters
dt = 0.01           # time step
g = 9.81            # gravitational acceleration
L = 1               # bar length
c = 0.2             # damping constant
n_iter = 2000       # iterations

# initial conditions
theta = np.pi / 2 * 1.95
omega = 0
alpha = ode(theta, omega)

# data storage
theta_lst = [theta]
omega_lst = [omega]
alpha_lst = [alpha]

# semi implicit euler scheme (symplectic)
for i in range(n_iter):

    omega = omega + alpha*dt
    theta = theta + omega*dt
    alpha = ode(theta, omega)

    theta_lst.append(theta)
    omega_lst.append(omega)
    alpha_lst.append(alpha)


############################### Graphing and Animation ###############################


# set up figure and axis - 1 animation axis and 3 graphs for s(t) v(t) a(t)
graphs = [['dis'], 
          ['vel'], 
          ['acc']]
fig, axd = plt.subplot_mosaic([['ani', graphs]], figsize=(10, 5), constrained_layout=True)


# set axis labels 
axd['ani'].set_xlabel('x')
axd['ani'].set_ylabel('y')

axd['dis'].set_xlabel('t')
axd['dis'].set_ylabel('θ')

axd['vel'].set_xlabel('t')
axd['vel'].set_ylabel('ω')

axd['acc'].set_xlabel('t')
axd['acc'].set_ylabel('α')


# set up axis limits
axd['ani'].set_xlim(-1.5*L, 1.5*L)
axd['ani'].set_ylim(-1.5*L, 1.5*L)

axd['dis'].set_xlim(0, n_iter*dt)
axd['dis'].set_ylim(-1.1*max(np.abs(theta_lst)), 1.1*max(np.abs(theta_lst)))

axd['vel'].set_xlim(0, n_iter*dt)
axd['vel'].set_ylim(-1.1*max(np.abs(omega_lst)), 1.1*max(np.abs(omega_lst)))

axd['acc'].set_xlim(0, n_iter*dt)
axd['acc'].set_ylim(-1.1*max(np.abs(alpha_lst)), 1.1*max(np.abs(alpha_lst)))


# set up plot objects, each will have its data updated in each animation loop
dis, = axd['dis'].plot([],[])
vel, = axd['vel'].plot([],[])
acc, = axd['acc'].plot([],[])

theta_curr = theta_lst[0]
x, y = L*np.sin(theta_curr), -L*np.cos(theta_curr)
line, = axd['ani'].plot([0, x], [0, y], zorder=1)
mass = axd['ani'].add_patch(patches.Circle((x, y), radius=0.1*L, zorder=2))


# function to update the plot, fed into FuncAnimation
def update_ax(frame): 

    # note: n = current data index number to be plotted
    n = frame*k

    # set values for displacement / velocity / acceleration against time so far
    dis.set_data(np.linspace(0, n*dt, n+1), theta_lst[:n+1])
    vel.set_data(np.linspace(0, n*dt, n+1), omega_lst[:n+1])
    acc.set_data(np.linspace(0, n*dt, n+1), alpha_lst[:n+1])

    # set position of pendulum at this instant in time
    theta_curr = theta_lst[n]
    x, y = L*np.sin(theta_curr), -L*np.cos(theta_curr)
    line.set_data([0, x], [0, y])
    mass.set_center([x, y])

    # return all plot objects (artists)
    return [dis, vel, acc, line, mass]


# animate only every k number of datapoints to reduce cost of plotting
k = 10  

# create animation, without looping (repeat=False), animation will be a little slower than real time
animation = FuncAnimation(fig, func=update_ax, frames=n_iter//k, interval=dt*1000*k, blit=True, repeat=False)
plt.show()
