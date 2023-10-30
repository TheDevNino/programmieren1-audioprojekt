import scipy.io.wavfile as wavfile

roomfn = 'big_hall.wav'
rate, data = wavfile.read(roomfn)
N = data.shape[0]
CHN = data.shape[1] if len(data.shape) == 2 else 1

print(f"Audiodatei {roomfn} mit Abtastrate {rate}Hz")
print(f"Anzahl der Abtastwerte in der Datei: {N}")
print(f"Anzahl der Audio-Kanäle (1=Mono, 2=Stereo): {CHN}")
print(f"Dauer: {N/rate:.3f}s")
print(f"Die ersten vier Abtastwerte:")
print(data[:4])