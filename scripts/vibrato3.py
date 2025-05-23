import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks, savgol_filter

# Lista para almacenar los picos encontrados
peaks_normal = []
peaks_vibrato = []

# Configuración para el tamaño del gráfico
plt.rcParams['figure.figsize'] = [15, 25]  # Ancho x Alto en pulgadas

# Ruta de los archivos de audio
file_path_normal = os.path.join('work', 'seno.wav')
file_path_vibrato = os.path.join('work', 'seno_vibrato_normal_interpolado.wav')

# Directorio para guardar la imagen
img_dir = os.path.join('img')
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
img_path = os.path.join(img_dir, 'DoReMi_Vibrato_normal_interpolado_FFT.png')

# Función para calcular y graficar la FFT limitada hasta 1 kHz y agregar líneas de picos


def plot_fft_comparison_with_peaks(file_path, subplot_index, title):
    global peaks_normal, peaks_vibrato  # Acceder a los picos globales

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

    # Limitar la visualización hasta 1 kHz
    max_freq_limit = 2000  # Hz
    max_visible_index = np.argmax(fft_freqs >= max_freq_limit)

    # Gráfico de la señal en el dominio del tiempo
    plt.subplot(9, 3, 1)
    plt.plot(time_axis, audio_data, color='b')
    plt.title(f'Normal Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia)
    plt.subplot(9, 3, subplot_index + 1)
    plt.plot(fft_freqs[:max_visible_index],
             fft_abs[:max_visible_index], color='r')
    plt.title(f'{title} FFT (Frequency Spectrum)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

    if (subplot_index == 1):
        # Encontrar picos en la FFT
        # Aplicar filtro Savitzky-Golay para suavizar
        smoothed_fft_abs = savgol_filter(fft_abs[:max_visible_index], 51, 3)
        peaks, _ = find_peaks(smoothed_fft_abs, distance=int(
            2 / (fft_freqs[1] - fft_freqs[0])))  # Encontrar picos

        # Tomar los 8 picos más altos
        if len(peaks) > 8:
            peak_values = smoothed_fft_abs[peaks]
            # Indices de los 8 picos más altos
            peak_indices = peaks[np.argsort(-peak_values)[:8]]
            peak_freqs = fft_freqs[:max_visible_index][peak_indices]
        else:
            peak_freqs = fft_freqs[:max_visible_index][peaks]

        # Guardar los picos encontrados en las variables globales
        peaks_normal = list(peak_freqs)

    # Graficar los picos como líneas verticales
    for freq in peaks_normal:
        plt.axvline(x=freq, color='g', linestyle='--', linewidth=1)

    # Retornar la lista de picos identificados
    return peaks_normal

# Función para graficar la FFT de una nota específica del caso vibrato


def plot_individual_note_fft(file_path_normal, file_path_vibrato, subplot_index, note_name):
    global peaks_normal, peaks_vibrato  # Acceder a los picos globales

    # Cargar archivo de audio y frecuencia de muestreo
    sampling_rate_normal, audio_data_normal = wavfile.read(file_path_normal)
    sampling_rate_vibrato, audio_data_vibrato = wavfile.read(file_path_vibrato)

    # Duración total del audio
    total_samples = len(audio_data_vibrato)
    total_time = total_samples / sampling_rate_vibrato

    # Calcular la duración de cada nota (asumiendo 8 notas equidistribuidas)
    note_duration = total_time / 8

    # Definir los tiempos de inicio y fin para la nota específica
    note_index = ['do', 're', 'mi', 'fa', 'sol',
                  'la', 'si', 'do2'].index(note_name)
    start_time = note_duration * note_index
    end_time = start_time + note_duration

    # Convertir tiempos a índices de muestra
    start_sample = int(start_time * sampling_rate_vibrato)
    end_sample = int(end_time * sampling_rate_vibrato)

    # Extraer la porción de datos para la nota específica
    audio_data_note_normal = audio_data_normal[start_sample:end_sample]
    audio_data_note_vibrato = audio_data_vibrato[start_sample:end_sample]

    # Generar eje de tiempo en segundos para la nota específica
    time_axis_note = np.linspace(
        start_time, end_time, len(audio_data_note_normal))

    # Calcular la Transformada de Fourier de la señal de la nota específica
    fft_result_note_normal = np.fft.fft(audio_data_note_normal)
    fft_result_note_vibrato = np.fft.fft(audio_data_note_vibrato)
    fft_freqs_note = np.fft.fftfreq(
        len(fft_result_note_normal), 1 / sampling_rate_normal)

    # Calcular los valores absolutos de la FFT de la nota específica
    fft_abs_note_normal = np.abs(fft_result_note_normal)
    fft_abs_note_vibrato = np.abs(fft_result_note_vibrato)

    # Limitar la visualización hasta 1 kHz para la nota específica
    max_freq_limit = 2000  # Hz
    max_visible_index = np.argmax(fft_freqs_note >= max_freq_limit)

    # Gráfico de la señal de la nota específica en el dominio del tiempo
    plt.subplot(9, 3, subplot_index)
    plt.plot(time_axis_note, audio_data_note_normal, color='g')
    plt.title(f'Normal "{note_name.capitalize()}" Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Gráfico de la FFT (espectro de frecuencia) de la nota específica - Normal
    plt.subplot(9, 3, subplot_index + 1)
    plt.plot(fft_freqs_note[:max_visible_index],
             fft_abs_note_normal[:max_visible_index], color='m')
    plt.title(f'Normal "{note_name.capitalize()}" FFT')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

    # Graficar los picos globales como líneas verticales
    for freq in peaks_normal:
        plt.axvline(x=freq, color='g', linestyle='--', linewidth=1)

    # Gráfico de la FFT (espectro de frecuencia) de la nota específica - Vibrato
    plt.subplot(9, 3, subplot_index + 2)
    plt.plot(fft_freqs_note[:max_visible_index],
             fft_abs_note_vibrato[:max_visible_index], color='c')
    plt.title(f'Vibrato "{note_name.capitalize()}" FFT')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)  # Limitar el rango de frecuencias mostradas

    # Graficar los picos globales como líneas verticales
    for freq in peaks_vibrato:
        plt.axvline(x=freq, color='g', linestyle='--', linewidth=1)


# Graficar ambas señales y sus FFT, incluyendo las 8 notas del caso vibrato
plt.figure()

# Comparar el archivo normal (sin efectos)
peaks_normal = plot_fft_comparison_with_peaks(file_path_normal, 1, 'Normal')

# Comparar el archivo con vibrato
peaks_vibrato = plot_fft_comparison_with_peaks(file_path_vibrato, 2, 'Vibrato')

# Graficar las notas individuales del caso vibrato
notes = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si', 'do2']
for i, note in enumerate(notes):
    plot_individual_note_fft(
        file_path_normal, file_path_vibrato, 4 + 3 * i, note)

# Añadir título general
plt.suptitle(
    'DoReMi con Vibrato con FFT individual para cada nota', fontsize=16)

# Ajustar el diseño de la figura
plt.tight_layout(rect=[0, 0, 1, 0.97])

# Guardar la gráfica en un archivo
plt.savefig(img_path)

# Mostrar la gráfica
plt.show()

# Usar los picos encontrados (ejemplo de cómo acceder a los picos)
print("Picos encontrados en la FFT del archivo normal:", peaks_normal)
print("Picos encontrados en la FFT del archivo con vibrato:", peaks_vibrato)
