import pandas as pd
import mysql.connector
import ast
import os
from dotenv import load_dotenv

# NOTE: Consider switching to batch inserts (executemany) instead of row-by-row 
# inserts if the dataset grows significantly larger than 100 students.
# Load database credentials from .env
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Load the cleaned dataset
df = pd.read_csv("data/students_clean.csv")

# The list-type columns were saved as text like "['Python', 'Java']"
# ast.literal_eval turns that text back into a real Python list
df["Technical Skills"] = df["Technical Skills"].apply(ast.literal_eval)
df["Preferred Domain(s)"] = df["Preferred Domain(s)"].apply(ast.literal_eval)

inserted_students = 0
inserted_skills = 0

for _, row in df.iterrows():
    # Insert into students table
    cursor.execute("""
        INSERT INTO students (
            full_name, email, roll_number, class_division, branch,
            preferred_domains, preferred_role, working_preference,
            availability, experience_level, prior_team_experience,
            leadership, communication, independence, creativity
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["Full Name"], row["Email Address"], row["Roll Number"],
        row["Class and Division"], row["Branch/Department"],
        ", ".join(row["Preferred Domain(s)"]), row["Preferred Role"],
        row["Working Preference"], row["Availability"],
        row["Overall Experience Level"], row["Prior Team Project Experience"],
        row["Leadership"], row["Communication"], row["Independence"], row["Creativity"]
    ))
    student_id = cursor.lastrowid
    inserted_students += 1

    # Insert each skill (if new) and link it to this student
    for skill in row["Technical Skills"]:
        cursor.execute("INSERT IGNORE INTO skills (skill_name) VALUES (%s)", (skill,))
        cursor.execute("SELECT skill_id FROM skills WHERE skill_name = %s", (skill,))
        skill_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT IGNORE INTO student_skills (student_id, skill_id) VALUES (%s, %s)",
            (student_id, skill_id)
        )
        inserted_skills += 1

conn.commit()
print(f"Inserted {inserted_students} students and {inserted_skills} skill links.")

cursor.close()
conn.close()