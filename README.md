--📚 Student Grade Tracker

A desktop app built with Python to manage students and track their grades across subjects.





--Features

- Add and delete students
- Record grades per subject
- View each student's grade breakdown with a progress bar
- Dashboard with class average and top scores
- Student report with highest grade and subject summary

-- Tech Stack

- Python 3
- Tkinter (UI)
- SQLite3 (database)
- SQL (JOINs, AVG, GROUP BY)

-- How to Run

1. Make sure Python 3 is installed
2. Clone the repo
3. Go into the folder:
   cd student-grade-tracker
4. Run the app:
   python app.py

No extra installs needed — everything is built into Python!

-- Project Structure

- app.py        ➡️ Main UI (run this)
- database.py   ➡️  Database connection and table setup
- students.py   ➡️  Add, get, delete students
- grades.py     ➡️ Add grades, calculate averages, get reports
