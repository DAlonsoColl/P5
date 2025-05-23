import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [15, 10]  # Ancho x Alto en pulgadas

# Ruta de los archivos de audio
file_path_1 = os.path.join('work', 'seno_vibrato_normal_interpolado.wav')
file_path_2 = os.path.join('work', 'seno_vibrato_normal_Nointerpolado.wav')

# Directorio para guardar la imagen
img_dir = os.path.join('img')
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
img_path = os.path.join(img_dir, 'Waveform_Comparison.png')

# Función para graficar la forma de onda


def plot_waveform(file_path, subplot_index, title):
    # Cargar archivo de audio y frecuencia de muestreo
    sampling_rate, audio_data = wavfile.read(file_path)

    # Calcular duración total del audio
    total_samples = len(audio_data)
    total_time = total_samples / sampling_rate

    # Generar eje de tiempo en segundos
    time_axis = np.linspace(0, total_time, total_samples)

    # Gráfico de la señal en el dominio del tiempo
    plt.subplot(2, 1, subplot_index)
    plt.plot(time_axis, audio_data, color='b')
    plt.title(f'{title} Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


# Graficar las formas de onda de ambos archivos
plt.figure()

# Graficar el primer archivo
plot_waveform(file_path_1, 1, 'Archivo con Interpolación')

# Graficar el segundo archivo
plot_waveform(file_path_2, 2, 'Archivo sin Interpolación')

# Añadir título general
plt.suptitle(
    'Comparación de Waveform entre archivos con y sin Interpolación', fontsize=16)

# Ajustar el diseño de la figura
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Guardar la gráfica en un archivo
plt.savefig(img_path)

# Mostrar la gráfica
plt.show()
