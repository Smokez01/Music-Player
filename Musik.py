from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from pygame import mixer

# Fenster initialisieren
f = Tk()
f.title("Music Player")
f.geometry("800x600")
f.resizable(width=False, height=False)
f.iconbitmap("images/icon.ico")
f.configure(bg="white")

mixer.init()

# Bilder laden
button_images = {
    "pause": "images/pause.png",
    "unpause": "images/unpause.png",
    "play": "images/play.png",
    "add": "images/addToPlaylist.png",
    "remove": "images/removeFromPlaylist.png",
    "restart": "images/restart.png"
}

button_photos = {name: ImageTk.PhotoImage(Image.open(path)) for name, path in button_images.items()}

playlist = []

# Funktionen
def pause_music():
    mixer.music.pause()

def unpause_music():
    mixer.music.unpause()

def restart_music():
    mixer.music.rewind()

def play_music():
    selected_song_index = playlist_box.curselection()
    if selected_song_index:
        selected_song_path = playlist[selected_song_index[0]]
        mixer.music.load(selected_song_path)
        mixer.music.play()

def update_playlist():
    playlist_box.delete(0, END)
    for song_path in playlist:
        song_name = song_path.split("/")[-1].split(".")[0]
        playlist_box.insert(END, song_name)

def add_to_playlist():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Audio files", "*.mp3")])
    if file_path:
        playlist.append(file_path)
        update_playlist()

def remove_from_playlist():
    selected_song_index = playlist_box.curselection()
    if selected_song_index:
        playlist.pop(selected_song_index[0])
        update_playlist()

def set_volume(val):
    mixer.music.set_volume(int(val) / 100.0)

def on_closing():
    mixer.music.stop()
    f.destroy()
    f.quit()

# Buttons erstellen
button_configs = [
    ("restart", restart_music, 212),
    ("unpause", unpause_music, 281),
    ("play", play_music, 350),
    ("pause", pause_music, 419),
    ("add", add_to_playlist, 488),
    ("remove", remove_from_playlist, 557)
]

for name, command, x in button_configs:
    Button(f, image=button_photos[name], command=command, bg="white", relief=FLAT).place(x=x, y=531)

# Playlist-Box
playlist_box = Listbox(f)
playlist_box.place(x=20, y=120, width=180, height=400)

# Lautstärkeregler
volume_slider = Scale(f, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg="light blue", length=150, sliderlength=20, showvalue=0)
volume_slider.set(50)
volume_slider.place(x=348, y=505)

# Fenster schließen
f.protocol("WM_DELETE_WINDOW", on_closing)
f.mainloop()
