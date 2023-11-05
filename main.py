# Programmieren 1 - AudioProjekt

import scipy.io.wavfile as wavfile
from scipy import signal
import warnings
import sounddevice as sd
import soundfile as sf

def get_file_input(file_list, message):
    while True:
        try:
            user_input = int(input(message))
            if 1 <= user_input <= len(file_list):
                return file_list[user_input - 1]
            elif user_input > len(file_list):
                print(f"Aktuell befinden sich in unserer Library nur {len(file_list)} Samples.")
            else:
                print("Ungültige Zahl")
        except ValueError:
            print("Keine Zahl erkennbar.")

def show_statistics(file_name):
    with warnings.catch_warnings():  # ChatGP
        warnings.simplefilter("ignore", wavfile.WavFileWarning)
        rate, data = wavfile.read(file_name)
    N = data.shape[0]
    CHN = data.shape[1] if len(data.shape) == 2 else 1

    print(f"Statistiken zu {file_name}:")
    print(f"Audiodatei {file_name} mit Abtastrate {rate}Hz")
    print(f"Anzahl der Abtastwerte in der Datei: {N}")
    print(f"Anzahl der Audio-Kanäle (1=Mono, 2=Stereo): {CHN}")
    print(f"Dauer: {N/rate:.3f}s")
    print(f"Die ersten Abtastwerte:")
    print(data[:5])

xFile = ['piano.wav', 'spoken.wav']     # import signal
hFile = ['big_hall.wav', 'classroom.wav'] # impulse signal

x_selected = get_file_input(xFile, "X FILE: 'piano.wav' (1), 'spoken.wav' (2)")
h_selected = get_file_input(hFile, "H FILE: 'big_hall.wav' (1), 'classroom.wav' (2)")

with warnings.catch_warnings(): # ChatGPT
    warnings.simplefilter("ignore", wavfile.WavFileWarning)
    rateX, x = wavfile.read(x_selected)
    rateH, h = wavfile.read(h_selected)

assert(rateX == rateH)

# From stereo to mono (average value of both signals)
x = x.mean(axis=1) if len(x.shape) > 1 else x
h = h.mean(axis=1) if len(h.shape) > 1 else x

# convolution (german: Faltung)
y = signal.fftconvolve(x, h)

# scale to +-32765 and change to int
y /= max(abs(y))
y *= (2**15-1)
y = y.astype('int16')

# save
yFile = "y.wav"
wavfile.write(yFile, rateX, y)

taskFinished = False
while not taskFinished:
    playSound = input("Sound abspielen (y/n) ")
    if playSound.lower() == "y":
        with warnings.catch_warnings():  # ChatGPT
            warnings.simplefilter("ignore", wavfile.WavFileWarning)
            rateY, fs = sf.read(yFile)
        duration_to_play = 5  # 5 Sekunden
        data_to_play = rateY[:int(duration_to_play * fs)]
        sd.play(data_to_play, fs)
        sd.wait()
        taskFinished = True
    elif playSound.lower() == "n":
        taskFinished = True

taskFinished = False
while not taskFinished:
    checkStatistic = input("Statistiken anzeigen (y/n) ")
    if  checkStatistic.lower() == "y":
        show_statistics(x_selected)
        show_statistics(h_selected)
        show_statistics('y.wav')
        taskFinished = True
    elif checkStatistic.lower() == "n":
        taskFinished = True