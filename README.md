# 🎓 Student Timetable Generator

A Streamlit application that turns university lecture, lab and tutorial timetables into a clean personalized timetable PDF.

## Highlights

- Lecture-only timetable generation
- Lab & tutorial-only generation
- Combined lecture + lab + tutorial timetable
- Add newly released lab/tutorial schedules to an existing generated lecture PDF
- Course-code fields that add the next field automatically as you enter courses
- Automatic lecture section handling
- Automatic Lab/Tutorial group detection from the uploaded timetable
- Persistent Lab Group and Tutorial Group selections across courses
- Conflict detection for overlapping classes
- Automatic PDF title and filename based on the source timetable
- Excel, PDF and CSV input support

## How it works

1. Upload the timetable files currently available from your university.
2. Select the required timetable mode.
3. Enter course codes (or let the existing lecture PDF provide them).
4. Select a lecture section, Lab Group and/or Tutorial Group when required.
5. The application combines the relevant classes into one weekly timetable.
6. Download the generated PDF.

## Important association rule

Some universities publish practicals under a separate course code. The application therefore never assumes that similar-looking codes are the same course. It first uses an exact course-code match from the uploaded Lab/Tutorial timetable. If no exact match exists, it may suggest plausible activity codes (for example, CT304 for lecture code CT303), but the student must explicitly confirm the relationship. If the student says they are different courses, no activity is added. This prevents incorrect assumptions such as treating CT101 and CT102 as the same course.

## Run locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Project structure

```text
student-timetable-generator/
├── app.py
├── core.py
├── requirements.txt
├── README.md
├── run.bat
└── install_and_run.bat
```

## Privacy

No university timetable files or personal timetable files are included in this repository. Users upload their own timetable files at runtime.
