from Vicon import Vicon
from Trajectories import rigid_marker
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from Vicon import Markers
from Utilities import Mean_filter
import time


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_autoscale_on(False)
data = Vicon.Vicon("/home/nathaniel/gait_analysis_toolkit/testing_data/ben_leg_bend.csv")
markers = data.get_markers()
markers.smart_sort()
markers.auto_make_frames()
cor_filter = Mean_filter.Mean_Filter(10)
aor_filter = Mean_filter.Mean_Filter(10)

x = []
y = []
z = []

ax.clear()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.axis([-500, 500, -750, 1500])
ax.set_zlim3d(0, 1250)

offset = 3
shank_markers = markers.get_rigid_body("ben:RightShank")[0:]
thigh_markers = markers.get_rigid_body("ben:RightThigh")[0:]
shank_markers = markers.get_rigid_body("ben:RightShank")

m1 = shank_markers[0][150:350]
m2 = shank_markers[1][150:350]
m3 = shank_markers[2][150:350]
m4 = shank_markers[3][150:350]
data = [m1, m2, m3, m4]

core = Markers.calc_CoR(data)
axis = Markers.calc_AoR(data)
shank = Markers.calc_mass_vect([shank_markers[0][0],
                                shank_markers[1][0],
                                shank_markers[2][0],
                                shank_markers[3][0]])

thigh = Markers.calc_mass_vect([thigh_markers[0][0],
                                thigh_markers[1][0],
                                thigh_markers[2][0],
                                thigh_markers[3][0]])

sol = Markers.minimize_center((thigh, shank), axis=axis, initial=(core[0][0], core[1][0], core[2][0]))
temp_center = sol.x


def animate(frame):
    x = []
    y = []
    z = []
    m = markers.get_rigid_body("ben:hip")[0:]
    x += [m[0][frame].x, m[1][frame].x, m[2][frame].x, m[3][frame].x]
    y += [m[0][frame].y, m[1][frame].y, m[2][frame].y, m[3][frame].y]
    z += [m[0][frame].z, m[1][frame].z, m[2][frame].z, m[3][frame].z]

    m = markers.get_rigid_body("ben:RightThigh")[0:]
    x += [m[0][frame].x, m[1][frame].x, m[2][frame].x, m[3][frame].x]
    y += [m[0][frame].y, m[1][frame].y, m[2][frame].y, m[3][frame].y]
    z += [m[0][frame].z, m[1][frame].z, m[2][frame].z, m[3][frame].z]

    m = markers.get_rigid_body("ben:RightShank")[0:]
    x += [m[0][frame].x, m[1][frame].x, m[2][frame].x, m[3][frame].x]
    y += [m[0][frame].y, m[1][frame].y, m[2][frame].y, m[3][frame].y]
    z += [m[0][frame].z, m[1][frame].z, m[2][frame].z, m[3][frame].z]

    shank = Markers.calc_mass_vect( [shank_markers[0][frame],
                                     shank_markers[1][frame],
                                     shank_markers[2][frame],
                                     shank_markers[3][frame]])

    thigh = Markers.calc_mass_vect([thigh_markers[0][frame],
                                    thigh_markers[1][frame],
                                    thigh_markers[2][frame],
                                    thigh_markers[3][frame]])

    # (31.86380164,391.24609261,533.73053426)

    T_Th = markers.get_frame("ben:RightThigh")[frame]
    T_Sh = markers.get_frame("ben:RightShank")[frame]
    T = np.dot(np.linalg.pinv(T_Th), T_Sh)
    offset = np.dot(np.linalg.pinv(T_Th), np.append(shank, 1).reshape((-1, 1)))

    axis, theta = Markers.R_to_axis_angle(T[:3, :3])
    axis_x = []
    axis_y = []
    axis_z = []

    for ii in xrange(-1000, 1000):

        temp = np.array([[ii*axis[0]], [ii*axis[1]], [ii*axis[2]], [1]])
        trans = np.dot( np.linalg.pinv(T), temp)
        axis_x.append( trans[0][0])
        axis_y.append( trans[1][0])
        axis_z.append(trans[2][0])

    ax.clear()
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.axis([-500, 500, -750, 1500])
    ax.set_zlim3d(0, 1250)
    ax.scatter(x, y, z, c='r', marker='o')

    ax.scatter([thigh[0], shank[0], temp_center[0]],
               [thigh[1], shank[1], temp_center[1]],
               [thigh[2], shank[2], temp_center[2]], c='g', marker='o')
    ax.plot(axis_x, axis_y, axis_z, 'b')

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
np.savetxt("angles.csv", np.asarray(angles), delimiter=",")



