# 🧠 ContextKeeper

**Smart clipboard manager that automatically groups copied items into contextual sessions**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

---

## 📋 Overview

ContextKeeper isn't just another clipboard manager. It **intelligently groups** everything you copy into **contextual sessions** based on your activity patterns. 

Ever copied a bunch of code snippets, URLs, and error messages while debugging, then lost them? ContextKeeper remembers **what you were working on** and keeps related items together.

### ✨ Features

- 🎯 **Smart Session Detection** - Automatically groups related copied items (2-minute inactivity threshold)
- 💾 **Local-First** - All data stored locally in SQLite - your privacy matters
- 🖥️ **Native GUI** - Clean interface to browse your clipboard history by session
- 🔄 **Real-time Monitoring** - Works silently in the background
- 📊 **Session Timeline** - See what you were working on and when
- 🚀 **Lightweight** - Minimal dependencies, runs anywhere Python runs

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Pantane1/ContextKeeper.git
cd ContextKeeper

# Install dependencies
pip install pyperclip

# Run ContextKeeper
python main.py
```

### Requirements

- Python 3.7 or higher
- `pyperclip` library

---

## 💻 Usage

1. **Launch the app**
   ```bash
   python main.py
   ```

2. **Start copying!** - ContextKeeper runs in the background and captures everything you copy

3. **Browse sessions** - The left panel shows all your sessions with timestamps and item counts

4. **View session details** - Click any session to see all items you copied during that activity period

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Copy text | `Ctrl+C` (Windows/Linux) / `Cmd+C` (macOS) |
| Close app | `Ctrl+C` in terminal or close GUI window |

---

## 🏗️ Architecture

```
ContextKeeper/
├── main.py          # Entry point & orchestrator
├── monitor.py       # Clipboard monitoring thread
├── storage.py       # SQLite database & session logic
├── ui.py           # Tkinter GUI application
└── requirements.txt # Dependencies
```

### How It Works

1. **Monitor Thread** - Listens for clipboard changes every 0.5 seconds
2. **Session Detection** - Creates new sessions after 2 minutes of inactivity
3. **Smart Grouping** - Related items within the same time window are grouped together
4. **Local Storage** - Everything saved to `contextkeeper.db` in your project directory

---

## 🛠️ Configuration

### Database Location
By default, ContextKeeper creates `contextkeeper.db` in the current directory. You can change this in `storage.py`:

```python
db = ContextKeeperDB("your_custom_path.db")
```

### Session Timeout
Adjust the inactivity threshold in `storage.py` (default: 2 minutes):

```python
cutoff = timestamp - timedelta(minutes=2)  # Change '2' to your preference
```

---

## 🐛 Troubleshooting

### "SQLite objects created in a thread" error
**Solution:** Already fixed! ContextKeeper uses `check_same_thread=False` for multi-threaded access.

### "Module not found: pyperclip"
**Solution:** Run `pip install pyperclip` or `pip3 install pyperclip`

### GUI doesn't appear on Linux
**Solution:** Install Tkinter:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

---

## 📝 Roadmap

- [ ] AI-powered session summarization
- [ ] Global hotkey to paste last session items
- [ ] Export sessions to Markdown/JSON
- [ ] Cloud sync with encryption
- [ ] Search across all clips
- [ ] Tagging system for manual organization
- [ ] System tray icon (Windows/macOS)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Pantane1**
- GitHub: [@Pantane1](https://github.com/Pantane1)

---

## ⭐ Show your support

If ContextKeeper helps you stay organized, please give it a ⭐ on GitHub!

---

**Made with 🧠 for developers, researchers, and knowledge workers**

<p align="center">
  <a href="#"><img src="https://github.com/Pantane1/nf/blob/main/public/ph.png" alt="ph-logo">
</p>

<p align="center">
  <a href="#"><img src="http://readme-typing-svg.herokuapp.com?color=ACAF50&center=true&vCenter=true&multiline=false&lines=Built+Different" alt="pantane">
</p>
