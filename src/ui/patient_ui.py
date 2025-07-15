# Imports
import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import csv
# Add this import at the top if not already present:
from tkinter import filedialog



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ds')))

from ..ds.hashtable_patients import HashTable, Patient
from ..database.db_connection import (
    insert_patient_to_db,
    delete_patient_from_db,
    get_all_patients,
    init_db,
)

# Initialize DB and hash table
init_db()
hashtable = HashTable()


# Load existing database entries into the hashtable
for row in get_all_patients():
    patient = Patient(*row) 
    hashtable.addPatient(patient)


# Function to log to output box
def log(msg):
    output_box.insert(tk.END, msg + "\n")
    output_box.see(tk.END)
    root.update_idletasks()


# Add patient 
def add_patient():
    id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()
    condition = entry_condition.get()

    if not(id and name and age and condition):
        messagebox.showerror("❌ Error", "All fields are required!")
        return
    
    # Check if age is valid (age must be positive)
    try:
        age_int = int(age)
        if age_int < 0:
            raise ValueError("Age must be positive")
    except ValueError:
        messagebox.showerror("❌ Error", "Please enter a valid age!")
        return
    
    # Create patient
    patient = Patient(id, name, age, condition)

    # Add patient to hash table and consequently, the database
    if hashtable.addPatient(patient):
        insert_patient_to_db(patient)
        log(f"✅ SUCCESS: Added patient {name} (ID: {id})")
        clear_entries()
        messagebox.showinfo("✅ Success", f"Patient {name} added successfully!")

    else:
        # Patient already exists
        log(f"⚠️ WARNING: Patient with ID {id} already exists")
        messagebox.showwarning("⚠️ Warning", f"Patient with ID {id} already exists!")


# Search patient
def search_patient():
    id = entry_id.get().strip()
    if not id:
        messagebox.showerror("❌ Error", "Please enter a Patient ID to search!")
        return
    
    patient = hashtable.getPatient(id)
    if patient:
        log(f"✅ SUCCESS: Found patient {patient.name} (ID: {id})")

        # Populate fields with result
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_condition.delete(0, tk.END)

        entry_id.insert(0, patient.id)
        entry_name.insert(0, patient.name)
        entry_age.insert(0, patient.age)
        entry_condition.insert(0, patient.condition)

    # No patient found
    else: 
        log(f"❌ NOT FOUND: Patient ID {id} does not exist")
        messagebox.showinfo("Search Result", f"Patient ID {id} not found!")


# Delete patient
def delete_patient():
    id = entry_id.get().strip()
    if not id:
        messagebox.showerror("❌ Error", "Please enter a Patient ID to delete!")
        return
    
    # Confirm delete
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient ID {id}?"):
        if hashtable.removePatient(id):
            delete_patient_from_db(id)
            log(f"✅ SUCCESS: Deleted patient ID {id}")
            clear_entries()
            messagebox.showinfo("✅ Success", f"Patient ID {id} deleted successfully!")

        else:
            log(f"❌ ERROR: Failed to delete patient ID {id}")
            messagebox.showerror("❌ Error", f"Patient ID {id} not found!")


# Display all patients
def display_all_patients():
    output_box.delete(1.0, tk.END)
    patients = get_all_patients()
    if not patients:
        log("No patients found in the database")
    else:
        log("ALL PATIENTS:")
        log("=================================")

        for index, patient in enumerate(patients):
            log(f"{index:2d}. ID: {patient[0]:<8} | Name: {patient[1]:<12} | Age: {patient[2]:<3} | Condition: {patient[3]}")

        log("=================================")
        log(f"Count: {len(patients)}")


# Export patients to CSV
def export_to_csv():
    patients = get_all_patients()
    if not patients:
        log("⚠️ No patients to export")
        messagebox.showwarning("No Data", "There are no patients to export.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Patient Report As"
    )

    if not filename:
        log("Export cancelled by user.")
        return  # User cancelled the dialog

    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Patient ID", "Name", "Age", "Condition"])
            for patient in patients:
                writer.writerow(patient)
        log(f"📁 Exported patient data to {filename}")
        messagebox.showinfo("✅ Exported", f"Patient data exported to:\n{filename}")
    except Exception as e:
        log(f"❌ Error exporting CSV: {e}")
        messagebox.showerror("❌ Export Failed", f"Could not export data: {e}")


# Clear log button functionality
def clear_log():
    output_box.delete(1.0, tk.END)
    log("Log cleared")


# Clear fields
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_condition.delete(0, tk.END)


# Button hover effects
def on_enter(e):
    e.widget['background'] = e.widget.hover_color

def on_leave(e):
    e.widget['background'] = e.widget.original_color


# Create styled button function
def create_styled_button(parent, text, command, bg_color, hover_color, row, column, columnspan=1):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg='white',
        font=('Arial', 10, 'bold'),
        relief='flat',
        bd=0,
        padx=20,
        pady=10,
        cursor='hand2',
        activebackground=hover_color,
        activeforeground='white'
    )
    
    # Store colors for hover effect
    button.original_color = bg_color
    button.hover_color = hover_color
    
    # Bind hover events
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    button.grid(row=row, column=column, columnspan=columnspan, padx=8, pady=8, sticky='ew')
    return button


# GUI setup
root = tk.Tk()
root.title("Hospital Management System")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)


# -- Form Section --

# Form frame
form_frame = tk.Frame(main_frame)
form_frame.pack(fill="x", padx=50, pady=10)

form_frame.columnconfigure(0, weight=0)
form_frame.columnconfigure(1, weight=1)

# Form title
title_label = ttk.Label(form_frame, text="HOSPITAL MANAGEMENT SYSTEM", style='Title.TLabel')
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# PatientID
lbl_id = tk.Label(form_frame, text="Patient ID: ")
lbl_id.grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_id = tk.Entry(form_frame)
entry_id.grid(row=1, column=1, sticky='ew', padx=5, pady=5, ipady=5)

# Name
lbl_name = tk.Label(form_frame, text="Name: ")
lbl_name.grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_name = tk.Entry(form_frame)
entry_name.grid(row=2, column=1, sticky='ew', padx=5, pady=5, ipady=5)

# Age
lbl_age = tk.Label(form_frame, text="Age: ")
lbl_age.grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry_age = tk.Entry(form_frame)
entry_age.grid(row=3, column=1, sticky='ew', padx=5, pady=5, ipady=5)

# Condition
lbl_condition = tk.Label(form_frame, text="Condition: ")
lbl_condition.grid(row=4, column=0, sticky='e', padx=5, pady=5)
entry_condition = tk.Entry(form_frame)
entry_condition.grid(row=4, column=1, sticky='ew', padx=5, pady=5, ipady=5)

# -- Buttons section --

# Buttons frame
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(fill="x", padx=10, pady=10)

for i in range(3):
    buttons_frame.columnconfigure(i, weight=1)

# Add patient button
btn_add_patient = create_styled_button(buttons_frame, "Add Patient", add_patient, '#27ae60', '#2ecc71', 0, 0)


# Search patient button
btn_search_patient = create_styled_button(buttons_frame, "Search Patient", search_patient, '#3498db', '#5dade2', 0, 1)


# Delete patient button
btn_delete_patient = create_styled_button(buttons_frame, "Delete Patient", delete_patient, '#e74c3c', '#ec7063', 0, 2)


# Dipslay all patients button
btn_display_all_patients = create_styled_button(buttons_frame, "Display All", display_all_patients, '#9b59b6', '#bb8fce', 1, 0)


# Clear fields button
btn_clear_fields = create_styled_button(buttons_frame, "Clear Fields", clear_entries, '#f39c12', '#f8c471', 1, 1)


# Clear log button
btn_clear_log = create_styled_button(buttons_frame, "Clear Log", clear_log, '#95a5a6', '#aeb6bf', 1, 2)

# Export CSV Report button
btn_export_csv = create_styled_button(buttons_frame, "Export CSV Report", export_to_csv, '#34495e', '#5d6d7e', 2, 0, columnspan=3)

# --- Log section --- 

# Output Frame
output_frame = tk.Frame(main_frame, bg="#fff", relief='raised', bd=2)
output_frame.pack(fill='both', expand=True)

# Output section title
output_title = tk.Label(output_frame, text="System Log", bg="#fff")
output_title.pack(fill="x", pady=(15, 10))

# Output box
output_box = scrolledtext.ScrolledText(
    output_frame, 
    width=80, 
    height=20, 
    bg='#2c3e50',
    fg='#ecf0f1',
    relief='flat',
    wrap=tk.WORD
)

output_box.pack(padx=20, pady=(0, 20), fill='both', expand=True)

# Initial startup messages
log("Hospital Management System Started")
log("=====================================")
log("Ready to start managing patient records")

# Center window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')


root.mainloop()