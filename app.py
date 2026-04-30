from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import config
from mysql.connector.errors import IntegrityError

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# MySQL Configuration
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)

# Home route (updated to include instructor info)
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT c.*, i.name AS instructor_name
        FROM Courses c
        LEFT JOIN Instructors i ON c.instructor_id = i.instructor_id
    ''')
    courses = cur.fetchall()
    cur.close()
    return render_template('index.html', courses=courses)

# Enroll route (updated to handle new student logic)
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        email = request.form.get('email')
        course_id = request.form.get('course_id')
        semester = request.form.get('semester')
        cur = mysql.connection.cursor()

        try:
            # Check if student exists
            cur.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
            student = cur.fetchone()

            # ==== New Student Logic ====
            if not student:
                if not name or not email:
                    flash('Name and email are required for new students', 'danger')
                    return redirect(url_for('enroll'))

                # Create new student
                cur.execute(
                    "INSERT INTO Students (student_id, name, email) VALUES (%s, %s, %s)",
                    (student_id, name, email)
                )
                mysql.connection.commit()
                flash(f'New student {name} created!', 'success')

            # ==== Enrollment Logic ====
            try:
                cur.execute(
                    "INSERT INTO Enrollments (student_id, course_id, semester) VALUES (%s, %s, %s)",
                    (student_id, course_id, semester)
                )
                mysql.connection.commit()
                flash('Enrollment successful!', 'success')
            except IntegrityError:
                flash('This enrollment already exists!', 'warning')
            except Exception as e:
                mysql.connection.rollback()
                flash(f'Error: {str(e)}', 'danger')

        finally:
            cur.close()

        return redirect(url_for('home'))

    # GET request handling remains the same
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()
    cur.close()
    return render_template('enroll.html', courses=courses)

# Students route (existing)
@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Students")
    students = cur.fetchall()
    cur.close()
    return render_template('students.html', students=students)

# My Courses route (existing)
@app.route('/my_courses/<int:student_id>')
def my_courses(student_id):
    cur = mysql.connection.cursor()

    # Get student details
    cur.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    student = cur.fetchone()

    # Get enrolled courses
    cur.execute('''
        SELECT Courses.title, Courses.credits, Enrollments.semester
        FROM Enrollments
        JOIN Courses ON Enrollments.course_id = Courses.course_id
        WHERE student_id = %s
    ''', (student_id,))
    enrolled_courses = cur.fetchall()
    cur.close()

    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('home'))

    return render_template(
        'my_courses.html',
        student=student,
        courses=enrolled_courses
    )

# New route for instructors
@app.route('/instructors')
def instructors():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT i.instructor_id, i.name, i.email, d.name AS department_name, 
               GROUP_CONCAT(c.title SEPARATOR ', ') AS courses_taught
        FROM Instructors i
        LEFT JOIN Departments d ON i.department_id = d.department_id
        LEFT JOIN Courses c ON i.instructor_id = c.instructor_id
        GROUP BY i.instructor_id
    ''')
    instructors = cur.fetchall()
    cur.close()
    return render_template('instructors.html', instructors=instructors)

# Route to check if a student exists (AJAX request)
@app.route('/check-student/<int:student_id>')
def check_student(student_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT name, email FROM Students WHERE student_id = %s", (student_id,))
        student = cur.fetchone()

        return jsonify({
            'exists': bool(student),
            'name': student[0] if student else '',
            'email': student[1] if student else ''
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(debug=True)
