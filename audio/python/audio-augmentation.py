from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift
import librosa
import soundfile as sf

augment = Compose([
    AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5), #ruido
    TimeStretch(min_rate=0.9, max_rate=1.25, p=0.5), # velocidad
    PitchShift(min_semitones=-4, max_semitones=4, p=0.5) # tono
])

y, sr = librosa.load(librosa.example('nutcracker'))

# Aplicamos los filtros
augmented = augment(samples=y, sample_rate=sr)

# Persistimos el audio
sf.write('audio_augmented.wav', augmented, sr)
