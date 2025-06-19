
# 📅 Calendarify (Command-Line App)

A terminal-based tool to generate `.ics` calendar files from BRACU course schedules. It supports recurring classes, lab sessions, and exams, converting them into standard calendar events.

---

## 🚀 Features

- Weekly recurring classes using `RRULE`
- Midterm and Final exam entries
- Support for lab classes
- Timezone handling: Converts Asia/Dhaka to UTC
- Interactive prompt for saving calendar files

---

## 🗂️ Folder Structure

```
command_line_app/
├── backend/
│   ├── app.py                  # Main entry point
│   ├── icsCreator.py           # .ics generation logic
│   ├── dataCollection.py       # Course data handler
│   ├── checkSchedule.py
│   ├── checkScheduleOFFLINE.py
│   ├── welcome.py              # Welcome screen (uses pyfiglet & colorama)
│   └── .cache/connect.json            # Input course data (JSON)
│
├── dist/
│   └── macOS/
│       └── calendarify         # Compiled binary
│
├── build/                      # PyInstaller build cache
├── calendarify_mac.spec        # PyInstaller spec file
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## 🧪 Running the App

### 📦 Run from Python source

```bash
cd backend
python3 app.py
```

### 🖥️ Run the macOS compiled app

```bash
./dist/macOS/calendarify
```

---

## 🔧 Building Your Own Executable

Navigate to <dir>\calendarify\command_line_app\ and follow the below steps:

### 1. Create and activate a virtual environment

For Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
For Windows (PowerShell):
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Build with PyInstaller

For Linux/macOS:
```bash
pyinstaller --onefile   --hidden-import=colorama   --hidden-import=pyfiglet   --add-data "$(python3 -c 'import pyfiglet, os; print(os.path.join(os.path.dirname(pyfiglet.__file__), "fonts"))'):pyfiglet/fonts"   backend/app.py --name calendarify
```
For Windows (PowerShell):
```bash
$fontDir = python -c "import pyfiglet, os; print(os.path.join(os.path.dirname(pyfiglet.__file__), 'fonts'))"

pyinstaller --onefile `
  --hidden-import=colorama `
  --hidden-import=pyfiglet `
  --add-data "$fontDir;pyfiglet/fonts" `
  --name calendarify backend/app.py
```

> 🔁 Use this on Windows to create a `.exe` (must be run from Windows Python environment).

---

## ⚠️ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `No module named 'colorama'` | Install with pip & include in PyInstaller hidden-import |
| `No module named 'pyfiglet.fonts'` | Use `--add-data` option shown above |
| `_tkinter` errors | Use Python downloaded from [python.org](https://python.org) instead of Homebrew |

---

## 🙏 Special Thanks

Special thanks to **[Eniamza](https://eniamza.com/)** for providing the Connect CDN, which made parts of this project possible.

---

## 📄 License

MIT License © 2025 [Anindya Kabbya Biswas]
