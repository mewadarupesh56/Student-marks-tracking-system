# Student Marks Tracking System

A command-line application, written in Python, for recording and analysing
student marks. Data is stored in a local SQLite database.

## Features

- Add and delete students
- Enter or update marks subject by subject (with validation)
- Report card with percentage, letter grade and pass/fail result
- Class ranking by overall percentage
- Subject-wise average, highest and lowest marks
- Export all records to a CSV file

## Project structure

```
marks_tracker/
├── main.py            # menu and user interaction
├── db.py              # all database code (SQLite)
├── requirements.txt
├── README.md
└── REPORT.md          # project report
```

## Requirements

Python 3.8 or newer. No external libraries are needed.

## How to run

```bash
cd marks_tracker
python main.py
```

The database file `marks.db` is created automatically on first run.

## Grading scale

| Percentage | Grade |
|-----------|-------|
| 90+       | O     |
| 80-89     | A+    |
| 70-79     | A     |
| 60-69     | B     |
| 50-59     | C     |
| 40-49     | D     |
| below 40  | F     |

A student fails if any subject is below 40%. Change `PASS_PERCENT` and
`grade_for()` in `main.py` to use your college's scale.

## Sample session

```
=== Student Marks Tracking System ===
 1. Add student
 ...
Choose an option: 1
Roll number: 101
Name: Asha
Course/Branch: BCA
Student added.
```

## Author

NAME :RUPESH KUMAR        REGISTRATION NO. :26MIM10180         COURSE NAME :M.tech integrated course COLLEGE NAME:VIT BHOPAL UNIVERSITY.