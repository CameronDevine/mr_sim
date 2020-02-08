from context import mr_sim
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt

R = 0.1
spacing = 1.75 * R
velocity = 0.1
dt = 0.05

Simulation = mr_sim.create_simulation(
    mr_sim.Round, mr_sim.Flat, mr_sim.Rotary, mr_sim.Preston
)

curve = HilbertCurve(3, 2)

points = np.array(
    [curve.coordinates_from_distance(d) for d in range(curve.max_h + 1)], np.float
)
points -= curve.max_x / 2
points *= spacing

t_final = curve.max_h * spacing / velocity
point_times = np.linspace(0, t_final, points.shape[0])
t = np.arange(0, t_final, dt)

path = np.vstack(
    (np.interp(t, point_times, points[:, 0]), np.interp(t, point_times, points[:, 1]))
).T

size = spacing * curve.max_x + 2 * R

simulation = Simulation(
    size, size, radius=R, dt=dt, dx=0.005, dy=0.005, auto_velocity=True
)

simulation.set_speed(100)
simulation.set_force(5)

for location in path:
    simulation.set_location(*location)
    simulation.step()

plt.figure()
simulation.plot()
plt.plot(points[:, 0], points[:, 1], ":w", linewidth=0.5)
plt.show()
