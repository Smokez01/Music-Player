import customtkinter as ctk
from tkinter import filedialog, Listbox
from PIL import Image
from pygame import mixer
import os
import shutil

button_width = 60
button_height = 60
files_folder = "files"

if not os.path.exists(files_folder):
    os.makedirs(files_folder)

f = ctk.CTk()
f.title("Music Player")
f.geometry("800x600")
f.resizable(width=False, height=False)
try:
    f.iconbitmap("images/icon.ico")
except Exception as e:
    print("Icon konnte nicht geladen werden:", e)
f.configure(fg_color="white")

mixer.init()

button_images = {
    "pause": "images/pause.png",
    "unpause": "images/unpause.png",
    "play": "images/play.png",
    "add": "images/addToPlaylist.png",
    "remove": "images/removeFromPlaylist.png",
    "restart": "images/restart.png"
}

button_photos = {name: ctk.CTkImage(Image.open(path), size=(button_width, button_height))
                 for name, path in button_images.items()}

playlist = []

def load_playlist_from_folder():
    global playlist
    playlist = []
    for filename in os.listdir(files_folder):
        if filename.lower().endswith(".mp3"):
            full_path = os.path.join(files_folder, filename)
            playlist.append(full_path)
    update_playlist()

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
    playlist_box.delete(0, 'end')
    for song_path in playlist:
        song_name = os.path.splitext(os.path.basename(song_path))[0]
        playlist_box.insert('end', song_name)

def add_to_playlist():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Audio files", "*.mp3")])
    if file_path:
        basename = os.path.basename(file_path)
        destination = os.path.join(files_folder, basename)
        try:
            shutil.copy(file_path, destination)
        except Exception as e:
            print("Fehler beim Kopieren:", e)
        if destination not in playlist:
            playlist.append(destination)
            update_playlist()

def remove_from_playlist():
    selected_song_index = playlist_box.curselection()
    if selected_song_index:
        file_to_remove = playlist[selected_song_index[0]]
        if os.path.exists(file_to_remove):
            try:
                os.remove(file_to_remove)
            except Exception as e:
                print("Fehler beim Entfernen der Datei:", e)
        playlist.pop(selected_song_index[0])
        update_playlist()

def set_volume(val):
    mixer.music.set_volume(float(val) / 100.0)

def on_closing():
    mixer.music.stop()
    f.destroy()

button_configs = [
    ("restart", restart_music, 212),
    ("unpause", unpause_music, 281),
    ("play", play_music, 350),
    ("pause", pause_music, 419),
    ("add", add_to_playlist, 488),
    ("remove", remove_from_playlist, 557)
]

for name, command, x in button_configs:
    ctk.CTkButton(
        f,
        image=button_photos[name],
        text="",
        command=command,
        fg_color="white",
        hover_color="#d9d9d9",
        corner_radius=0,
        width=button_width,
        height=button_height,
    ).place(x=x, y=531)

playlist_box = Listbox(f, font=("Helvetica", 12))
playlist_box.place(x=20, y=120, width=180, height=400)

volume_slider = ctk.CTkSlider(f, from_=0, to=100, command=set_volume, width=150)
volume_slider.set(50)
volume_slider.place(x=348, y=505)

f.protocol("WM_DELETE_WINDOW", on_closing)
load_playlist_from_folder()
f.mainloop()
