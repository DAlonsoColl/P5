import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 6]  # Ancho x Alto en pulgadas

# Ruta del archivo de audio
file_path = os.path.join('work', 'seno.wav')

# Cargar archivo de audio y frecuencia de muestreo
sampling_rate, audio_data = wavfile.read(file_path)

# Definir parámetros de la envolvente ADSR
attack_time = 0.1   # Tiempo de ataque en segundos
decay_time = 0.2     # Tiempo de decaimiento en segundos
sustain_time = 0.5  # Tiempo de sustain en segundos
release_time = 0.2   # Tiempo de liberación en segundos

# Calcular duración total del audio
total_samples = len(audio_data)

# Convertir tiempos de ADSR a muestras
attack_samples = int(attack_time * total_samples)
decay_samples = int(decay_time * total_samples)
sustain_samples = int(sustain_time * total_samples)
release_samples = int(release_time * total_samples)

# Generar eje de tiempo en segundos
time_axis = np.linspace(0, 1, total_samples)

note_data = audio_data[:total_samples]

attack_data = note_data[:attack_samples]
decay_data = note_data[attack_samples:attack_samples + decay_samples]
sustain_data = note_data[attack_samples +
                         decay_samples:attack_samples + decay_samples + sustain_samples]
release_data = note_data[-release_samples:]

# apply normalization to data samples
max_value = note_data.max()
attack_data_normalized = np.divide(attack_data, max_value)
decay_data_normalized = np.divide(decay_data, max_value)
sustain_data_normalized = np.divide(sustain_data, max_value)
release_data_normalized = np.divide(release_data, max_value)

# Graficar la envolvente ADSR
plt.plot(time_axis[:attack_samples],
         attack_data_normalized, color='tab:red', label='Attack', linewidth=0.8)
plt.plot(time_axis[attack_samples: attack_samples +
         decay_samples], decay_data_normalized, color='tab:orange', label='Decay', linewidth=0.8)
plt.plot(time_axis[attack_samples + decay_samples:
         attack_samples + decay_samples + sustain_samples], sustain_data_normalized, color='tab:green', label='Sustain', linewidth=0.8)
plt.plot(time_axis[attack_samples + decay_samples + sustain_samples + 1:],
         release_data_normalized, color='tab:purple', label='Release', linewidth=0.8)

# Detalles de la gráfica
plt.title("ADSR Genérica")
plt.xlabel("% De Tiempo En Un Estado")
plt.ylabel("Amplitud Relativa (en %% del total)")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()  # Ajustar el espaciado
plt.grid(True)  # Habilitar cuadrícula
plt.show()
