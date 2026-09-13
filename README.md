# 🎓 Student Timetable Generator

> **Turn your university's full timetable into your own personalized timetable — in seconds.**

A web application that helps university students generate a clean, personalized timetable from their official **Lecture, Lab, and Tutorial timetable files**.

Instead of manually searching through a large university timetable, simply upload the official timetable, enter your course codes, select the required sections/groups, and generate a ready-to-use PDF timetable.

---

## 🚀 Live Demo

### 👉 [Open Student Timetable Generator](https://student-timetable-generator.streamlit.app/)

No installation required — open the application, upload your timetable file, select your courses, and generate your personalized timetable.

---

## ✨ Features

- 📚 **Lecture Timetable Generation**
- 🧪 **Lab & Tutorial Timetable Generation**
- 📅 **Complete Timetable Generation**
- ➕ **Add Lab & Tutorial schedules to an existing Lecture timetable**
- 🔎 **Course-code based timetable matching**
- ♾️ **No fixed course limit**
- 🔀 **Automatic section handling**
- 👥 **Lab and Tutorial group selection**
- ⚠️ **Timetable conflict detection**
- 📄 **Clean A4 PDF generation**
- 📤 Supports **XLSX, XLSM, PDF, and CSV** timetable files
- 🏷️ Includes relevant **course, type, section, group, room, and schedule details**
- 🔒 University timetable files are **not included in this public repository**

---

## 🧠 How It Works

### 1️⃣ Upload Your Official Timetable

Upload the timetable provided by your university.

The application supports:

- Lecture timetable
- Lab & Tutorial timetable
- Existing generated Lecture timetable

---

### 2️⃣ Enter Your Course Codes

Enter the course codes you want to include in your personal timetable.

The course input fields automatically expand as you add courses.

---

### 3️⃣ Select Sections & Groups

If a course has multiple sections or groups, the application asks you to select the appropriate one.

Where possible, a common section or group selection can be reused across applicable courses.

---

### 4️⃣ Check for Conflicts

The application checks the selected schedules for overlapping time periods and reports timetable conflicts.

---

### 5️⃣ Generate Your Timetable

The application creates a clean weekly timetable containing the selected:

- Lectures
- Labs
- Tutorials

with their relevant schedule and room information.

---

### 6️⃣ Download Your PDF

Your personalized timetable is generated as a clean PDF that can be:

- 💾 Saved
- 🖨️ Printed
- 📱 Viewed on your phone
- 📤 Shared with others

---

## 📋 Timetable Modes

| Mode | Description |
|---|---|
| 📚 **Lecture Timetable Only** | Generate only lecture schedules |
| 🧪 **Lab & Tutorial Timetable Only** | Generate only labs and tutorials |
| 📅 **Complete Timetable** | Combine lectures, labs, and tutorials |
| ➕ **Add Lab & Tutorial** | Add labs and tutorials to an existing lecture timetable |

---

## 🔎 Course-Code Matching

The application uses a **conservative course-code matching approach** to avoid incorrectly assigning activities.

### Exact Match

If the requested course code exists directly in the uploaded timetable, it is matched automatically.

### Different Course Code

A different course code is **never silently assumed to represent the same course**.

If a possible matching course is found, the application asks the user to explicitly confirm whether it represents the same course.

This helps prevent incorrect Lab or Tutorial schedules from being added to a timetable.

---

## 📁 Supported Input Formats

The application supports the following timetable file formats:

```text
.xlsx
.xlsm
.pdf
.csv
