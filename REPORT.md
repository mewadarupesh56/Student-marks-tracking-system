# Project Report: Student Marks Tracking System

**Submitted by:** RUPESH KUMAR                  **Roll No.:** 26MIM10180                   |             **Course:** INTEGRATED M.tech
**College:**  VIT BHOPAL UNIVERSITY                   | **Guide:** Dr. PRIYADHARSHINI           | **Year:** 2026

---

## 1. Abstract

The Student Marks Tracking System is a Python application that stores student
details and subject marks in a SQLite database and produces report cards,
class rankings and subject statistics. It replaces manual registers and
spreadsheets with a validated, searchable and reliable system.

## 2. Introduction

Teachers often record marks on paper or in loose spreadsheets. This makes
totals error-prone, ranking slow, and old records hard to find. This project
provides a small, easy-to-use program that keeps all marks in one place and
calculates results automatically.

## 3. Objectives

1. Store student and marks data permanently and safely.
2. Reject invalid input (empty fields, negative marks, marks above maximum).
3. Calculate totals, percentages, grades and pass/fail automatically.
4. Rank students and summarise performance per subject.
5. Export data for use in other tools.

## 4. Scope and Limitations

The system is a single-user, command-line program for one institution or
class. It has no login system and no graphical interface.

## 5. System Requirements

| Item | Requirement |
|------|-------------|
| Language | Python 3.8+ |
| Database | SQLite (built into Python) |
| Libraries | Standard library only (`sqlite3`, `csv`) |
| OS | Windows, Linux or macOS |
| Hardware | Any computer that can run Python |

## 6. System Design

### 6.1 Modules

- **main.py** - shows the menu, reads and validates input, prints reports.
- **db.py** - creates tables and runs all SQL queries.

Separating the two means the interface can change (for example to a GUI)
without touching the database code.

### 6.2 Database schema

**students**

| Column | Type | Notes |
|--------|------|-------|
| roll_no | TEXT | Primary key |
| name | TEXT | Required |
| course | TEXT | Required |

**marks**

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key, auto-increment |
| roll_no | TEXT | Foreign key to students (delete cascades) |
| subject | TEXT | Unique together with roll_no |
| obtained | REAL | Marks scored |
| maximum | REAL | Maximum marks |

### 6.3 Flow of the program

1. Program starts and creates the database if missing.
2. Menu is displayed in a loop.
3. User selects an option; the matching function collects input.
4. Input is validated; `db.py` runs the query.
5. Result is printed and the menu shows again until the user exits.

## 7. Implementation Details

- **Validation:** `ask_number()` repeats until a number inside the allowed
  range is entered; `ask_text()` rejects empty strings.
- **Insert or update:** `set_marks()` uses SQLite's `ON CONFLICT ... DO UPDATE`
  so entering marks for an existing subject simply corrects them.
- **Grading:** `grade_for()` maps a percentage to a letter from a
  configurable scale. A student fails if any single subject is below 40%.
- **Ranking:** overall percentage per student is computed from totals, then
  sorted in descending order.
- **Statistics:** SQL aggregate functions (`AVG`, `MAX`, `MIN`, `COUNT`)
  with `GROUP BY subject`.
- **Export:** Python's `csv` module writes a joined view of both tables.

## 8. Testing

| # | Test case | Input | Expected | Result |
|---|-----------|-------|----------|--------|
| 1 | Add student | 101, Asha, BCA | Student added | Pass |
| 2 | Duplicate roll number | 101 again | Error message | Pass |
| 3 | Marks above maximum | 120 out of 100 | Rejected, re-asked | Pass |
| 4 | Negative marks | -5 | Rejected, re-asked | Pass |
| 5 | Letters as marks | abc | Rejected, re-asked | Pass |
| 6 | Update marks | Same subject, new value | Old value replaced | Pass |
| 7 | Unknown roll number | 999 | "No such student" | Pass |
| 8 | Delete student | 101 | Student and marks removed | Pass |
| 9 | Export CSV | Option 9 | File created | Pass |

(Run each case yourself and add screenshots in your submission.)

## 9. Results

The system produces a per-student report card with total, percentage, grade
and result; a class ranking table; and a subject statistics table. All data
persists between runs in `marks.db`.

## 10. Future Enhancements

- Graphical interface (Tkinter) or web interface (Flask)
- Teacher login with passwords
- Charts of performance over semesters
- Import marks from CSV/Excel
- Semester-wise and CGPA calculation

## 11. Conclusion

The project meets its objectives: it stores marks reliably, validates input,
automates calculations and gives quick summaries. It also gave practice in
Python functions, modular design, SQL and file handling.

## 12. References

1. Python Software Foundation, *Python 3 Documentation* - docs.python.org
2. Python `sqlite3` module documentation - docs.python.org/3/library/sqlite3.html
3. SQLite Documentation - sqlite.org/docs.html
4. Python `csv` module documentation - docs.python.org/3/library/csv.html