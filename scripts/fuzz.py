import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# Ruta de los archivos de audio
file_path_with_fuzz = os.path.join('work', 'audio_con_fuzz.wav')
file_path_without_fuzz = os.path.join('work', 'seno.wav')

# Función para visualizar la forma de onda y el espectrograma del archivo de audio
def visualize_audio_effects(file_path_with_fuzz, file_path_without_fuzz):
    # Cargar archivos de audio
    sampling_rate_with_fuzz, audio_data_with_fuzz = wavfile.read(file_path_with_fuzz)
    sampling_rate_without_fuzz, audio_data_without_fuzz = wavfile.read(file_path_without_fuzz)

    # Generar eje de tiempo en segundos
    total_samples_with_fuzz = len(audio_data_with_fuzz)
    total_time_with_fuzz = total_samples_with_fuzz / sampling_rate_with_fuzz
    time_axis_with_fuzz = np.linspace(0, total_time_with_fuzz, total_samples_with_fuzz)

    total_samples_without_fuzz = len(audio_data_without_fuzz)
    total_time_without_fuzz = total_samples_without_fuzz / sampling_rate_without_fuzz
    time_axis_without_fuzz = np.linspace(0, total_time_without_fuzz, total_samples_without_fuzz)

    # Plotear formas de onda
    plt.figure(figsize=(15, 12))

    plt.subplot(4, 1, 1)
    plt.plot(time_axis_without_fuzz, audio_data_without_fuzz, color='g')
    plt.title('Audio sin Efecto Fuzz - Forma de Onda')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    plt.subplot(4, 1, 2)
    plt.plot(time_axis_with_fuzz, audio_data_with_fuzz, color='b')
    plt.title('Audio con Efecto Fuzz - Forma de Onda')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    # Plotear espectrogramas
    plt.subplot(4, 1, 3)
    f_without_fuzz, t_without_fuzz, Sxx_without_fuzz = signal.spectrogram(audio_data_without_fuzz, fs=sampling_rate_without_fuzz)
    plt.pcolormesh(t_without_fuzz, f_without_fuzz, 10 * np.log10(Sxx_without_fuzz), shading='gouraud')
    plt.title('Audio sin Efecto Fuzz - Espectrograma')
    plt.ylabel('Frecuencia (Hz)')
    plt.xlabel('Tiempo (s)')
    plt.colorbar().set_label('Intensidad (dB)')

    plt.subplot(4, 1, 4)
    f_with_fuzz, t_with_fuzz, Sxx_with_fuzz = signal.spectrogram(audio_data_with_fuzz, fs=sampling_rate_with_fuzz)
    plt.pcolormesh(t_with_fuzz, f_with_fuzz, 10 * np.log10(Sxx_with_fuzz), shading='gouraud')
    plt.title('Audio con Efecto Fuzz - Espectrograma')
    plt.ylabel('Frecuencia (Hz)')
    plt.xlabel('Tiempo (s)')
    plt.colorbar().set_label('Intensidad (dB)')

    plt.tight_layout()
    plt.show()

# Llamar a la función para visualizar los archivos de audio
visualize_audio_effects(file_path_with_fuzz, file_path_without_fuzz)
