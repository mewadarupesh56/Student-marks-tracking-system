"""
Student Academic Performance Tracker
CLI Application for Managing Student Records and Subject Marks
"""

import csv
import db

MINIMUM_PASSING_PERCENTAGE = 40.0


def determine_grade(percentage_score):
    """Maps numerical percentage to corresponding letter grades."""
    grade_thresholds = [
        (90, "O"),
        (80, "A+"),
        (70, "A"),
        (60, "B"),
        (50, "C"),
        (MINIMUM_PASSING_PERCENTAGE, "D"),
    ]
    for threshold, letter_grade in grade_thresholds:
        if percentage_score >= threshold:
            return letter_grade
    return "F"


def prompt_non_empty_string(user_prompt):
    """Prompts user for text input and validates that it is non-empty."""
    while True:
        user_input = input(user_prompt).strip()
        if user_input:
            return user_input
        print("  Error: Input field cannot be left blank.")


def prompt_numeric_value(user_prompt, min_limit=0, max_limit=None):
    """Prompts for a numeric value within specified boundaries."""
    while True:
        try:
            numeric_input = float(input(user_prompt).strip())
        except ValueError:
            print("  Error: Please enter a valid numerical value.")
            continue

        if numeric_input < min_limit or (max_limit is not None and numeric_input > max_limit):
            upper_bound_text = f"{max_limit}" if max_limit is not None else "no upper bound"
            print(f"  Error: Value must range between {min_limit} and {upper_bound_text}.")
            continue

        return numeric_input


def calculate_percentage(marks_obtained, total_marks):
    """Calculates percentage based on marks obtained vs total maximum marks."""
    if not total_marks:
        return 0.0
    return (marks_obtained / total_marks) * 100


def register_new_student():
    """Handles adding a new student to the database."""
    roll_number = prompt_non_empty_string("Enter Roll Number: ")
    student_name = prompt_non_empty_string("Enter Full Name: ")
    academic_course = prompt_non_empty_string("Enter Course/Branch: ")

    if db.add_student(roll_number, student_name, academic_course):
        print("Success: Student registered successfully.")
    else:
        print("Error: A student record with this roll number already exists.")


def record_subject_marks():
    """Records or updates marks for a specific subject."""
    roll_number = prompt_non_empty_string("Enter Roll Number: ")
    if not db.get_student(roll_number):
        print("Error: No student record found matching this roll number.")
        return

    subject_title = prompt_non_empty_string("Enter Subject Name: ").title()
    max_score = prompt_numeric_value("Enter Maximum Marks: ", min_limit=1)
    score_obtained = prompt_numeric_value("Enter Marks Obtained: ", min_limit=0, max_limit=max_score)

    db.set_marks(roll_number, subject_title, score_obtained, max_score)
    print("Success: Academic marks saved successfully.")


def delete_subject_marks():
    """Removes recorded marks for a specific subject."""
    roll_number = prompt_non_empty_string("Enter Roll Number: ")
    subject_title = prompt_non_empty_string("Enter Subject Name to Remove: ").title()

    if db.delete_marks(roll_number, subject_title):
        print("Success: Subject entry removed.")
    else:
        print("Error: Specified subject entry not found.")


def delete_student_record():
    """Deletes a student record entirely from the system."""
    roll_number = prompt_non_empty_string("Enter Roll Number to Delete: ")
    if db.delete_student(roll_number):
        print("Success: Student record deleted.")
    else:
        print("Error: No student record found matching this roll number.")


def display_all_students():
    """Displays a list of all registered students."""
    student_records = db.list_students()
    if not student_records:
        print("Notice: No student records found in the database.")
        return

    print(f"\n{'Roll No':<15}{'Student Name':<25}{'Course/Branch'}")
    print("=" * 55)
    for roll, name, course in student_records:
        print(f"{roll:<15}{name:<25}{course}")


def generate_report_card():
    """Generates and displays a consolidated academic performance report card."""
    roll_number = prompt_non_empty_string("Enter Roll Number: ")
    student_info = db.get_student(roll_number)

    if not student_info:
        print("Error: No student record found matching this roll number.")
        return

    marks_data = db.get_marks(roll_number)
    print(f"\n--- ACADEMIC REPORT CARD ---")
    print(f"Name: {student_info[1]} | Roll No: {student_info[0]} | Course: {student_info[2]}")

    if not marks_data:
        print("Notice: No subject scores recorded for this student yet.")
        return

    print(f"\n{'Subject Name':<22}{'Obtained':>10}{'Max':>8}{'Percentage':>12}{'Grade':>8}")
    print("-" * 60)

    cumulative_obtained = 0.0
    cumulative_maximum = 0.0
    has_failed_subject = False

    for subject, got_marks, max_marks in marks_data:
        subject_pct = calculate_percentage(got_marks, max_marks)
        if subject_pct < MINIMUM_PASSING_PERCENTAGE:
            has_failed_subject = True

        grade = determine_grade(subject_pct)
        print(f"{subject:<22}{got_marks:>10.1f}{max_marks:>8.1f}{subject_pct:>11.1f}%{grade:>8}")

        cumulative_obtained += got_marks
        cumulative_maximum += max_marks

    overall_pct = calculate_percentage(cumulative_obtained, cumulative_maximum)
    final_result = "FAIL" if has_failed_subject else "PASS"

    print("-" * 60)
    print(f"Total Marks: {cumulative_obtained:.1f}/{cumulative_maximum:.1f}  |  "
          f"Overall: {overall_pct:.2f}%  |  Status: {final_result}")


def show_class_rankings():
    """Calculates and renders class ranking based on overall percentages."""
    ranking_data = []
    for roll, name, got_marks, max_marks in db.class_totals():
        if max_marks:
            percentage = calculate_percentage(got_marks, max_marks)
            ranking_data.append((roll, name, got_marks, max_marks, percentage))

    if not ranking_data:
        print("Notice: Insufficient evaluation data to compute class rankings.")
        return

    # Sort descending by calculated percentage
    ranking_data.sort(key=lambda item: item[4], reverse=True)

    print(f"\n{'Rank':<6}{'Roll No':<15}{'Student Name':<25}{'Overall %':>10}")
    print("=" * 58)
    for rank, (roll, name, _, _, score_pct) in enumerate(ranking_data, start=1):
        print(f"{rank:<6}{roll:<15}{name:<25}{score_pct:>9.2f}%")


def display_subject_statistics():
    """Displays subject-wise average, lowest, and highest percentage statistics."""
    stats_records = db.subject_stats()
    if not stats_records:
        print("Notice: No evaluation records available to build statistics.")
        return

    print(f"\n{'Subject Name':<22}{'Average %':>10}{'Highest %':>10}{'Lowest %':>10}{'Entries':>8}")
    print("=" * 62)
    for subject, avg_val, high_val, low_val, total_entries in stats_records:
        print(f"{subject:<22}{avg_val:>9.1f}%{high_val:>9.1f}%{low_val:>9.1f}%{total_entries:>8}")


def export_records_to_csv():
    """Exports all student marks data into an external CSV spreadsheet."""
    export_filename = "marks_export.csv"
    with db.connect() as connection, open(export_filename, "w", newline="", encoding="utf-8") as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(["Roll Number", "Student Name", "Course", "Subject Title", "Marks Obtained", "Max Marks"])

        fetch_query = """
            SELECT s.roll_no, s.name, s.course, m.subject, m.obtained, m.maximum
            FROM students s 
            JOIN marks m ON s.roll_no = m.roll_no
            ORDER BY s.roll_no ASC, m.subject ASC
        """
        file_writer.writerows(connection.execute(fetch_query))

    print(f"Success: Data export finished. File created at '{export_filename}'.")


# Menu map linking menu option descriptions to execution handlers
ACTION_MENU = [
    ("Add New Student", register_new_student),
    ("Enter or Modify Marks", record_subject_marks),
    ("List All Students", display_all_students),
    ("Generate Report Card", generate_report_card),
    ("View Class Rankings", show_class_rankings),
    ("View Subject Statistics", display_subject_statistics),
    ("Delete Specific Marks Entry", delete_subject_marks),
    ("Remove Student Record", delete_student_record),
    ("Export Data to CSV", export_records_to_csv),
]


def main():
    """Main execution loop for CLI navigation."""
    db.init_db()

    while True:
        print("\n" + "=" * 12 + " STUDENT TRACKING SYSTEM " + "=" * 12)
        for idx, (label, _) in enumerate(ACTION_MENU, start=1):
            print(f" {idx}. {label}")
        print(" 0. Exit Application")

        user_choice = input("\nSelect an action [0-9]: ").strip()

        if user_choice == "0":
            print("Exiting application. Have a great day!")
            break

        if user_choice.isdigit() and 1 <= int(user_choice) <= len(ACTION_MENU):
            # Execute mapped handler function
            ACTION_MENU[int(user_choice) - 1][1]()
        else:
            print("Invalid selection. Please enter a valid menu number.")


if __name__ == "__main__":
    main()