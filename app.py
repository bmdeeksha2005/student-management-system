from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Connect to database
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create students table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def index():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students
    )


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        conn = get_db()

        conn.execute("""
            INSERT INTO students
            (name, email, course, phone)
            VALUES (?, ?, ?, ?)
        """, (name, email, course, phone))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_student.html")


# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE students
            SET name = ?,
                email = ?,
                course = ?,
                phone = ?
            WHERE id = ?
        """, (name, email, course, phone, id))

        conn.commit()
        conn.close()

        return redirect("/")

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Run application
if __name__ == "__main__":

    create_table()

    app.run(debug=True)