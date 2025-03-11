import subprocess
import sys
import json
import os
import time
import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
from tkinter import ttk

# 📂 File di configurazione
CONFIG_FILE = "config.json"

# 📌 Funzione per caricare la configurazione salvata
def carica_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

# 📌 Funzione per salvare la configurazione
def salva_config():
    config = {
        "microfono": microfono_var.get(),
        "tasto": tasto_var.get(),
        "ctrl": mod_ctrl.get(),
        "alt": mod_alt.get(),
        "shift": mod_shift.get(),
        "soglia": soglia_var.get(),
        "delay": delay_var.get()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# 🔎 Rimuove i dispositivi duplicati dalla lista
def get_unique_devices():
    devices = sd.query_devices()
    seen = set()
    unique_devices = []
    for d in devices:
        name = d["name"]
        if name not in seen and d["max_input_channels"] > 0:
            seen.add(name)
            unique_devices.append(name)
    return unique_devices
    
    # ▶️ Funzione per avviare l'ascolto
def start_listening():
    global stream, running
    if running:
        return  # Evita di riavviare se già attivo

    try:
        index_microfono = dispositivi_audio.index(microfono_var.get())
        num_canali = sd.query_devices(index_microfono)["max_input_channels"]

        running = True
        start_button.config(state="disabled")
        stop_button.config(state="normal")

        stream = sd.InputStream(callback=audio_callback, channels=num_canali, samplerate=44100, blocksize=1024, device=index_microfono)
        stream.start()
        status_label.config(text="Ascoltando...", fg="black")
    except Exception as e:
        status_label.config(text=f"Errore: {e}", fg="red")

# ⏹️ Funzione per fermare l'ascolto
def stop_listening():
    global stream, running
    if running:
        running = False
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        stream.stop()
        stream.close()
        status_label.config(text="Premi 'Start' per ascoltare", fg="black")

# 🌎 Variabili globali
running = False
stream = None
dispositivi_audio = get_unique_devices()
config = carica_config()

# 🖼️ Creazione GUI
root = tk.Tk()
root.title("Auto Push-to-Talk by Cirou")
root.geometry("450x480")  # Aumentata l'altezza per far spazio ai pulsanti Start e Stop
root.resizable(False, False)

# 🎤 Variabili di configurazione
microfono_var = tk.StringVar(value=config.get("microfono", dispositivi_audio[0] if dispositivi_audio else "Nessun microfono"))
tasto_var = tk.StringVar(value=config.get("tasto", "SPACE"))
soglia_var = tk.DoubleVar(value=config.get("soglia", 15.0))
delay_var = tk.DoubleVar(value=config.get("delay", 200))

# 🔘 Stato pulsanti
start_enabled = tk.BooleanVar(value=True)
stop_enabled = tk.BooleanVar(value=False)

# 🎭 Dizionario per i tasti del tastierino numerico
mappa_tasti_numpad = {
    "NUMPAD 0": "0", "NUMPAD 1": "1", "NUMPAD 2": "2", "NUMPAD 3": "3",
    "NUMPAD 4": "4", "NUMPAD 5": "5", "NUMPAD 6": "6", "NUMPAD 7": "7",
    "NUMPAD 8": "8", "NUMPAD 9": "9", "NUMPAD +": "add", "NUMPAD -": "subtract",
    "NUMPAD *": "multiply", "NUMPAD /": "divide"
}

# 🔠 Lista tasti con maiuscole
tutti_i_tasti = [
    "SPACE", "ENTER", "BACKSPACE", "TAB", "CAPS LOCK", "ESC", "PRINT SCREEN", "PAUSE",
    "INSERT", "DELETE", "HOME", "END", "PAGE UP", "PAGE DOWN", "UP", "DOWN", "LEFT", "RIGHT",
    "NUM LOCK", "SCROLL LOCK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"
] + [f"NUMPAD {i}" for i in range(10)] + [chr(i).upper() for i in range(97, 123)]

# 🖥️ UI: Label di stato
status_label = tk.Label(root, text="Premi 'Start' per ascoltare", font=("Arial", 12))
status_label.pack(pady=10)

# 📊 UI: Barra di avanzamento
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=10)

# 🎙️ UI: Selezione microfono
tk.Label(root, text="Seleziona il microfono:").pack(pady=5)
microfono_menu = ttk.Combobox(root, textvariable=microfono_var, values=dispositivi_audio, state="readonly", width=30)
microfono_menu.pack()

# ⌨️ UI: Checkbox modificatori
mod_ctrl = tk.BooleanVar(value=config.get("ctrl", False))
mod_alt = tk.BooleanVar(value=config.get("alt", False))
mod_shift = tk.BooleanVar(value=config.get("shift", False))

frame_checkbox = tk.Frame(root)
frame_checkbox.pack(pady=5)
tk.Checkbutton(frame_checkbox, text="CTRL", variable=mod_ctrl, command=salva_config).pack(side="left", padx=5)
tk.Checkbutton(frame_checkbox, text="ALT", variable=mod_alt, command=salva_config).pack(side="left", padx=5)
tk.Checkbutton(frame_checkbox, text="SHIFT", variable=mod_shift, command=salva_config).pack(side="left", padx=5)

# 🖱️ UI: Menu per il tasto
tk.Label(root, text="Seleziona il tasto principale:").pack(pady=5)
tasto_menu = ttk.Combobox(root, textvariable=tasto_var, values=tutti_i_tasti, state="readonly", width=20)
tasto_menu.pack()
tasto_menu.bind("<<ComboboxSelected>>", lambda e: salva_config())

# 🎚️ UI: Slider per la soglia
tk.Label(root, text="Soglia di attivazione:").pack(pady=5)
soglia_slider = ttk.Scale(root, from_=5, to=50, orient="horizontal", variable=soglia_var, length=350, command=lambda x: salva_config())
soglia_slider.pack()

# 🕒 UI: Slider per il delay con valore aggiornato
delay_frame = tk.Frame(root)
delay_frame.pack(pady=5)
tk.Label(delay_frame, text="Durata pressione tasto (ms):").pack(side="left")

delay_value_label = tk.Label(delay_frame, text=f"{int(delay_var.get())} ms")
delay_value_label.pack(side="left", padx=10)

def update_delay_label(value):
    delay_value_label.config(text=f"{int(float(value))} ms")
    salva_config()

delay_slider = ttk.Scale(root, from_=50, to=1000, orient="horizontal", variable=delay_var, length=350, command=update_delay_label)
delay_slider.pack()

# ▶️ Pulsanti Start e Stop (Riaggiunti)
start_button = tk.Button(root, text="Start", command=lambda: start_listening(), width=15)
start_button.pack(pady=5)
stop_button = tk.Button(root, text="Stop", command=lambda: stop_listening(), width=15, state="disabled")
stop_button.pack(pady=5)

# 🎤 Funzione di callback per il rilevamento audio
def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)
    progress["value"] = min(volume_norm * 300, 100)
    soglia_db = soglia_var.get() / 50

    if volume_norm > soglia_db:
        combo_keys = []
        if mod_ctrl.get():
            combo_keys.append("ctrl")
        if mod_alt.get():
            combo_keys.append("alt")
        if mod_shift.get():
            combo_keys.append("shift")

        tasto_selezionato = tasto_var.get()
        if tasto_selezionato in mappa_tasti_numpad:
            tasto_selezionato = mappa_tasti_numpad[tasto_selezionato]

        combo_keys.append(tasto_selezionato.lower())
        keyboard.press("+".join(combo_keys))
        time.sleep(delay_var.get() / 1000)  # ⏳ Mantiene il tasto premuto per il delay configurato
        keyboard.release("+".join(combo_keys))
        status_label.config(text=f"Premuto: {' + '.join(combo_keys).upper()}", fg="red")
    else:
        status_label.config(text="Ascoltando...", fg="black")

root.mainloop()
