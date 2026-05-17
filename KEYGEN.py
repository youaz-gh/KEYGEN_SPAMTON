import os
import time
import threading
import urllib.request
import tkinter as tk
from tkinter import messagebox
import winsound

folder = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Temp", "KEYGEN")
os.makedirs(folder, exist_ok=True)

url = "https://drive.google.com/uc?export=download&id=1fedl_SxArHwCv16AAkFgzcpSKNccjp34"
dest = os.path.join(folder, "keygen.wav")

if not os.path.exists(dest):
    print(f"Downloading to {dest}...")
    urllib.request.urlretrieve(url, dest)
    print("Download complete.")
else:
    print(f"File already exists")

root = tk.Tk()
root.withdraw()

overlay = tk.Toplevel(root)
overlay.attributes("-fullscreen", True)
overlay.attributes("-alpha", 0.20)
overlay.attributes("-topmost", True)
overlay.overrideredirect(True)

canvas = tk.Canvas(overlay, highlightthickness=0)
canvas.pack(fill="both", expand=True)

screen_w = overlay.winfo_screenwidth()
screen_h = overlay.winfo_screenheight()

rect = canvas.create_rectangle(0, 0, screen_w, screen_h, fill="red", outline="")

hue = 0.0

def hsv_to_hex(h, s=1.0, v=1.0):
    h = h % 1.0
    i = int(h * 6)
    f = h * 6 - i
    p, q, t = v*(1-s), v*(1-f*s), v*(f*s)
    r, g, b = [
        (v, t, p), (q, v, p), (p, v, t),
        (p, q, v), (t, p, v), (v, p, q)
    ][i % 6]
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def animate():
    global hue
    hue = (hue + 0.002) % 1.0
    color = hsv_to_hex(hue)
    canvas.itemconfig(rect, fill=color)
    overlay.after(16, animate)

animate()

stop_audio = threading.Event()

def play_loop():
    while not stop_audio.is_set():
        winsound.PlaySound(dest, winsound.SND_FILENAME)

audio_thread = threading.Thread(target=play_loop, daemon=True)
audio_thread.start()

def show_message():
    time.sleep(0.3)
    messagebox.showerror("", "[KEYGEN]")
    stop_audio.set()
    winsound.PlaySound(None, winsound.SND_PURGE)
    root.quit()

threading.Thread(target=show_message, daemon=True).start()

root.mainloop()
overlay.destroy()