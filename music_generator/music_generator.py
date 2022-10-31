from tkinter import*
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import random
import simpleaudio as sa
from tones.mixer import Mixer

notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Ab', 'Bb', 'Db', 'Eb', 'Gb',
         'A#', 'C#', 'D#', 'E#', 'F#', 'G#']
octaves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

mixer = Mixer(44100, 0.5)


def random_music(size=20, chars=notes, int=octaves):
    mixer.create_track(1, decay=0.1)
    for tunes in range(size):
        random_tone = random.choice(chars)
        random_octave = random.choice(int)
        mixer.add_note(1, note=random_tone, octave=random_octave, duration=0.25)
        mixer.write_wav('tones.wav')


def play_music():
    # Path to file
    f_name = 'tones.wav'

    # create WaveObject instances
    # directly from WAV files on disk
    wave_obj = sa.WaveObject.from_wave_file(f_name)

    # Audio playback
    play = wave_obj.play()

    # To stop after playing the whole audio
    play.wait_done()
    play.stop()


def download_music():
    f = asksaveasfile(initialfile='Untitled.wav',
                      defaultextension=".wav", filetypes=[("WAV file", "*.wav")])


if __name__ == "__main__":
    root = Tk()
    root.title('Music Generator')
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    ttk.Label(frm, text="Music Key Generator").grid(column=0, row=-0)
    play_btn = ttk.Button(frm, text="Generate Music Key", command=random_music)
    generate_btn = ttk.Button(frm, text="Play Music", command=play_music)
    play_btn.grid(column=0, row=1)
    generate_btn.grid(column=0, row=2)
    save_file = ttk.Button(frm, text="Save audio file", command=download_music)
    save_file.grid(column=0, row=5)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=6)
    root.mainloop()
    samples = mixer.mix()

