import tkinter as tk
from tkinter import ttk

from src.ui.doctorlookup_ui import DoctorLookupTab
from src.ui.medication_ui import MedicationTab
from src.ui.patient_ui import PatientTab
from src.ui.priorityQueueUI import PriorityQueueTab
from src.ui.queue_appointments_ui import AppointmentTab

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hospital Management System")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Add patient record tab
    patient_tab = PatientTab(notebook)
    notebook.add(patient_tab, text="Patient Records")

    # Add priority queue tab
    priority_queue_tab = PriorityQueueTab(notebook)
    notebook.add(priority_queue_tab, text="Priority Queue")

    medication_tab = MedicationTab(notebook)
    notebook.add(medication_tab, text="Medication History")

    doctor_lookup_tab = DoctorLookupTab(notebook)
    notebook.add(doctor_lookup_tab, text="Doctor Lookup")

    appointment_tab = AppointmentTab(notebook)
    notebook.add(appointment_tab, text="Appointments")

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('1000x700')

    root.mainloop()