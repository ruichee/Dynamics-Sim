import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# UWaterlooME 362 Fluid Mechanics 2 - Project 2 (Fall 2025)
# Fluid Mechanics of Sports - Modelling of Frisbee Trajectory 

# constants
rho = 1.2
d = 0.274
b = 0.032
m = 0.175
g = 9.81
A = np.pi * d**2 / 4
dt = 0.01

# initial conditions
x0 = 0
y0 = 0
z0 = 1
vx0 = 14
vy0 = 0
vz0 = 0

# stored iteration results
x_lst = [[x0] for _ in range(5)]
y_lst = [[y0] for _ in range(5)]
z_lst = [[z0] for _ in range(5)]

# iteration
k = -1
for bank in [5, 10, 12, 15, 20]: 
    
    trim_rad = 10 / 180 * np.pi
    x_prev = x0
    y_prev = y0
    z_prev = z0
    vx_prev = vx0
    vy_prev = vy0
    vz_prev = vz0
    omega = 5*2*np.pi
    bank = bank*np.pi/180
    k += 1

    # forward euler scheme - appropriate due to small time scale
    while z_prev > 0:

        flight_angle = np.arctan(vz_prev/vx_prev)
        alpha = trim_rad - flight_angle
        C_L = 0.188 + 2.37*alpha
        C_D = 0.15 + 1.24*alpha*alpha
        U = np.sqrt(vx_prev*vx_prev + vz_prev*vz_prev)
        D = 1/2*C_D*rho*A*U*U
        L = 1/2*C_L*rho*A*U*U 

        Dx = vx_prev/U * D
        Dy = vy_prev/U * D
        Dz = vz_prev/U * D
        Lx = -L*np.cos(bank)*np.sin(flight_angle)
        Ly = -L*np.sin(bank)
        Lz = L*np.cos(bank)*np.cos(flight_angle)

        ax = (-Dx + Lx) / m
        ay = (-Dy + Ly) / m
        az = (-Dz + Lz) / m - g

        vx_curr = vx_prev + ax*dt
        vy_curr = vy_prev + ay*dt
        vz_curr = vz_prev + az*dt
        x_curr = x_prev + vx_prev*dt
        y_curr = y_prev + vy_prev*dt
        z_curr = z_prev + vz_prev*dt

        x_lst[k].append(x_curr)
        y_lst[k].append(y_curr)
        z_lst[k].append(z_curr)

        vx_prev = vx_curr
        vy_prev = vy_curr
        vz_prev = vz_curr
        x_prev = x_curr
        y_prev = y_curr
        z_prev = z_curr

# 3D trajectory plots
ax = plt.figure().add_subplot(projection='3d')
for i in range(5):
    ax.plot(x_lst[i], y_lst[i], z_lst[i])

ax.legend(['5', '10', '12', '15', '20'])
plt.show()

# 3D animation plots - create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Set up the plot limits (adjust based on your data range)
ax.set_xlim(0, max([max(x) for x in x_lst]))
ax.set_ylim(min([min(y) for y in y_lst]), max([max(y) for y in y_lst]))
ax.set_zlim(0, max([max(z) for z in z_lst]))
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
ax.set_title('Aircraft Flight Trajectories')

# Initialize line objects for each bank angle
lines = []
bank_angles = [5, 10, 12, 15, 20]
colors = ['blue', 'green', 'red', 'cyan', 'magenta']

for i, (bank, color) in enumerate(zip(bank_angles, colors)):
    line, = ax.plot([], [], [], lw=2, label=f'Bank {bank}°', color=color)
    lines.append(line)

ax.legend()

def animate(frame):
    for i, line in enumerate(lines):
        # Show trajectory up to current frame
        end_idx = min(frame, len(x_lst[i]))
        line.set_data(x_lst[i][:end_idx], y_lst[i][:end_idx])
        line.set_3d_properties(z_lst[i][:end_idx])
    return lines

# Find the maximum number of frames needed
max_frames = max([len(x) for x in x_lst])

# Create animation
anim = FuncAnimation(fig, animate, frames=max_frames, 
                    interval=dt, blit=True, repeat=True)

# Display the animation
plt.show()
