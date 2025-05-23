import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Ruta de los archivos de audio
file_path_1 = os.path.join('work', 'clarineteSimple1.wav')
file_path_2 = os.path.join('work', 'clarineteSimple2.wav')

# Función para calcular y graficar la FFT de una sola nota con ambas FFT superpuestas
def plot_single_note_fft(file_path_1, file_path_2, note_index):
    # Cargar archivos de audio y frecuencias de muestreo
    sampling_rate_1, audio_data_1 = wavfile.read(file_path_1)
    sampling_rate_2, audio_data_2 = wavfile.read(file_path_2)

    # Duración total del audio
    total_samples_1 = len(audio_data_1)
    total_samples_2 = len(audio_data_2)
    total_time_1 = total_samples_1 / sampling_rate_1
    total_time_2 = total_samples_2 / sampling_rate_2

    # Calcular la duración de cada nota (asumiendo 8 notas equidistribuidas)
    note_duration_1 = total_time_1 / 8
    note_duration_2 = total_time_2 / 8

    # Definir los tiempos de inicio y fin para la nota específica
    start_time_1 = note_duration_1 * note_index
    end_time_1 = start_time_1 + note_duration_1

    start_time_2 = note_duration_2 * note_index
    end_time_2 = start_time_2 + note_duration_2

    # Convertir tiempos a índices de muestra
    start_sample_1 = int(start_time_1 * sampling_rate_1)
    end_sample_1 = int(end_time_1 * sampling_rate_1)

    start_sample_2 = int(start_time_2 * sampling_rate_2)
    end_sample_2 = int(end_time_2 * sampling_rate_2)

    # Extraer la porción de datos para la nota específica
    audio_data_note_1 = audio_data_1[start_sample_1:end_sample_1]
    audio_data_note_2 = audio_data_2[start_sample_2:end_sample_2]

    # Calcular la Transformada de Fourier de la señal de la nota específica
    fft_result_note_1 = np.fft.fft(audio_data_note_1)
    fft_result_note_2 = np.fft.fft(audio_data_note_2)
    fft_freqs_note_1 = np.fft.fftfreq(len(fft_result_note_1), 1 / sampling_rate_1)
    fft_freqs_note_2 = np.fft.fftfreq(len(fft_result_note_2), 1 / sampling_rate_2)

    # Calcular los valores absolutos de la FFT de la nota específica
    fft_abs_note_1 = np.abs(fft_result_note_1)
    fft_abs_note_2 = np.abs(fft_result_note_2)

    # Limitar la visualización hasta 1 kHz para la nota específica
    max_freq_limit = 1000  # Hz
    max_visible_index_1 = np.argmax(fft_freqs_note_1 >= max_freq_limit)
    max_visible_index_2 = np.argmax(fft_freqs_note_2 >= max_freq_limit)

    # Gráfico de la FFT (espectro de frecuencia) de la nota específica
    plt.figure(figsize=(10, 6))

    # Gráfico de la FFT de ambas señales superpuestas
    plt.plot(fft_freqs_note_1[:max_visible_index_1], fft_abs_note_1[:max_visible_index_1], color='b', label='FFT I=1 & N2=2')
    plt.plot(fft_freqs_note_2[:max_visible_index_2], fft_abs_note_2[:max_visible_index_2], color='r', label='FFT I=3 & N2=4')
    plt.title(f'Note {note_index + 1} FFT Comparison')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, max_freq_limit)
    plt.legend()

    # Ajustar el diseño de la figura
    plt.tight_layout()
    
    # Directorio para guardar la imagen
    img_dir = os.path.join('img')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    # Guardar la gráfica en un archivo
    img_path = os.path.join(img_dir, f'Note_{note_index + 1}_FFT_Comparison.png')
    plt.savefig(img_path)
    
    # Mostrar la gráfica
    plt.show()

# Especifica el índice de la nota (0 a 7 para do a do2)
note_index = 0  # Cambiar este valor según la nota deseada (0 para la primera nota, 1 para la segunda, etc.)

# Ejecutar la función para graficar la FFT de la nota específica
plot_single_note_fft(file_path_1, file_path_2, note_index)
