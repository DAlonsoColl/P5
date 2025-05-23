import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 6]  # Ancho x Alto en pulgadas

# Ruta del archivo de audio
file_path = os.path.join('work', 'seno_tremolo_agresivo.wav')

# Cargar archivo de audio y frecuencia de muestreo
sampling_rate, audio_data = wavfile.read(file_path)

# Calcular duración total del audio
total_samples = len(audio_data)
total_time = total_samples / sampling_rate

# Generar eje de tiempo en segundos
time_axis = np.linspace(0, total_time, total_samples)

# Graficar la nota entera
plt.plot(time_axis, audio_data, color='tab:blue', label='Note', linewidth=0.8)

# Detalles de la gráfica
plt.title("DoReMi Con Trémolo Agresivo (A=150% & fm=10Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()  # Ajustar el espaciado
plt.grid(True)  # Habilitar cuadrícula
plt.show()
