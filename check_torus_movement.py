import utils
import numpy as np

x, y = 0.0, 0.5 # point 1 
x0, y0, u0, v0 = .5, .5, .25, 0.5 # movement parameters
dt = 0.02

n = 500
d = np.zeros((n, 2))
for i in xrange(n):
    x_pos = x0 + dt * i * u0
    y_pos = y0 + dt * i * v0
    dx = utils.torus_distance(x, x_pos)
    dy = utils.torus_distance(y, y_pos)
#    dx = utils.torus_distance(x_pos, x)
#    dy = utils.torus_distance(y_pos, y)
#    d[i, 0] = dt * i
#    d[i, 1] = dx
#    d[i, 0] = dt * i
#    d[i, 1] = dx
    d[i, 0] = dx
    d[i, 1] = dy
#    print x_pos, '\t', x_pos % 1, '\t', y_pos, '\t', np.sqrt(dx**2 + dy**2)
    print x_pos, '\t', x_pos % 1, '\t', y_pos, '\t', dx, '\t', dy

np.savetxt('delme_torus_movement.dat', d)


