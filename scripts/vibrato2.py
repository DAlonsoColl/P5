import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [10, 20]  # Ancho x Alto en pulgadas

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
    max_freq_limit = 1000  # Hz
    max_visible_index = np.argmax(fft_freqs >= max_freq_limit)

    # Gráfico de la señal en el dominio del tiempo
    plt.subplot(10, 2, subplot_index)
    plt.plot(time_axis, audio_data, color='b')
    plt.title(f'{title} Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia)
    plt.subplot(10, 2, subplot_index + 1)
    plt.plot(fft_freqs[:max_visible_index],
             fft_abs[:max_visible_index], color='r')
    plt.title(f'{title} FFT (Frequency Spectrum)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

# Función para graficar la FFT de una nota específica del caso vibrato


def plot_individual_note_fft(file_path_vibrato, subplot_index, note_name):
    # Cargar archivo de audio y frecuencia de muestreo
    sampling_rate, audio_data = wavfile.read(file_path_vibrato)

    # Duración total del audio
    total_samples = len(audio_data)
    total_time = total_samples / sampling_rate

    # Calcular la duración de cada nota (asumiendo 8 notas equidistribuidas)
    note_duration = total_time / 8

    # Definir los tiempos de inicio y fin para la nota específica
    note_index = ['do (Low)', 're', 'mi', 'fa', 'sol',
                  'la', 'si', 'do (High)'].index(note_name)
    start_time = note_duration * note_index
    end_time = start_time + note_duration

    # Convertir tiempos a índices de muestra
    start_sample = int(start_time * sampling_rate)
    end_sample = int(end_time * sampling_rate)

    # Extraer la porción de datos para la nota específica
    audio_data_note = audio_data[start_sample:end_sample]

    # Generar eje de tiempo en segundos para la nota específica
    time_axis_note = np.linspace(start_time, end_time, len(audio_data_note))

    # Calcular la Transformada de Fourier de la señal de la nota específica
    fft_result_note = np.fft.fft(audio_data_note)
    fft_freqs_note = np.fft.fftfreq(len(fft_result_note), 1 / sampling_rate)

    # Calcular los valores absolutos de la FFT de la nota específica
    fft_abs_note = np.abs(fft_result_note)

    # Limitar la visualización hasta 2.5 kHz para la nota específica
    max_freq_limit = 1000  # Hz
    max_visible_index = np.argmax(fft_freqs_note >= max_freq_limit)

    # Gráfico de la señal de la nota específica en el dominio del tiempo
    plt.subplot(10, 2, subplot_index)
    plt.plot(time_axis_note, audio_data_note, color='g')
    plt.title(f'Vibrato "{note_name.capitalize()}" Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia) de la nota específica
    plt.subplot(10, 2, subplot_index + 1)
    plt.plot(fft_freqs_note[:max_visible_index],
             fft_abs_note[:max_visible_index], color='m')
    plt.title(f'Vibrato "{note_name.capitalize()}" FFT (Frequency Spectrum)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas


# Graficar ambas señales y sus FFT, incluyendo las 8 notas del caso vibrato
plt.figure()

# Comparar el archivo normal (sin efectos)
plot_fft_comparison(file_path_normal, 1, 'Normal')

# Comparar el archivo con vibrato
plot_fft_comparison(file_path_vibrato, 3, 'Vibrato')

# Graficar las notas individuales del caso vibrato
notes = ['do (Low)', 're', 'mi', 'fa', 'sol', 'la', 'si', 'do (High)']
for i, note in enumerate(notes):
    plot_individual_note_fft(file_path_vibrato, 5 + 2 * i, note)

# Ajustar el diseño de la figura
plt.tight_layout()

# Mostrar la gráfica
plt.show()
