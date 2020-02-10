from context import mr_sim
import numpy as np
import matplotlib.pyplot as plt

R = 3.5 / 2 * 25.4 / 1000
length = 208 / 1000
period = 0.2 * 20
dt = period / 1000
dt = dt / 4
amp = length / 2

Simulation = mr_sim.create_simulation(
    mr_sim.Round, mr_sim.Flat, mr_sim.Orbital, mr_sim.Preston
)

simulation = Simulation(
    length + 2 * R,
    2 * R,
    kp=1.362e-9,
    radius=R,
    eccentricity=0.1875 * 25.4 / 1000,
    dt=dt,
    auto_velocity=True,
)

simulation.set_speed(620)
simulation.set_force(15)

for t in np.arange(0, period / 2, dt):
    simulation.set_location(amp * np.cos(2 * t * np.pi / period))
    simulation.step()

plt.figure()
simulation.plot()
plt.show()
