import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    gender TEXT,
    phone TEXT,
    disease TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1000x650")
root.configure(bg="#f4f6f8")


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)

title.pack(fill="x")


# ---------------- NOTEBOOK ----------------

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=15)


# ==================================================
# DOCTOR TAB
# ==================================================

doctor_tab = tk.Frame(notebook, bg="white")
notebook.add(doctor_tab, text="  Doctors  ")


tk.Label(
    doctor_tab,
    text="Doctor Management",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=15)


doctor_frame = tk.Frame(doctor_tab, bg="white")
doctor_frame.pack()


tk.Label(doctor_frame, text="Doctor Name:", bg="white").grid(
    row=0, column=0, padx=10, pady=10
)

doctor_name = tk.Entry(doctor_frame, width=30)
doctor_name.grid(row=0, column=1)


tk.Label(doctor_frame, text="Specialization:", bg="white").grid(
    row=1, column=0, padx=10, pady=10
)

specialization = tk.Entry(doctor_frame, width=30)
specialization.grid(row=1, column=1)


tk.Label(doctor_frame, text="Phone:", bg="white").grid(
    row=2, column=0, padx=10, pady=10
)

doctor_phone = tk.Entry(doctor_frame, width=30)
doctor_phone.grid(row=2, column=1)


def add_doctor():

    name = doctor_name.get()
    spec = specialization.get()
    phone = doctor_phone.get()

    if name == "" or spec == "":
        messagebox.showwarning(
            "Warning",
            "Please enter doctor details"
        )
        return

    cursor.execute(
        "INSERT INTO doctors(name, specialization, phone) VALUES (?, ?, ?)",
        (name, spec, phone)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Doctor added successfully"
    )

    doctor_name.delete(0, tk.END)
    specialization.delete(0, tk.END)
    doctor_phone.delete(0, tk.END)

    show_doctors()


tk.Button(
    doctor_frame,
    text="Add Doctor",
    command=add_doctor,
    bg="#1f4e78",
    fg="white",
    width=20
).grid(row=3, column=1, pady=15)


doctor_table = ttk.Treeview(
    doctor_tab,
    columns=("ID", "Name", "Specialization", "Phone"),
    show="headings"
)

doctor_table.heading("ID", text="ID")
doctor_table.heading("Name", text="Doctor Name")
doctor_table.heading("Specialization", text="Specialization")
doctor_table.heading("Phone", text="Phone")

doctor_table.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


def show_doctors():

    for row in doctor_table.get_children():
        doctor_table.delete(row)

    cursor.execute("SELECT * FROM doctors")

    for row in cursor.fetchall():
        doctor_table.insert("", tk.END, values=row)


show_doctors()


# ==================================================
# PATIENT TAB
# ==================================================

patient_tab = tk.Frame(notebook, bg="white")
notebook.add(patient_tab, text="  Patients  ")


tk.Label(
    patient_tab,
    text="Patient Management",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=15)


patient_frame = tk.Frame(patient_tab, bg="white")
patient_frame.pack()


tk.Label(patient_frame, text="Patient Name:", bg="white").grid(
    row=0, column=0, padx=10, pady=8
)

patient_name = tk.Entry(patient_frame, width=30)
patient_name.grid(row=0, column=1)


tk.Label(patient_frame, text="Age:", bg="white").grid(
    row=1, column=0, padx=10, pady=8
)

patient_age = tk.Entry(patient_frame, width=30)
patient_age.grid(row=1, column=1)


tk.Label(patient_frame, text="Gender:", bg="white").grid(
    row=2, column=0, padx=10, pady=8
)

patient_gender = ttk.Combobox(
    patient_frame,
    values=["Male", "Female", "Other"],
    width=27
)

patient_gender.grid(row=2, column=1)


tk.Label(patient_frame, text="Phone:", bg="white").grid(
    row=3, column=0, padx=10, pady=8
)

patient_phone = tk.Entry(patient_frame, width=30)
patient_phone.grid(row=3, column=1)


tk.Label(patient_frame, text="Disease:", bg="white").grid(
    row=4, column=0, padx=10, pady=8
)

patient_disease = tk.Entry(patient_frame, width=30)
patient_disease.grid(row=4, column=1)


def add_patient():

    name = patient_name.get()
    age = patient_age.get()
    gender = patient_gender.get()
    phone = patient_phone.get()
    disease = patient_disease.get()

    if name == "":
        messagebox.showwarning(
            "Warning",
            "Please enter patient name"
        )
        return

    cursor.execute(
        """
        INSERT INTO patients
        (name, age, gender, phone, disease)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, age, gender, phone, disease)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Patient added successfully"
    )

    patient_name.delete(0, tk.END)
    patient_age.delete(0, tk.END)
    patient_gender.set("")
    patient_phone.delete(0, tk.END)
    patient_disease.delete(0, tk.END)

    show_patients()


tk.Button(
    patient_frame,
    text="Add Patient",
    command=add_patient,
    bg="#1f4e78",
    fg="white",
    width=20
).grid(row=5, column=1, pady=15)


patient_table = ttk.Treeview(
    patient_tab,
    columns=("ID", "Name", "Age", "Gender", "Phone", "Disease"),
    show="headings"
)

for column in ("ID", "Name", "Age", "Gender", "Phone", "Disease"):
    patient_table.heading(column, text=column)

patient_table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


def show_patients():

    for row in patient_table.get_children():
        patient_table.delete(row)

    cursor.execute("SELECT * FROM patients")

    for row in cursor.fetchall():
        patient_table.insert("", tk.END, values=row)


show_patients()


# ==================================================
# APPOINTMENT TAB
# ==================================================

appointment_tab = tk.Frame(notebook, bg="white")
notebook.add(appointment_tab, text="  Appointments  ")


tk.Label(
    appointment_tab,
    text="Appointment Management",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=20)


appointment_frame = tk.Frame(
    appointment_tab,
    bg="white"
)

appointment_frame.pack()


tk.Label(
    appointment_frame,
    text="Patient Name:",
    bg="white"
).grid(row=0, column=0, padx=10, pady=10)


appointment_patient = tk.Entry(
    appointment_frame,
    width=30
)

appointment_patient.grid(row=0, column=1)


tk.Label(
    appointment_frame,
    text="Doctor Name:",
    bg="white"
).grid(row=1, column=0, padx=10, pady=10)


appointment_doctor = tk.Entry(
    appointment_frame,
    width=30
)

appointment_doctor.grid(row=1, column=1)


tk.Label(
    appointment_frame,
    text="Date:",
    bg="white"
).grid(row=2, column=0, padx=10, pady=10)


appointment_date = tk.Entry(
    appointment_frame,
    width=30
)

appointment_date.grid(row=2, column=1)


tk.Label(
    appointment_frame,
    text="Time:",
    bg="white"
).grid(row=3, column=0, padx=10, pady=10)


appointment_time = tk.Entry(
    appointment_frame,
    width=30
)

appointment_time.grid(row=3, column=1)


def book_appointment():

    patient = appointment_patient.get()
    doctor = appointment_doctor.get()
    date = appointment_date.get()
    time = appointment_time.get()

    if patient == "" or doctor == "":
        messagebox.showwarning(
            "Warning",
            "Enter patient and doctor"
        )
        return

    cursor.execute(
        """
        INSERT INTO appointments
        (patient, doctor, date, time)
        VALUES (?, ?, ?, ?)
        """,
        (patient, doctor, date, time)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Appointment booked successfully"
    )

    appointment_patient.delete(0, tk.END)
    appointment_doctor.delete(0, tk.END)
    appointment_date.delete(0, tk.END)
    appointment_time.delete(0, tk.END)

    show_appointments()


tk.Button(
    appointment_frame,
    text="Book Appointment",
    command=book_appointment,
    bg="#1f4e78",
    fg="white",
    width=20
).grid(row=4, column=1, pady=15)


appointment_table = ttk.Treeview(
    appointment_tab,
    columns=("ID", "Patient", "Doctor", "Date", "Time"),
    show="headings"
)

for column in ("ID", "Patient", "Doctor", "Date", "Time"):
    appointment_table.heading(column, text=column)

appointment_table.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


def show_appointments():

    for row in appointment_table.get_children():
        appointment_table.delete(row)

    cursor.execute("SELECT * FROM appointments")

    for row in cursor.fetchall():
        appointment_table.insert("", tk.END, values=row)


show_appointments()


# ---------------- RUN ----------------

root.mainloop()

conn.close()