from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)

DB_PATH = Path("data/attendance.db")


def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            UNIQUE(student_id, attendance_date),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/students")
def get_students():
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM students ORDER BY roll_no"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.post("/api/students")
def add_student():
    data = request.get_json() or {}

    roll_no = data.get("roll_no", "").strip()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not roll_no or not name:
        return jsonify({
            "error": "Roll number and name are required."
        }), 400

    conn = get_db()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students (roll_no, name, email)
            VALUES (?, ?, ?)
            """,
            (roll_no, name, email)
        )

        conn.commit()
        student_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conn.close()

        return jsonify({
            "error": "Roll number already exists."
        }), 409

    conn.close()

    return jsonify({
        "message": "Student registered successfully.",
        "id": student_id
    }), 201


@app.post("/api/attendance")
def mark_attendance():
    data = request.get_json() or {}

    student_id = data.get("student_id")
    attendance_date = (
        data.get("attendance_date")
        or date.today().isoformat()
    )
    status = data.get("status")

    if not student_id or status not in ["Present", "Absent"]:
        return jsonify({
            "error": "Student and valid attendance status are required."
        }), 400

    conn = get_db()

    conn.execute(
        """
        INSERT INTO attendance
        (student_id, attendance_date, status)
        VALUES (?, ?, ?)

        ON CONFLICT(student_id, attendance_date)
        DO UPDATE SET status = excluded.status
        """,
        (student_id, attendance_date, status)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Attendance saved successfully."
    })


@app.get("/api/records")
def get_records():
    selected_date = request.args.get("date")

    conn = get_db()

    if selected_date:

        rows = conn.execute(
            """
            SELECT
                a.attendance_date,
                s.roll_no,
                s.name,
                a.status
            FROM attendance a
            JOIN students s
            ON s.id = a.student_id
            WHERE a.attendance_date = ?
            ORDER BY s.roll_no
            """,
            (selected_date,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT
                a.attendance_date,
                s.roll_no,
                s.name,
                a.status
            FROM attendance a
            JOIN students s
            ON s.id = a.student_id
            ORDER BY
                a.attendance_date DESC,
                s.roll_no
            """
        ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.get("/api/summary")
def attendance_summary():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            s.id,
            s.roll_no,
            s.name,
            COUNT(a.id) AS total,
            COALESCE(
                SUM(
                    CASE
                        WHEN a.status = 'Present'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS present

        FROM students s

        LEFT JOIN attendance a
        ON a.student_id = s.id

        GROUP BY s.id

        ORDER BY s.roll_no
        """
    ).fetchall()

    conn.close()

    result = []

    for row in rows:

        total = row["total"]
        present = row["present"]

        percentage = (
            round((present / total) * 100, 2)
            if total > 0
            else 0
        )

        result.append({
            "id": row["id"],
            "roll_no": row["roll_no"],
            "name": row["name"],
            "total": total,
            "present": present,
            "percentage": percentage
        })

    return jsonify(result)


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )