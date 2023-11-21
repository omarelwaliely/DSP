import numpy as np
from scipy.io import wavfile
from scipy.signal import convolve
import matplotlib.pyplot as plt

def filter(input,output, L):
    rate, inputAud = wavfile.read(input)
    n = np.arange(0, L + 1) #n is not one value its an array from 0-> L+1 so I did that here
    h = (1 / (L*(n + 1))) * (np.heaviside(n, 1) - np.heaviside(n - L, 1))
    h = h / np.sum(np.abs(h))#doing some normalization
    filtered = convolve(inputAud, h, mode='full') 
    filtered = filtered[:len(inputAud)]#I use mode full above which seems to pad with 0's so i clipped it to be the original input signal length 
    filtered = filtered * (np.max(np.abs(inputAud)) / np.max(np.abs(filtered))) #normalzing to be the same as input signal
    wavfile.write(output, rate, filtered.astype(np.int16))


def plot(signal, label, samples=1500, ax=None): 
    ax.plot(signal[:samples], label=label)
    ax.set_title(label)
    ax.legend()

clean = 'CleanTone.wav'
dirty= 'NoisyTone.wav'

filter(dirty, 'Filtered_L_3.wav', L=3)
filter(dirty, 'Filtered_L_15.wav', L=15)
filter(dirty, 'Filtered_L_100.wav', L=500)

_ , cleansig = wavfile.read(clean)
_ , dirtysig = wavfile.read(dirty)
_, L3 = wavfile.read('Filtered_L_3.wav')
_, L15 = wavfile.read('Filtered_L_15.wav')
_, L100 = wavfile.read('Filtered_L_100.wav')

fig, axs = plt.subplots(5, 1, figsize=(7, 7))
plot(cleansig, label='Clean Signal', ax=axs[0])
plot(dirtysig, label='Noisy Signal', ax=axs[1])
plot(L3, label='Filtered (L = 3)', ax=axs[2])
plot(L15, label='Filtered (L = 15)', ax=axs[3])
plot(L100, label='Filtered (L = 100)', ax=axs[4])

plt.tight_layout()
plt.show()