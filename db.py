"""
Database Access Layer for Student Records and Academic Evaluation
Engineered using SQLite3 with Foreign Key constraints enabled.
"""

import sqlite3

DATABASE_FILENAME = "marks.db"


def get_db_connection():
    """Establishes and returns an active SQLite connection with Foreign Keys enabled."""
    connection = sqlite3.connect(DATABASE_FILENAME)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def init_db():
    """Initializes schema tables if they do not already exist."""
    schema_script = """
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name    TEXT NOT NULL,
            course  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS marks (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no   TEXT NOT NULL,
            subject   TEXT NOT NULL,
            obtained  REAL NOT NULL,
            maximum   REAL NOT NULL,
            CONSTRAINT unique_student_subject UNIQUE (roll_no, subject),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
        );
    """
    with get_db_connection() as conn:
        conn.executescript(schema_script)


# Main code compatibility aliases
connect = get_db_connection


def add_student(roll_number, full_name, branch_course):
    """Inserts a new student record into the database."""
    query_str = "INSERT INTO students (roll_no, name, course) VALUES (?, ?, ?)"
    try:
        with get_db_connection() as conn:
            conn.execute(query_str, (roll_number, full_name, branch_course))
        return True
    except sqlite3.IntegrityError:
        return False


def get_student(roll_number):
    """Fetches a single student record matching the specified roll number."""
    query_str = "SELECT roll_no, name, course FROM students WHERE roll_no = ?"
    with get_db_connection() as conn:
        cursor = conn.execute(query_str, (roll_number,))
        return cursor.fetchone()


def list_students():
    """Retrieves all registered student records ordered by roll number."""
    query_str = "SELECT roll_no, name, course FROM students ORDER BY roll_no ASC"
    with get_db_connection() as conn:
        return conn.execute(query_str).fetchall()


def delete_student(roll_number):
    """Deletes a student record (and cascades deletion to associated marks)."""
    query_str = "DELETE FROM students WHERE roll_no = ?"
    with get_db_connection() as conn:
        cursor = conn.execute(query_str, (roll_number,))
        return cursor.rowcount > 0


def set_marks(roll_number, subject_title, score_obtained, score_max):
    """Inserts a new mark entry or updates existing subject score on conflict."""
    upsert_query = """
        INSERT INTO marks (roll_no, subject, obtained, maximum)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(roll_no, subject)
        DO UPDATE SET 
            obtained = excluded.obtained,
            maximum  = excluded.maximum
    """
    with get_db_connection() as conn:
        conn.execute(upsert_query, (roll_number, subject_title, score_obtained, score_max))


def get_marks(roll_number):
    """Fetches all subject scores for a specific student."""
    query_str = """
        SELECT subject, obtained, maximum 
        FROM marks 
        WHERE roll_no = ? 
        ORDER BY subject ASC
    """
    with get_db_connection() as conn:
        return conn.execute(query_str, (roll_number,)).fetchall()


def delete_marks(roll_number, subject_title):
    """Removes subject marks for a given student."""
    query_str = "DELETE FROM marks WHERE roll_no = ? AND subject = ?"
    with get_db_connection() as conn:
        cursor = conn.execute(query_str, (roll_number, subject_title))
        return cursor.rowcount > 0


def class_totals():
    """Calculates overall aggregate marks and total possible marks for each student."""
    aggregate_query = """
        SELECT 
            s.roll_no, 
            s.name,
            COALESCE(SUM(m.obtained), 0) AS total_obtained,
            COALESCE(SUM(m.maximum), 0) AS total_max
        FROM students s 
        LEFT JOIN marks m ON s.roll_no = m.roll_no
        GROUP BY s.roll_no, s.name 
        ORDER BY s.roll_no ASC
    """
    with get_db_connection() as conn:
        return conn.execute(aggregate_query).fetchall()


def subject_stats():
    """Computes subject performance analytics: Average percentage, Highest, Lowest, Entry Count."""
    stats_query = """
        SELECT 
            subject,
            AVG((obtained * 100.0) / maximum) AS avg_percentage,
            MAX(obtained) AS highest_score,
            MIN(obtained) AS lowest_score,
            COUNT(*) AS total_records
        FROM marks 
        GROUP BY subject 
        ORDER BY subject ASC
    """
    with get_db_connection() as conn:
        return conn.execute(stats_query).fetchall()