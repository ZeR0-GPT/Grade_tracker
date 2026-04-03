import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import create_tables
from students import add_student, get_all_students, delete_student
from grades import add_grade, get_grades_by_student, get_average, get_top_students

# ── colours ──────────────────────────────────────────────
BG       = "#f9f9f9"
WHITE    = "#ffffff"
ACCENT   = "#4f7ef7"
TEXT     = "#1a1a1a"
MUTED    = "#6b7280"
SUCCESS  = "#16a34a"
WARNING  = "#d97706"
DANGER   = "#dc2626"
BORDER   = "#e5e7eb"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Grade Tracker")
        self.geometry("820x600")
        self.configure(bg=BG)
        self.resizable(True, True)
        create_tables()
        self._build_sidebar()
        self._build_main()
        self.show_dashboard()

    # ── sidebar ──────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=WHITE, width=180,
                                highlightbackground=BORDER,
                                highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Grade Tracker", bg=WHITE,
                 fg=TEXT, font=("Helvetica", 14, "bold"),
                 pady=20).pack()

        self.nav_btns = {}
        for label, cmd in [("Dashboard",    self.show_dashboard),
                            ("Students",     self.show_students),
                            ("Add Grade",    self.show_add_grade),
                            ("Report",       self.show_report)]:
            btn = tk.Button(self.sidebar, text=label, bg=WHITE, fg=MUTED,
                            relief="flat", anchor="w", padx=20, pady=10,
                            font=("Helvetica", 11), cursor="hand2",
                            command=cmd)
            btn.pack(fill="x")
            self.nav_btns[label] = btn

    def _set_active(self, label):
        for name, btn in self.nav_btns.items():
            if name == label:
                btn.configure(bg="#eff4ff", fg=ACCENT,
                              font=("Helvetica", 11, "bold"))
            else:
                btn.configure(bg=WHITE, fg=MUTED,
                              font=("Helvetica", 11))

    # ── main area ────────────────────────────────────────
    def _build_main(self):
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _header(self, title, subtitle=""):
        tk.Label(self.main, text=title, bg=BG, fg=TEXT,
                 font=("Helvetica", 18, "bold")).pack(anchor="w",
                 padx=24, pady=(24, 2))
        if subtitle:
            tk.Label(self.main, text=subtitle, bg=BG, fg=MUTED,
                     font=("Helvetica", 11)).pack(anchor="w", padx=24)

    def _card(self, parent=None, **kwargs):
        p = parent or self.main
        f = tk.Frame(p, bg=WHITE, highlightbackground=BORDER,
                     highlightthickness=1, **kwargs)
        return f

    # ── badge helper ─────────────────────────────────────
    def _badge(self, parent, avg):
        if avg is None:
            return
        if avg >= 75:
            color, text = SUCCESS, "Good"
        elif avg >= 50:
            color, text = WARNING, "Average"
        else:
            color, text = DANGER, "Needs work"
        tk.Label(parent, text=text, bg=color, fg=WHITE,
                 font=("Helvetica", 9, "bold"),
                 padx=8, pady=2).pack(side="right", padx=4)

    # ── DASHBOARD ────────────────────────────────────────
    def show_dashboard(self):
        self._clear_main()
        self._set_active("Dashboard")
        self._header("Dashboard", "Overview of all students")

        students = get_all_students()
        top = get_top_students()
        all_avgs = [r[1] for r in top]
        class_avg = round(sum(all_avgs) / len(all_avgs), 1) if all_avgs else None

        # metric cards
        metrics_frame = tk.Frame(self.main, bg=BG)
        metrics_frame.pack(fill="x", padx=24, pady=16)
        for label, value in [("Total Students", len(students)),
                              ("Class Average",  class_avg if class_avg else "—"),
                              ("Top Score",      max(all_avgs) if all_avgs else "—")]:
            c = self._card(metrics_frame, padx=16, pady=12)
            c.pack(side="left", expand=True, fill="both", padx=(0, 8))
            tk.Label(c, text=label, bg=WHITE, fg=MUTED,
                     font=("Helvetica", 10)).pack(anchor="w")
            tk.Label(c, text=str(value), bg=WHITE, fg=TEXT,
                     font=("Helvetica", 22, "bold")).pack(anchor="w")

        # student list
        card = self._card(padx=16, pady=12)
        card.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        tk.Label(card, text="All Students", bg=WHITE, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w",
                 pady=(0, 8))

        if not students:
            tk.Label(card, text="No students yet — add one in the Students tab.",
                     bg=WHITE, fg=MUTED,
                     font=("Helvetica", 11)).pack(pady=20)
        else:
            for s in students:
                avg = get_average(s[0])
                row = tk.Frame(card, bg=WHITE)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=s[1], bg=WHITE, fg=TEXT,
                         font=("Helvetica", 11)).pack(side="left")
                avg_text = f"{avg}" if avg else "No grades"
                tk.Label(row, text=avg_text, bg=WHITE, fg=MUTED,
                         font=("Helvetica", 11)).pack(side="right", padx=8)
                self._badge(row, avg)

    # ── STUDENTS ─────────────────────────────────────────
    def show_students(self):
        self._clear_main()
        self._set_active("Students")
        self._header("Students", "Add or remove students")

        # add form
        card = self._card(padx=16, pady=12)
        card.pack(fill="x", padx=24, pady=16)
        tk.Label(card, text="Add a student", bg=WHITE, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w",
                 pady=(0, 8))
        row = tk.Frame(card, bg=WHITE)
        row.pack(fill="x")
        name_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=name_var, font=("Helvetica", 11),
                         relief="solid", bd=1, width=30)
        entry.pack(side="left", ipady=5, padx=(0, 8))
        msg_var = tk.StringVar()

        def do_add():
            n = name_var.get().strip()
            if not n:
                return
            add_student(n)
            name_var.set("")
            msg_var.set(f"{n} added!")
            self.after(2000, lambda: msg_var.set(""))
            self.show_students()

        tk.Button(row, text="Add", bg=ACCENT, fg=WHITE,
                  relief="flat", padx=16, pady=5,
                  font=("Helvetica", 11), cursor="hand2",
                  command=do_add).pack(side="left")
        tk.Label(card, textvariable=msg_var, bg=WHITE,
                 fg=SUCCESS, font=("Helvetica", 10)).pack(anchor="w",
                 pady=(6, 0))

        # roster
        card2 = self._card(padx=16, pady=12)
        card2.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        tk.Label(card2, text="Student roster", bg=WHITE, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w",
                 pady=(0, 8))
        students = get_all_students()
        if not students:
            tk.Label(card2, text="No students yet.",
                     bg=WHITE, fg=MUTED,
                     font=("Helvetica", 11)).pack(pady=20)
        else:
            for s in students:
                row2 = tk.Frame(card2, bg=WHITE)
                row2.pack(fill="x", pady=4)
                tk.Label(row2, text=s[1], bg=WHITE, fg=TEXT,
                         font=("Helvetica", 11)).pack(side="left")
                tk.Button(row2, text="Delete", bg=DANGER, fg=WHITE,
                          relief="flat", padx=8, pady=2,
                          font=("Helvetica", 9), cursor="hand2",
                          command=lambda sid=s[0]: [delete_student(sid),
                                                    self.show_students()]
                          ).pack(side="right")

    # ── ADD GRADE ────────────────────────────────────────
    def show_add_grade(self):
        self._clear_main()
        self._set_active("Add Grade")
        self._header("Add Grade", "Record a grade for a student")

        card = self._card(padx=16, pady=16)
        card.pack(fill="x", padx=24, pady=16)

        students = get_all_students()
        student_names = [s[1] for s in students]
        student_ids   = [s[0] for s in students]

        fields = {}

        def labeled_entry(label, var):
            tk.Label(card, text=label, bg=WHITE, fg=MUTED,
                     font=("Helvetica", 10)).pack(anchor="w", pady=(8, 2))
            e = tk.Entry(card, textvariable=var,
                         font=("Helvetica", 11),
                         relief="solid", bd=1)
            e.pack(fill="x", ipady=5)
            return e

        tk.Label(card, text="Student", bg=WHITE, fg=MUTED,
                 font=("Helvetica", 10)).pack(anchor="w", pady=(8, 2))
        student_var = tk.StringVar()
        combo = ttk.Combobox(card, textvariable=student_var,
                             values=student_names, state="readonly",
                             font=("Helvetica", 11))
        combo.pack(fill="x", ipady=4)

        subject_var = tk.StringVar()
        grade_var   = tk.StringVar()
        date_var    = tk.StringVar(value=str(date.today()))
        labeled_entry("Subject", subject_var)
        labeled_entry("Grade (0–100)", grade_var)
        labeled_entry("Date", date_var)

        msg_var = tk.StringVar()

        def do_add():
            if not student_var.get():
                messagebox.showwarning("Missing", "Please select a student.")
                return
            try:
                g = float(grade_var.get())
                assert 0 <= g <= 100
            except:
                messagebox.showwarning("Invalid", "Grade must be 0–100.")
                return
            idx = student_names.index(student_var.get())
            sid = student_ids[idx]
            add_grade(sid, subject_var.get().strip(), g, date_var.get())
            subject_var.set("")
            grade_var.set("")
            msg_var.set("Grade saved!")
            self.after(2000, lambda: msg_var.set(""))

        tk.Button(card, text="Save grade", bg=ACCENT, fg=WHITE,
                  relief="flat", padx=16, pady=6,
                  font=("Helvetica", 11), cursor="hand2",
                  command=do_add).pack(anchor="w", pady=(16, 4))
        tk.Label(card, textvariable=msg_var, bg=WHITE,
                 fg=SUCCESS, font=("Helvetica", 10)).pack(anchor="w")

    # ── REPORT ───────────────────────────────────────────
    def show_report(self):
        self._clear_main()
        self._set_active("Report")
        self._header("Report", "View grades for a student")

        students = get_all_students()
        student_names = [s[1] for s in students]
        student_ids   = [s[0] for s in students]

        top_card = self._card(padx=16, pady=12)
        top_card.pack(fill="x", padx=24, pady=16)

        tk.Label(top_card, text="Select student", bg=WHITE, fg=MUTED,
                 font=("Helvetica", 10)).pack(anchor="w", pady=(0, 4))
        student_var = tk.StringVar()
        combo = ttk.Combobox(top_card, textvariable=student_var,
                             values=student_names, state="readonly",
                             font=("Helvetica", 11))
        combo.pack(fill="x", ipady=4)

        result_frame = tk.Frame(self.main, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=24)

        def load_report(event=None):
            for w in result_frame.winfo_children():
                w.destroy()
            if not student_var.get():
                return
            idx = student_names.index(student_var.get())
            sid = student_ids[idx]
            sg  = get_grades_by_student(sid)
            avg = get_average(sid)

            if not sg:
                tk.Label(result_frame,
                         text="No grades recorded for this student yet.",
                         bg=BG, fg=MUTED,
                         font=("Helvetica", 11)).pack(pady=20)
                return

            # metrics
            mf = tk.Frame(result_frame, bg=BG)
            mf.pack(fill="x", pady=(0, 12))
            highest = max(r[2] for r in sg)
            for label, val in [("Average", avg),
                                ("Highest", highest),
                                ("Subjects", len(sg))]:
                c = self._card(mf, padx=12, pady=10)
                c.pack(side="left", expand=True, fill="both", padx=(0, 8))
                tk.Label(c, text=label, bg=WHITE, fg=MUTED,
                         font=("Helvetica", 10)).pack(anchor="w")
                tk.Label(c, text=str(val), bg=WHITE, fg=TEXT,
                         font=("Helvetica", 20, "bold")).pack(anchor="w")

            # grade breakdown
            card = self._card(result_frame, padx=16, pady=12)
            card.pack(fill="both", expand=True, pady=(0, 24))
            tk.Label(card, text="Grade breakdown", bg=WHITE, fg=TEXT,
                     font=("Helvetica", 12, "bold")).pack(anchor="w",
                     pady=(0, 8))
            for r in sg:
                row = tk.Frame(card, bg=WHITE)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=r[1], bg=WHITE, fg=TEXT,
                         font=("Helvetica", 11), width=16,
                         anchor="w").pack(side="left")
                # bar
                bar_bg = tk.Frame(row, bg=BORDER, height=8, width=200)
                bar_bg.pack(side="left", padx=8)
                bar_bg.pack_propagate(False)
                bar_w = int(r[2] / 100 * 200)
                bar_color = SUCCESS if r[2] >= 75 else (WARNING if r[2] >= 50 else DANGER)
                tk.Frame(bar_bg, bg=bar_color, height=8,
                         width=bar_w).place(x=0, y=0)
                tk.Label(row, text=f"{r[2]:.0f}", bg=WHITE, fg=TEXT,
                         font=("Helvetica", 11, "bold"),
                         width=4).pack(side="left")
                self._badge(row, r[2])

        combo.bind("<<ComboboxSelected>>", load_report)

if __name__ == "__main__":
    app = App()
    app.mainloop()