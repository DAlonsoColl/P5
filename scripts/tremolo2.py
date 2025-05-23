import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 6]  # Ancho x Alto en pulgadas

# Ruta del archivo de audio
file_path = os.path.join('work', 'seno_tremolo_agresivo.wav')

# Cargar archivo de audio y frecuencia de muestreo
sampling_rate, audio_data = wavfile.read(file_path)

# Calcular duración total del audio
total_samples = len(audio_data)
total_time = total_samples / sampling_rate

# Asumimos que hay 8 notas de igual duración
num_notas = 8
duracion_nota = total_time / num_notas

# Calcular el rango de tiempo para la segunda nota (nota "re")
inicio_segunda_nota = duracion_nota
fin_segunda_nota = 2 * duracion_nota

# Convertir tiempo a muestras
inicio_muestra = int(inicio_segunda_nota * sampling_rate)
fin_muestra = int(fin_segunda_nota * sampling_rate)

# Extraer la porción de datos para la segunda nota
audio_data_segunda_nota = audio_data[inicio_muestra:fin_muestra]

# Generar eje de tiempo en segundos para la segunda nota
time_axis_segunda_nota = np.linspace(
    inicio_segunda_nota, fin_segunda_nota, fin_muestra - inicio_muestra)

# Calcular la envolvente analítica
analytic_signal = hilbert(audio_data_segunda_nota)
amplitude_envelope = np.abs(analytic_signal)

# Función para suavizar la envolvente usando un filtro de media móvil


def smooth(data, window_len=100):
    window = np.ones(window_len) / window_len
    return np.convolve(data, window, mode='same')


# Suavizar las envolventes
smoothed_envelope = smooth(amplitude_envelope)

# Graficar la segunda nota y sus envolventes suavizadas
plt.plot(time_axis_segunda_nota, audio_data_segunda_nota,
         color='tab:blue', label='Note "Re"', linewidth=0.8)
plt.plot(time_axis_segunda_nota, smoothed_envelope, color='tab:orange',
         linestyle='--', label='Upper Envelope', linewidth=2)
plt.plot(time_axis_segunda_nota, -smoothed_envelope, color='tab:green',
         linestyle='--', label='Lower Envelope', linewidth=2)

# Detalles de la gráfica
plt.title("Re Con Trémolo Agresivo (A=150% & fm=10Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()  # Ajustar el espaciado
plt.grid(True)  # Habilitar cuadrícula
plt.show()
