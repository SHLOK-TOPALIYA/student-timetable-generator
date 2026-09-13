<div align="center">

# 🎓 Student Timetable Generator

**Turn your university's full timetable into your own personalized timetable — in seconds.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-See%20LICENSE-blue?style=for-the-badge)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](#-contributing)

### 🚀 [**Open the Live App**](https://student-timetable-generator.streamlit.app) — no installation required

</div>

---

A web app that reads your official **Lecture**, **Lab**, and **Tutorial** timetable files and builds a clean, personalized PDF timetable — just for the courses, sections, and groups that matter to you.

No more scrolling through a 700-row university master timetable to find your own classes. Upload the file, enter your course codes, pick your sections/groups, and download a ready-to-use PDF.

<br>

## 📋 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Timetable Modes](#-timetable-modes)
- [Course-Code Matching](#-course-code-matching)
- [Supported File Formats](#-supported-input-formats)
- [Run Locally](#-run-locally)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Privacy](#-privacy)
- [Built With](#️-built-with)
- [Contributing](#-contributing)
- [License](#-license)

<br>

## ✨ Features

| | |
|---|---|
| 📚 | Lecture-only timetable generation |
| 🧪 | Lab & Tutorial-only timetable generation |
| 📅 | Complete timetable — lectures + labs + tutorials combined |
| ➕ | Add newly released Lab/Tutorial schedules to an existing generated timetable |
| 🔎 | Course-code based matching — add as many courses as you need, no fixed limit |
| 🔀 | Automatic lecture section detection and handling |
| 👥 | Automatic Lab/Tutorial group detection, with selections reused across courses |
| ⚠️ | Conflict detection for overlapping classes |
| 📄 | Clean, print-ready A4 PDF output |
| 📤 | Supports `.xlsx`, `.xlsm`, `.pdf`, and `.csv` timetable files |
| 🏷️ | Keeps course, type, section, group, room, and schedule details intact |
| 🔒 | No university timetable files are stored or included in this repository |

<br>

## 🧠 How It Works

**1️⃣ Upload your official timetable**
Supports Lecture timetables, Lab & Tutorial timetables, or an existing generated Lecture PDF.

**2️⃣ Enter your course codes**
Input fields expand automatically as you add more courses.

**3️⃣ Select sections & groups**
If a course has multiple sections or groups, you'll be asked to choose. A shared selection is reused across courses wherever it applies.

**4️⃣ Check for conflicts**
The app scans your selected schedule for overlapping time slots and flags any conflicts before you download.

**5️⃣ Generate your timetable**
All selected lectures, labs, and tutorials are combined into one clean weekly view, with schedule and room details included.

**6️⃣ Download your PDF**
Ready to save, print, view on your phone, or share.

<br>

## 📋 Timetable Modes

| Mode | Description |
|---|---|
| 📚 **Lecture Timetable Only** | Generate only lecture schedules |
| 🧪 **Lab & Tutorial Timetable Only** | Generate only labs and tutorials |
| 📅 **Complete Timetable** | Combine lectures, labs, and tutorials |
| ➕ **Add Lab & Tutorial** | Add labs and tutorials to an existing lecture timetable |

<br>

## 🔎 Course-Code Matching

The app uses a **conservative matching approach** so it never guesses incorrectly on your behalf.

- **Exact match** — if the requested course code exists directly in the uploaded timetable, it's matched automatically.
- **Different course code** — a differently-named course is never silently assumed to be the same. If a plausible related course is found (e.g. a separate lab code for a lecture), you're explicitly asked to confirm before it's added.

This prevents mistakes like treating `CT101` and `CT102` as the same course just because they look similar.

<br>

## 📁 Supported Input Formats

| Format | Extension |
|---|---|
| Excel Workbook | `.xlsx` |
| Excel Macro-Enabled Workbook | `.xlsm` |
| PDF Document | `.pdf` |
| CSV File | `.csv` |

The uploaded timetable is always treated as the source of truth for schedule information.

<br>

## 🎯 Why This Project?

University timetables can contain hundreds of entries spanning multiple semesters, courses, sections, labs, tutorials, time slots, and rooms. Finding just the classes relevant to *one* student is a repetitive, error-prone manual task.

This project automates that — upload the official timetable once, and get back exactly your own schedule.

<br>

## 🛠️ Built With

<div align="left">

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenPyXL](https://img.shields.io/badge/OpenPyXL-217346?style=flat-square&logo=microsoft-excel&logoColor=white)](https://openpyxl.readthedocs.io/)
[![pdfplumber](https://img.shields.io/badge/pdfplumber-EC1C24?style=flat-square)](https://github.com/jsvine/pdfplumber)
[![ReportLab](https://img.shields.io/badge/ReportLab-4285F4?style=flat-square)](https://www.reportlab.com/)

</div>

<br>

## 💻 Run Locally

Prefer to run it on your own machine instead of using the hosted version?

```bash
# 1. Clone the repository
git clone https://github.com/SHLOK-TOPALIYA/student-timetable-generator.git
cd student-timetable-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

The app will open automatically in your browser.

> **Windows shortcut:** double-click `install_and_run.bat` to install dependencies and launch in one step, or `run.bat` if dependencies are already installed.

<br>

## 📂 Project Structure

```text
student-timetable-generator/
│
├── app.py                 # Streamlit application (UI)
├── core.py                # Timetable parsing and generation logic
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── LICENSE                # Project license
├── run.bat                # Windows run script
└── install_and_run.bat    # Windows installation and run script
```

<br>

## 🌐 Deployment

This application is deployed on **Streamlit Community Cloud**, directly from this GitHub repository.

### 🚀 [student-timetable-generator.streamlit.app](https://student-timetable-generator.streamlit.app)

<br>

## 🔐 Privacy

- University timetable files are **not included** in this public repository.
- Users provide their own timetable files at runtime, directly through the app.
- Uploaded files are processed in-memory to generate your PDF and are not stored.

<br>

## 🤝 Contributing

Suggestions, improvements, and bug reports are always welcome!

If you have an idea that could make this more useful for students, feel free to:

- 🐛 [Open an issue](https://github.com/SHLOK-TOPALIYA/student-timetable-generator/issues)
- 🔧 Submit a pull request

<br>

## ⭐ Support the Project

If you find this project useful, consider giving the repository a **star** ⭐ — it helps more students discover it.

<br>

## 📄 License

This project is licensed under the terms of the [LICENSE](./LICENSE) included in this repository.

---

<div align="center">

Made with ❤️ for students tired of squinting at giant timetable spreadsheets.

</div>
