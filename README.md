# 🎓 Student Timetable Generator

> **Turn a university's full timetable into your own personalized timetable — in seconds.**

A simple web application that helps university students generate a clean, personalized timetable from their official **Lecture, Lab, and Tutorial timetable files**.

Instead of manually searching through a large university timetable, students can upload the official timetable, enter their course codes, choose the required sections/groups, and generate a ready-to-use PDF timetable.

---

## 🚀 Live Demo

**Coming soon — the public Streamlit app will be available here.**

---

## ✨ Features

- 📚 Generate **Lecture-only** timetables
- 🧪 Generate **Lab & Tutorial-only** timetables
- 📅 Generate a **Complete Timetable** with lectures, labs, and tutorials
- ➕ Add Lab & Tutorial schedules to an existing Lecture timetable
- 🔎 Match courses using their official course codes
- ♾️ Add as many courses as needed — no fixed course limit
- 🔀 Handle courses with multiple sections
- 👥 Handle Lab and Tutorial groups
- ⚠️ Detect timetable conflicts automatically
- 📄 Generate a clean, printable **A4 PDF timetable**
- 📤 Support timetable files in **XLSX, XLSM, PDF, and CSV** formats
- 🏷️ Automatically include course type, section, group, room, and schedule details
- 🔐 No university timetable files are stored in the public repository

---

## 🧠 How It Works

### 1️⃣ Upload the Official Timetable

Upload the timetable provided by your university.

The application can work with:

- Lecture timetable
- Lab & Tutorial timetable
- Existing generated Lecture timetable

### 2️⃣ Select Your Courses

Enter the course codes you want in your personal timetable.

The course input fields automatically expand as you add more courses.

### 3️⃣ Choose Sections & Groups

If a course has multiple sections or groups, the application asks you to select the appropriate one.

Where possible, a common section/group selection is reused across applicable courses.

### 4️⃣ Check for Conflicts

The application checks the selected schedules for overlapping time slots and clearly reports conflicts.

### 5️⃣ Generate Your Timetable

The application creates a clean weekly timetable covering:

**Monday → Friday**

with the relevant lecture, lab, and tutorial information.

### 6️⃣ Download the PDF

Your personalized timetable is generated as a PDF that can be saved, printed, or shared.

---

## 📋 Timetable Modes

| Mode | Purpose |
|---|---|
| 📚 Lecture Timetable Only | Generate only lecture schedules |
| 🧪 Lab & Tutorial Only | Generate only lab and tutorial schedules |
| 📅 Complete Timetable | Combine lectures, labs, and tutorials |
| ➕ Add Lab & Tutorial | Add lab/tutorial schedules to an existing lecture timetable |

---

## 🔎 Course-Code Matching

The application follows a conservative matching approach.

### Exact match

If the course code exists directly in the uploaded timetable, it is matched automatically.

### Different course code

A different course code is **never silently assumed to be the same course**.

If a possible matching course is found, the application asks the user to explicitly confirm whether it represents the same course.

This helps avoid incorrect Lab or Tutorial schedules being added to a timetable.

---

## 📁 Supported Input Files

The application supports:

- `.xlsx`
- `.xlsm`
- `.pdf`
- `.csv`

The uploaded timetable acts as the source of truth for schedule information.

---

## 🛠️ Technology

Built using:

- 🐍 **Python**
- 🎈 **Streamlit**
- 📊 **OpenPyXL**
- 📄 **pdfplumber**
- 📝 **ReportLab**

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/SHLOK-TOPALIYA/student-timetable-generator.git
cd student-timetable-generator
