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
attack_time = 0.02   # Tiempo de ataque en segundos
decay_time = 0.1     # Tiempo de decaimiento en segundos
sustain_time = 0.38  # Tiempo de sustain en segundos
release_time = 0.1   # Tiempo de liberación en segundos

# Calcular duración total del audio
total_samples = len(audio_data)
total_time = total_samples / sampling_rate

# Convertir tiempos de ADSR a muestras
attack_samples = int(attack_time * sampling_rate)
decay_samples = int(decay_time * sampling_rate)
sustain_samples = int(sustain_time * sampling_rate)
release_samples = int(release_time * sampling_rate)

# Generar eje de tiempo en segundos
time_axis = np.linspace(0, total_time, total_samples)

# Definir segmentos de la nota y su envolvente
note_start_time = 0.0
note_duration = attack_time + decay_time + sustain_time + release_time

note_start_sample = int(note_start_time * sampling_rate)
note_end_sample = note_start_sample + int(note_duration * sampling_rate)

note_data = audio_data[note_start_sample:note_end_sample]

attack_data = note_data[:attack_samples]
decay_data = note_data[attack_samples:attack_samples + decay_samples]
sustain_data = note_data[attack_samples +
                         decay_samples:attack_samples + decay_samples + sustain_samples]
release_data = note_data[-release_samples:]

# Graficar la envolvente ADSR
plt.plot(time_axis[note_start_sample:note_start_sample + attack_samples],
         attack_data, color='tab:red', label='Attack', linewidth=0.8)
plt.plot(time_axis[note_start_sample + attack_samples:note_start_sample + attack_samples +
         decay_samples], decay_data, color='tab:orange', label='Decay', linewidth=0.8)
plt.plot(time_axis[note_start_sample + attack_samples + decay_samples:note_end_sample -
         release_samples], sustain_data, color='tab:green', label='Sustain', linewidth=0.8)
plt.plot(time_axis[note_end_sample - release_samples:note_end_sample],
         release_data, color='tab:purple', label='Release', linewidth=0.8)

# Detalles de la gráfica
plt.title("ADSR Envelope for a Single Note")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()  # Ajustar el espaciado
plt.grid(True)  # Habilitar cuadrícula
plt.show()
