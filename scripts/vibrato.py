import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 6]  # Ancho x Alto en pulgadas

# Ruta de los archivos de audio
file_path_normal = os.path.join('work', 'seno.wav')
file_path_vibrato = os.path.join('work', 'seno_vibrato_normal.wav')

# Función para calcular y graficar la FFT limitada hasta 2.5 kHz
def plot_fft_comparison(file_path, subplot_index, title):
    # Cargar archivo de audio y frecuencia de muestreo
    sampling_rate, audio_data = wavfile.read(file_path)

    # Calcular duración total del audio
    total_samples = len(audio_data)
    total_time = total_samples / sampling_rate

    # Generar eje de tiempo en segundos
    time_axis = np.linspace(0, total_time, total_samples)

    # Calcular la Transformada de Fourier de la señal
    fft_result = np.fft.fft(audio_data)
    fft_freqs = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)

    # Calcular los valores absolutos de la FFT (magnitud)
    fft_abs = np.abs(fft_result)

    # Limitar la visualización hasta 2.5 kHz
    max_freq_limit = 2500  # Hz
    max_visible_index = np.argmax(fft_freqs >= max_freq_limit)

    # Gráfico de la señal en el dominio del tiempo
    plt.subplot(3, 2, subplot_index)
    plt.plot(time_axis, audio_data, color='b')
    plt.title(f'{title} Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia)
    plt.subplot(3, 2, subplot_index + 1)
    plt.plot(fft_freqs[:max_visible_index], fft_abs[:max_visible_index], color='r')
    plt.title(f'{title} FFT (Frequency Spectrum)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

# Función para graficar la FFT de la nota "Re" del caso vibrato
def plot_re_vibrato(file_path_vibrato, subplot_index):
    # Cargar archivo de audio y frecuencia de muestreo
    sampling_rate, audio_data = wavfile.read(file_path_vibrato)

    # Duración total del audio
    total_samples = len(audio_data)
    total_time = total_samples / sampling_rate

    # Nota "Re" tiene duración de 1 segundo, asumiendo 8 notas equidistribuidas
    duracion_nota = total_time / 8
    inicio_segunda_nota = duracion_nota
    fin_segunda_nota = 2 * duracion_nota

    # Convertir tiempo a muestras
    inicio_muestra = int(inicio_segunda_nota * sampling_rate)
    fin_muestra = int(fin_segunda_nota * sampling_rate)

    # Extraer la porción de datos para la segunda nota (Re)
    audio_data_segunda_nota = audio_data[inicio_muestra:fin_muestra]

    # Generar eje de tiempo en segundos para la segunda nota
    time_axis_segunda_nota = np.linspace(inicio_segunda_nota, fin_segunda_nota, fin_muestra - inicio_muestra)

    # Calcular la Transformada de Fourier de la señal de la segunda nota (Re)
    fft_result_segunda_nota = np.fft.fft(audio_data_segunda_nota)
    fft_freqs_segunda_nota = np.fft.fftfreq(len(fft_result_segunda_nota), 1 / sampling_rate)

    # Calcular los valores absolutos de la FFT de la segunda nota (Re)
    fft_abs_segunda_nota = np.abs(fft_result_segunda_nota)

    # Limitar la visualización hasta 2.5 kHz para la segunda nota (Re)
    max_freq_limit = 2500  # Hz
    max_visible_index = np.argmax(fft_freqs_segunda_nota >= max_freq_limit)

    # Gráfico de la señal de la segunda nota (Re) en el dominio del tiempo
    plt.subplot(3, 2, subplot_index)
    plt.plot(time_axis_segunda_nota, audio_data_segunda_nota, color='g')
    plt.title('Vibrato "Re" Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia) de la segunda nota (Re)
    plt.subplot(3, 2, subplot_index + 1)
    plt.plot(fft_freqs_segunda_nota[:max_visible_index], fft_abs_segunda_nota[:max_visible_index], color='m')
    plt.title('Vibrato "Re" FFT (Frequency Spectrum)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

# Graficar ambas señales y sus FFT, incluyendo la nota "Re" del caso vibrato
plt.figure()

# Comparar el archivo normal (sin efectos)
plot_fft_comparison(file_path_normal, 1, 'Normal')

# Comparar el archivo con vibrato
plot_fft_comparison(file_path_vibrato, 3, 'Vibrato')

# Graficar la nota "Re" del caso vibrato
plot_re_vibrato(file_path_vibrato, 5)

# Ajustar el diseño de la figura
plt.tight_layout()

# Mostrar la gráfica
plt.show()
