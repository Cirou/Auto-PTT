# 🎤 Auto Push-to-Talk by Cirou

**Auto Push-to-Talk by Cirou** is a Python-based application that automatically presses a selected key (or key combination) when it detects audio input above a configurable threshold.  
This tool was created specifically for **Discord users** who need to use **Priority Speaker**, which only works when Push-to-Talk (PTT) is enabled.

With this program, users can **automate the PTT activation** based on voice detection, eliminating the need to manually press the assigned key while speaking.

---

## 🚀 Features
✔️ **Automatic Push-to-Talk activation** based on voice detection  
✔️ **Configurable threshold** to adjust microphone sensitivity  
✔️ **Selectable hotkey** for PTT activation  
✔️ **Supports key combinations** (CTRL, ALT, SHIFT + any key)  
✔️ **Custom press duration** (hold the key for a set time)  
✔️ **Graphical User Interface (GUI)** with an intuitive design  
✔️ **Saves settings automatically** for future sessions  
✔️ **Standalone executable** available for Windows users  

---

## 📥 Installation
### **🔹 Option 1: Run with Python**
1. Install Python (if not already installed) from [python.org](https://www.python.org/downloads/)
2. Clone this repository:
   ```sh
   git clone https://github.com/Cirou/auto-push-to-talk.git
   cd auto-push-to-talk
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the program:
   ```sh
   python autoPTT.py
   ```

### **🔹 Option 2: Run as a Standalone `.exe` (Windows)**
1. Download the pre-compiled `.exe` file from the [Releases](https://github.com/Cirou/Auto-PTT/releases) page.
2. Run `AutoPTT.exe` – **no installation required**.

---

## 🛠 How to Use
1. **Select your microphone** from the dropdown menu.
2. **Choose the key** that will be pressed when voice is detected.
3. **(Optional) Enable modifiers** like CTRL, ALT, or SHIFT.
4. **Adjust the activation threshold** using the slider.
5. **Set the key press duration** (how long the key remains pressed after activation).
6. **Click "Start"** to begin voice detection.
7. **Click "Stop"** to deactivate the system.

---

## 🔧 Building the `.exe` File
To create a standalone **Windows executable**, use **PyInstaller**:
```sh
pip install pyinstaller
pyinstaller --onefile --windowed --name AutoPTT autoPTT.py
```
The `.exe` file will be generated in the `dist/` folder.

---

## ❓ FAQ
### **Does this work with Discord?**
✅ **Yes!** The tool was specifically designed for **Discord Priority Speaker**, which requires Push-to-Talk.

### **Can I use it in games or other applications?**
Yes! The tool simply simulates a key press when voice is detected, so it can be used in any application that supports keyboard shortcuts.

### **Why is my antivirus flagging the `.exe`?**
Some antivirus programs may flag PyInstaller-generated executables as false positives. You can build the `.exe` yourself using the steps above if needed.

### **Does this work on macOS/Linux?**
Currently, this tool is **Windows-only**. However, you can run the Python script on macOS/Linux with minor modifications.

---

## 👨‍💻 Author
Developed by **Cirou**  
GitHub: [Cirou](https://github.com/Cirou)  

---

## 📜 License
This project is licensed under the **MIT License**.
