from fastapi import FastAPI, HTTPException
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MatchCrewAI API")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.get("/")
def read_root():
    return {"message": "MatchCrewAI backend is running"}

@app.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:
        cursor.execute("""
            SELECT sk.skill_name
            FROM student_skills ss
            JOIN skills sk ON ss.skill_id = sk.skill_id
            WHERE ss.student_id = %s
        """, (student["student_id"],))
        skills = cursor.fetchall()
        student["skills"] = [s["skill_name"] for s in skills]

    cursor.close()
    conn.close()
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.execute("""
        SELECT sk.skill_name
        FROM student_skills ss
        JOIN skills sk ON ss.skill_id = sk.skill_id
        WHERE ss.student_id = %s
    """, (student_id,))
    skills = cursor.fetchall()
    student["skills"] = [s["skill_name"] for s in skills]

    cursor.close()
    conn.close()
    return student