from database import create_connection

def add_student(name):
    conn = create_connection()
    conn.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = create_connection()
    cursor = conn.execute("SELECT * FROM students ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_student(student_id):
    conn = create_connection()
    conn.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()