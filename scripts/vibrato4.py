import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# Ruta de los archivos de audio
file_path_with_vibrato = os.path.join('work', 'seno_vibrato_agresivo.wav')
file_path_without_vibrato = os.path.join('work', 'seno.wav')

# Función para visualizar la forma de onda y el espectrograma del archivo de audio
def visualize_audio_effects(file_path_with_vibrato, file_path_without_vibrato):
    # Cargar archivos de audio
    sampling_rate_with_vibrato, audio_data_with_vibrato = wavfile.read(file_path_with_vibrato)
    sampling_rate_without_vibrato, audio_data_without_vibrato = wavfile.read(file_path_without_vibrato)

    # Generar eje de tiempo en segundos
    total_samples_with_vibrato = len(audio_data_with_vibrato)
    total_time_with_vibrato = total_samples_with_vibrato / sampling_rate_with_vibrato
    time_axis_with_vibrato = np.linspace(0, total_time_with_vibrato, total_samples_with_vibrato)

    total_samples_without_vibrato = len(audio_data_without_vibrato)
    total_time_without_vibrato = total_samples_without_vibrato / sampling_rate_without_vibrato
    time_axis_without_vibrato = np.linspace(0, total_time_without_vibrato, total_samples_without_vibrato)

    # Plotear formas de onda
    plt.figure(figsize=(15, 12))

    plt.subplot(4, 1, 1)
    plt.plot(time_axis_without_vibrato, audio_data_without_vibrato, color='g')
    plt.title('Audio sin Efecto vibrato - Forma de Onda')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    plt.subplot(4, 1, 2)
    plt.plot(time_axis_with_vibrato, audio_data_with_vibrato, color='b')
    plt.title('Audio con Efecto vibrato - Forma de Onda')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    # Plotear espectrogramas
    plt.subplot(4, 1, 3)
    f_without_vibrato, t_without_vibrato, Sxx_without_vibrato = signal.spectrogram(audio_data_without_vibrato, fs=sampling_rate_without_vibrato)
    plt.pcolormesh(t_without_vibrato, f_without_vibrato, 10 * np.log10(Sxx_without_vibrato), shading='gouraud')
    plt.title('Audio sin Efecto vibrato - Espectrograma')
    plt.ylabel('Frecuencia (Hz)')
    plt.xlabel('Tiempo (s)')
    plt.colorbar().set_label('Intensidad (dB)')

    plt.subplot(4, 1, 4)
    f_with_vibrato, t_with_vibrato, Sxx_with_vibrato = signal.spectrogram(audio_data_with_vibrato, fs=sampling_rate_with_vibrato)
    plt.pcolormesh(t_with_vibrato, f_with_vibrato, 10 * np.log10(Sxx_with_vibrato), shading='gouraud')
    plt.title('Audio con Efecto vibrato - Espectrograma')
    plt.ylabel('Frecuencia (Hz)')
    plt.xlabel('Tiempo (s)')
    plt.colorbar().set_label('Intensidad (dB)')

    plt.tight_layout()
    plt.show()

# Llamar a la función para visualizar los archivos de audio
visualize_audio_effects(file_path_with_vibrato, file_path_without_vibrato)
