from database import create_connection

def add_grade(student_id, subject, grade, date):
    conn = create_connection()
    conn.execute("INSERT INTO grades (student_id, subject, grade, date) VALUES (?, ?, ?, ?)",
                 (student_id, subject, grade, date))
    conn.commit()
    conn.close()

def get_grades_by_student(student_id):
    conn = create_connection()
    cursor = conn.execute('''
        SELECT students.name, grades.subject, grades.grade, grades.date
        FROM grades
        JOIN students ON grades.student_id = students.id
        WHERE students.id = ?
        ORDER BY grades.grade DESC
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_average(student_id):
    conn = create_connection()
    cursor = conn.execute('''
        SELECT AVG(grade) FROM grades WHERE student_id = ?
    ''', (student_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else None

def get_top_students():
    conn = create_connection()
    cursor = conn.execute('''
        SELECT students.name, ROUND(AVG(grades.grade), 2) as average
        FROM grades
        JOIN students ON grades.student_id = students.id
        GROUP BY students.id
        ORDER BY average DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows