
import streamlit as st
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("opd.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            date TEXT,
            time TEXT,
            reason TEXT,
            diagnosis TEXT,
            prescription TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect("opd.db")

def register_patient(name, age, gender, phone, address):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
              (name, age, gender, phone, address))
    conn.commit()
    conn.close()

def list_patients():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return patients

def add_appointment(patient_id, date, time, reason, diagnosis, prescription):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO appointments (patient_id, date, time, reason, diagnosis, prescription) VALUES (?, ?, ?, ?, ?, ?)",
              (patient_id, date, time, reason, diagnosis, prescription))
    conn.commit()
    conn.close()

def list_appointments():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''SELECT a.id, p.name, a.date, a.time, a.reason, a.diagnosis, a.prescription 
                 FROM appointments a 
                 JOIN patients p ON a.patient_id = p.id 
                 ORDER BY a.date DESC''')
    appts = c.fetchall()
    conn.close()
    return appts

# UI
init_db()
st.title("🩺 Simple OPD Management System")

menu = ["Register Patient", "Add Appointment", "View Appointments"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register Patient":
    st.subheader("Register New Patient")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone")
    address = st.text_area("Address")

    if st.button("Register"):
        register_patient(name, age, gender, phone, address)
        st.success(f"Patient '{name}' registered successfully!")

elif choice == "Add Appointment":
    st.subheader("Schedule Appointment")
    patients = list_patients()
    patient_map = {f"{p[0]} - {p[1]}": p[0] for p in patients}

    patient_sel = st.selectbox("Select Patient", list(patient_map.keys()))
    pid = patient_map[patient_sel]
    date = st.date_input("Date")
    time = st.time_input("Time")
    reason = st.text_input("Reason for Visit")
    diagnosis = st.text_input("Diagnosis")
    prescription = st.text_area("Prescription (e.g. Vati BID A/F)")

    if st.button("Add Appointment"):
        add_appointment(pid, date.strftime('%Y-%m-%d'), time.strftime('%H:%M'), reason, diagnosis, prescription)
        st.success("Appointment added successfully!")

elif choice == "View Appointments":
    st.subheader("All Appointments")
    data = list_appointments()
    st.table(data)
