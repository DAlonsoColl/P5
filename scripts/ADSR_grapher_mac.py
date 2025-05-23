import matplotlib
import matplotlib.pyplot as plt

import numpy as np

# Define the coordinates of the points
points = [
    (0.0, 0.0),  # Start
    (0.1, 0.8),  # Attack
    # (0.3, 0.6),  # Decay
    (0.8, 0.8),  # Sustain
    (1.0, 0.0)   # Release
]

# Extract x and y coordinates
x_coords, y_coords = zip(*points)

# Create the plot
fig, ax = plt.subplots()
ax.plot(x_coords, y_coords, marker='o')

# Set axis titles and figure title
ax.set_xlabel('% De Tiempo En Un Estado')
ax.set_ylabel('Amplitud Relativa (en %)')
ax.set_title('ADSR Instrumento Plano')

# Set axis limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Annotate lines
# annotations = ['Ataque', 'Caída', 'Mantenimiento', 'Liberación']
annotations = ['Ataque', 'Mantenimiento', 'Liberación']

# Add text annotations
for i, text in enumerate(annotations):
    mid_x = (x_coords[i] + x_coords[i + 1]) / 2
    mid_y = (y_coords[i] + y_coords[i + 1]) / 2
    angle = np.arctan2(y_coords[i + 1] - y_coords[i],
                       x_coords[i + 1] - x_coords[i]) * 180 / np.pi
    ax.text(mid_x, mid_y, text, rotation=angle, verticalalignment='bottom')

# Show grid
ax.grid(True)

# Show plot
plt.show()
