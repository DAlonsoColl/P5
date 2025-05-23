import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 6]  # Ancho x Alto en pulgadas

# Ruta del archivo de audio
file_path = os.path.join('work', 'seno_vibrato_normal.wav')

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

# Encontrar los índices correspondientes a los tiempos específicos
inicio_1 = np.argmax(time_axis_segunda_nota >= 0.85)
fin_1 = np.argmax(time_axis_segunda_nota >= 0.95)
inicio_2 = np.argmax(time_axis_segunda_nota >= 0.95)
fin_2 = np.argmax(time_axis_segunda_nota >= 1.05)

# Encontrar los valores máximos de la envolvente en los intervalos especificados
max_value_1 = np.max(smoothed_envelope[inicio_1:fin_1])
max_value_2 = np.max(smoothed_envelope[inicio_2:fin_2])

# Encontrar los tiempos correspondientes a estos máximos
time_max_1 = time_axis_segunda_nota[inicio_1 +
                                    np.argmax(smoothed_envelope[inicio_1:fin_1])]
time_max_2 = time_axis_segunda_nota[inicio_2 +
                                    np.argmax(smoothed_envelope[inicio_2:fin_2])]

# Convertir los tiempos de máximo a índices de matriz
inicio_linea_roja = np.searchsorted(time_axis_segunda_nota, time_max_1)
fin_linea_roja = np.searchsorted(time_axis_segunda_nota, time_max_2)

# Calcular el periodo en segundos
periodo_s = time_max_2 - time_max_1

# Calcular el periodo en milisegundos (redondeado)
periodo_ms = np.round(periodo_s * 1000, decimals=2)

# Graficar la segunda nota y sus envolventes suavizadas
plt.plot(time_axis_segunda_nota, audio_data_segunda_nota,
         color='tab:blue', label='Note "Re"', linewidth=0.8)

# Cambiar el color de la línea azul entre los dos máximos de la envolvente
plt.plot(time_axis_segunda_nota[inicio_linea_roja:fin_linea_roja],
         audio_data_segunda_nota[inicio_linea_roja:fin_linea_roja], color='tab:red', linewidth=0.8)

plt.plot(time_axis_segunda_nota, smoothed_envelope, color='tab:orange',
         linestyle='--', label='Upper Envelope', linewidth=2)
plt.plot(time_axis_segunda_nota, -smoothed_envelope, color='tab:green',
         linestyle='--', label='Lower Envelope', linewidth=2)

# Añadir líneas verticales en los puntos de máximo valor de la envolvente
plt.axvline(x=time_max_1, color='red', linestyle='--',
            label=f'Max 1 at {time_max_1:.2f}s')
plt.axvline(x=time_max_2, color='blue', linestyle='--',
            label=f'Max 2 at {time_max_2:.2f}s')

# Añadir texto con el periodo en milisegundos a la leyenda
plt.text(0.65, 0.92, f"Period: {periodo_ms} ms ≈ 100 ms", horizontalalignment='center',
         verticalalignment='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

# Detalles de la gráfica
plt.title(
    "Nota Re Con Trémolo Normal (A=15% & fm=10Hz) + Visualización 1 Período Trémolo")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()  # Ajustar el espaciado
plt.grid(True)  # Habilitar cuadrícula
plt.show()

# Imprimir los valores máximos y los tiempos correspondientes
print(f"Valor máximo en el intervalo 0.85-0.95s: {max_value_1}")
print(f"Valor máximo en el intervalo 0.95-1.05s: {max_value_2}")
