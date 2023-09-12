import numpy as np
import matplotlib.pyplot as plt
from sunposition import sunpos
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

# Specify the observer's location (latitude and longitude in degrees)
observer_latitude = 38.0  # Replace with your latitude
observer_longitude = -9.0  # Replace with your longitude

# Get the current time
now = datetime.utcnow()

# Calculate sun's position (azimuth and zenith angle) at the current time for the observer's location
az, zen = sunpos(now, observer_latitude, observer_longitude, 0)[:2]  # Discard RA, dec, H

# Invert the direction of the zenith angle to altitude
altitude = 90 - zen

# Invert the direction of the azimuth angle
azimuth = az + 180  # Invert direction

# Convert azimuth and altitude to spherical coordinates (theta and phi)
theta = (90 - altitude) * np.pi / 180  # Invert direction and convert to radians
phi = azimuth * np.pi / 180  # Convert to radians

# Create a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Calculate the 3D coordinates of the sun
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Plot the sun as a point
sun_point = ax.scatter(x, -y, z, color='yellow', s=100, label='Sun')  # Invert y value

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set axis limits
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Set the aspect ratio of the plot to be equal
ax.set_box_aspect([1, 1, 1])

# Set the title
ax.set_title(f'Sun Position at {now.strftime("%Y-%m-%d %H:%M:%S UTC")}')

# Add lines representing azimuth and altitude angles
ax.plot([0, x], [0, -y], [0, z], 'r', label=f'Azimuth Angle ({azimuth:.2f}°)')
ax.plot([x, x], [-y, -y], [0, z], 'g', label=f'Altitude Angle ({altitude:.2f}°)')  # Invert y value

# Define the flat surface (a grid)
surface_length = 2.0  # Adjust the length as needed
grid_x = np.linspace(-surface_length / 2, surface_length / 2, 100)
grid_y = np.linspace(-surface_length / 2, surface_length / 2, 100)
grid_x, grid_y = np.meshgrid(grid_x, grid_y)
grid_z = np.zeros_like(grid_x)

# Plot the flat surface with Z=0
ax.plot_surface(grid_x, grid_y, grid_z, color='blue', alpha=0.2, label='Earth Surface')

# Add arrows for north and west directions (aligned with true north)
arrow_length = 0.2
ax.quiver(0, 0, arrow_length, 0, 0, 0, color='red', label='West', pivot='tail', arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, -arrow_length, 0, 0, color='blue', label='North', pivot='tail', arrow_length_ratio=0.1)

# Create custom legend handles and labels with markers
legend_handles = [
    Line2D([0], [0], color='yellow', marker='o', markersize=8, label='Sun'),
    Line2D([0], [0], color='blue', marker='o', markersize=8, label='North'),
    
]

# Show the 3D plot with the custom legend
ax.legend(handles=legend_handles, loc='upper left')
ax.view_init(elev=10, azim=0)  # Adjust the view orientation
plt.show()
