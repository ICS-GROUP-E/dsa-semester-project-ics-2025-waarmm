import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, filedialog
import os, sys, csv

# Add paths to custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ds')))

from src.ds.hashtable_patients import HashTable, Patient
from src.database.db_connection import (
    insert_patient_to_db,
    delete_patient_from_db,
    get_all_patients,
    init_db,
)

class PatientTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # DB setup
        init_db()
        self.hashtable = HashTable()
        for row in get_all_patients():
            self.hashtable.addPatient(Patient(*row))

        self.create_widgets()
        self.log("Hospital Management System Started")
        self.log("=====================================")
        self.log("Ready to start managing patient records")


    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Form Section ---
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="x", padx=50, pady=10)
        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="HOSPITAL MANAGEMENT SYSTEM", style='Title.TLabel')\
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.entry_id = self._make_entry(form_frame, "Patient ID: ", 1)
        self.entry_name = self._make_entry(form_frame, "Name: ", 2)
        self.entry_age = self._make_entry(form_frame, "Age: ", 3)
        self.entry_condition = self._make_entry(form_frame, "Condition: ", 4)

        # --- Buttons Section ---
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        for i in range(3): buttons_frame.columnconfigure(i, weight=1)

        self._make_button(buttons_frame, "Add Patient", self.add_patient, '#27ae60', '#2ecc71', 0, 0)
        self._make_button(buttons_frame, "Search Patient", self.search_patient, '#3498db', '#5dade2', 0, 1)
        self._make_button(buttons_frame, "Delete Patient", self.delete_patient, '#e74c3c', '#ec7063', 0, 2)
        self._make_button(buttons_frame, "Display All", self.display_all_patients, '#9b59b6', '#bb8fce', 1, 0)
        self._make_button(buttons_frame, "Clear Fields", self.clear_entries, '#f39c12', '#f8c471', 1, 1)
        self._make_button(buttons_frame, "Clear Log", self.clear_log, '#95a5a6', '#aeb6bf', 1, 2)
        self._make_button(buttons_frame, "Export CSV Report", self.export_to_csv, '#34495e', '#5d6d7e', 2, 0, columnspan=3)

        # --- Log Section ---
        output_frame = tk.Frame(main_frame, bg="#fff", relief='raised', bd=2)
        output_frame.pack(fill='both', expand=True)

        tk.Label(output_frame, text="System Log", bg="#fff").pack(fill="x", pady=(15, 10))

        self.output_box = scrolledtext.ScrolledText(output_frame, width=80, height=20,
                                                    bg='#2c3e50', fg='#ecf0f1', relief='flat', wrap=tk.WORD)
        self.output_box.pack(padx=20, pady=(0, 20), fill='both', expand=True)


    def _make_entry(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky='e', padx=5, pady=5)
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5, ipady=5)
        return entry


    def _make_button(self, parent, text, command, bg_color, hover_color, row, col, columnspan=1):
        btn = tk.Button(parent, text=text, command=command, bg=bg_color, fg='white',
                        font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=20, pady=10,
                        cursor='hand2', activebackground=hover_color, activeforeground='white')

        btn.original_color = bg_color
        btn.hover_color = hover_color
        btn.bind("<Enter>", lambda e: e.widget.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=bg_color))
        btn.grid(row=row, column=col, columnspan=columnspan, padx=8, pady=8, sticky='ew')
        return btn


    def log(self, msg):
        self.output_box.insert(tk.END, msg + "\n")
        self.output_box.see(tk.END)


    def clear_entries(self):
        for entry in [self.entry_id, self.entry_name, self.entry_age, self.entry_condition]:
            entry.delete(0, tk.END)


    def clear_log(self):
        self.output_box.delete(1.0, tk.END)
        self.log("Log cleared")


    def add_patient(self):
        id, name, age, condition = [e.get().strip() for e in [self.entry_id, self.entry_name, self.entry_age, self.entry_condition]]
        if not all([id, name, age, condition]):
            messagebox.showerror("❌ Error", "All fields are required!")
            return
        try:
            age_int = int(age)
            if age_int < 0: raise ValueError()
        except ValueError:
            messagebox.showerror("❌ Error", "Age must be a positive integer!")
            return
        patient = Patient(id, name, age, condition)
        if self.hashtable.addPatient(patient):
            insert_patient_to_db(patient)
            self.log(f"✅ SUCCESS: Added patient {name} (ID: {id})")
            self.clear_entries()
            messagebox.showinfo("✅ Success", f"Patient {name} added successfully!")
        else:
            self.log(f"⚠ WARNING: Patient with ID {id} already exists")
            messagebox.showwarning("⚠ Warning", f"Patient with ID {id} already exists!")


    def search_patient(self):
        id = self.entry_id.get().strip()
        if not id:
            messagebox.showerror("❌ Error", "Please enter a Patient ID to search!")
            return
        patient = self.hashtable.getPatient(id)
        if patient:
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.entry_age.delete(0, tk.END)
            self.entry_condition.delete(0, tk.END)
            self.entry_id.insert(0, patient.id)
            self.entry_name.insert(0, patient.name)
            self.entry_age.insert(0, patient.age)
            self.entry_condition.insert(0, patient.condition)
            self.log(f"✅ SUCCESS: Found patient {patient.name} (ID: {id})")
        else:
            self.log(f"❌ NOT FOUND: Patient ID {id} does not exist")
            messagebox.showinfo("Search Result", f"Patient ID {id} not found!")


    def delete_patient(self):
        id = self.entry_id.get().strip()
        if not id:
            messagebox.showerror("❌ Error", "Please enter a Patient ID to delete!")
            return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient ID {id}?"):
            if self.hashtable.removePatient(id):
                delete_patient_from_db(id)
                self.clear_entries()
                self.log(f"✅ SUCCESS: Deleted patient ID {id}")
                messagebox.showinfo("✅ Success", f"Patient ID {id} deleted successfully!")
            else:
                self.log(f"❌ ERROR: Failed to delete patient ID {id}")
                messagebox.showerror("❌ Error", f"Patient ID {id} not found!")


    def display_all_patients(self):
        self.output_box.delete(1.0, tk.END)
        patients = get_all_patients()
        if not patients:
            self.log("No patients found in the database")
        else:
            self.log("ALL PATIENTS:\n" + "="*33)
            for index, p in enumerate(patients):
                self.log(f"{index:2d}. ID: {p[0]:<8} | Name: {p[1]:<12} | Age: {p[2]:<3} | Condition: {p[3]}")
            self.log("="*33)
            self.log(f"Count: {len(patients)}")


    def export_to_csv(self):
        patients = get_all_patients()
        if not patients:
            self.log("⚠ No patients to export")
            messagebox.showwarning("No Data", "There are no patients to export.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            self.log("Export cancelled by user.")
            return
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Patient ID", "Name", "Age", "Condition"])
                writer.writerows(patients)
            self.log(f"📁 Exported patient data to {filename}")
            messagebox.showinfo("✅ Exported", f"Patient data exported to:\n{filename}")
        except Exception as e:
            self.log(f"❌ Error exporting CSV: {e}")
            messagebox.showerror("❌ Export Failed", f"Could not export data: {e}")