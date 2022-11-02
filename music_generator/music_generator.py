from tkinter import*
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askdirectory
import random
import simpleaudio as playback_audio
from tones.mixer import Mixer
from tones import SINE_WAVE,  SAWTOOTH_WAVE
import shutil

notes = ['A', 'E', 'F', 'G', 'Ab', 'Bb', 'Db', 'Eb', 'Gb',
         'A#', 'C#', 'D#', 'E#', 'F#', 'G#']
octaves = [1, 2, 3, 4, 5, 6]

mixer = Mixer(44100, 0.5)


def get_username():
    global username, filename
    filename = username.get()
    # ttk.Label.configure(text=filename)


# create a random music
def random_music(size=50, second_size=25, chars=notes, int=octaves):
    # create a track to be used when adding tones
    mixer.create_track(1, attack=0.01, decay=0.1)
    mixer.create_track(0, attack=0.05, decay=0.5)
    # loop to generate music with 40 tones each tones lasting 3 seconds
    for tunes in range(size):
        # generate a random note from notes list
        random_tone = random.choice(chars)
        # generate a random octave from octaves list
        random_octave = random.choice(int)
        # add tone to the music
        mixer.add_note(1, note=random_tone, octave=random_octave, duration=0.30)
        # save a file called tones.wav
    for tunes in range(second_size):
        # generate a random note from notes list
        random_tone = random.choice(chars)
        # generate a random octave from octaves list
        random_octave = random.choice(int)
        # add tone to the music
        mixer.add_note(0, note=random_tone, octave=random_octave, duration=0.60)
        # save a file called tones.wav
    mixer.write_wav(filename + '.wav')


def play_music():
    # play path to file
    f_name = filename + '.wav'
    # instantiate the WaveObject directly from wav files on disk
    audio = playback_audio.WaveObject.from_wave_file(f_name)
    # playback the audio
    play = audio.play()
    # stop the audio after it finishes
    play.wait_done()
    play.stop()


def download_music():
    f = askdirectory()
    shutil.copy(filename + '.wav', f)


if __name__ == "__main__":
    frm = Tk()
    frm.title('Music Generator')
    frm.geometry("185x250")
    ttk.Label(frm, text="Music Key Generator").grid(column=0, row=0)
    ttk.Label(frm, text="Enter your preferred music name:").grid(column=0, row=1)
    username = ttk.Entry()
    username.grid(column=0, row=2)
    confirm_name = ttk.Button(frm, text="Confirm name", command=get_username)
    confirm_name.grid(column=0, row=3)
    username.focus_set()
    play_btn = ttk.Button(frm, text="Generate Music Key", command=random_music)
    generate_btn = ttk.Button(frm, text="Play Music", command=play_music)
    play_btn.grid(column=0, row=4)
    generate_btn.grid(column=0, row=5)
    label = Label(frm)
    label.grid(column=0, row=6)
    save_file = ttk.Button(frm, text="Save audio file", command=download_music)
    save_file.grid(column=0, row=6)
    ttk.Button(frm, text="Quit", command=frm.destroy).grid(column=0, row=7)
    frm.mainloop()
    samples = mixer.mix()
