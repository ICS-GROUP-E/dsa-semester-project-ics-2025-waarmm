import tkinter as tk
from tkinter import messagebox, filedialog
import logging
import sys
import csv
import datetime
from pathlib import Path

from tkinter import ttk

# --- Path Setup ---
base_dir = Path(__file__).resolve().parent
ds_dir = base_dir.parent / 'ds'
db_dir = base_dir.parent / 'database'

sys.path.extend([str(ds_dir), str(db_dir)])

try:
    from bst_doctorlookup import Doctor, DoctorBST
except ImportError:
    print("Error: Could not import Doctor or DoctorBST from bst_doctorlookup.")
    sys.exit(1)

try:
    import bst_db_connection as db
except ImportError:
    print("Error: Could not import bst_db_connection.")
    sys.exit(1)

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class DoctorLookupTab(ttk.Frame):
    def _init_(self, parent):
        super()._init_(parent)

        self.result_listbox = None
        self.specialty_entry = None
        self.name_entry = None
        self.tree = DoctorBST()

        try:
            db.initialize_db()
            for name, specialty in db.fetch_all_doctors():
                self.tree.insertDoctor(Doctor(name, specialty))
            logging.info("Doctors loaded from database.")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            messagebox.showerror("Database Error", str(e))

        self.setup_ui()

    def setup_ui(self):

        self.configure(padding=20)

        # --- Main Frame ---
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True)

        # --- Entry Frame ---
        form_frame = tk.LabelFrame(main_frame, text="Doctor Info", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(form_frame, text="Name:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        tk.Label(form_frame, text="Specialty:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", pady=5, padx=5)

        self.name_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.specialty_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.specialty_entry.grid(row=1, column=1, pady=5, padx=5)

        # --- Button Frame ---
        button_frame = tk.LabelFrame(main_frame, text="Actions", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        button_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        btn_style = {"width": 16, "font": ("Segoe UI", 9)}
        tk.Button(button_frame, text="➕ Add Doctor", command=self.add_doctor, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="🔍 Search", command=self.search_doctor, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="✏ Update", command=self.update_doctor, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="❌ Delete", command=self.delete_doctor, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="📋 Show All", command=self.display_all, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="🧹 Clear Fields", command=self.clear_entries, **btn_style).pack(pady=2)
        tk.Button(button_frame, text="📄 Export CSV", command=self.export_csv, **btn_style).pack(pady=10)

        # --- Results ---
        result_frame = tk.LabelFrame(main_frame, text="Results", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        result_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.result_listbox = tk.Listbox(result_frame, width=85, height=15, font=("Consolas", 10))
        self.result_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_listbox.config(yscrollcommand=scrollbar.set)

        # --- Status Bar ---
        self.status_label = tk.Label(self, text="Ready", anchor="w", bg="#e0e0e0", font=("Segoe UI", 9))
        self.status_label.pack(fill="x")

        self.display_all()

    def update_status(self, message):
        self.status_label.config(text=message)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.specialty_entry.delete(0, tk.END)

    def add_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        if not name or not specialty:
            messagebox.showwarning("Input Error", "Name and Specialty are required.")
            return

        if self.tree.searchDoctor(name):
            messagebox.showwarning("Duplicate", f"Doctor '{name}' already exists.")
            return

        try:
            doctor = Doctor(name, specialty)
            self.tree.insertDoctor(doctor)
            db.insert_doctor_db(name, specialty)
            logging.info(f"Doctor '{name}' added.")
            self.display_all()
            self.clear_entries()
            self.update_status(f"Doctor '{name}' added.")
            messagebox.showinfo("Success", f"Doctor '{name}' added.")
        except Exception as e:
            logging.error(f"Add error: {e}")
            messagebox.showerror("Error", str(e))

    def search_doctor(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to search.")
            return
        try:
            doctor = self.tree.searchDoctor(name)
            self.result_listbox.delete(0, tk.END)
            if doctor:
                self.result_listbox.insert(tk.END, f"✅ Found: {doctor}")
                self.specialty_entry.delete(0, tk.END)
                self.specialty_entry.insert(0, doctor.specialty)
                self.update_status(f"Doctor '{name}' found.")
            else:
                self.result_listbox.insert(tk.END, f"❌ Doctor '{name}' not found.")
                self.update_status(f"Doctor '{name}' not found.")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

    def update_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        if not name or not specialty:
            messagebox.showwarning("Input Error", "Name and Specialty are required.")
            return

        if self.tree.updateDoctor(name, specialty):
            db.update_doctor_db(name, specialty)
            logging.info(f"Doctor '{name}' updated.")
            self.display_all()
            self.clear_entries()
            self.update_status(f"Doctor '{name}' updated.")
            messagebox.showinfo("Updated", f"Doctor '{name}' updated.")
        else:
            messagebox.showerror("Error", f"Doctor '{name}' not found.")

    def delete_doctor(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Enter a name to delete.")
            return

        if not self.tree.searchDoctor(name):
            messagebox.showerror("Error", f"Doctor '{name}' not found.")
            return

        if messagebox.askyesno("Confirm Delete", f"Delete Dr. {name}?"):
            self.tree.deleteDoctor(name)
            db.delete_doctor_db(name)
            logging.info(f"Doctor '{name}' deleted.")
            self.display_all()
            self.clear_entries()
            self.update_status(f"Doctor '{name}' deleted.")
            messagebox.showinfo("Deleted", f"Doctor '{name}' deleted.")

    def display_all(self):
        try:
            self.result_listbox.delete(0, tk.END)
            doctors = self.tree.inorderTraversal()
            if doctors:
                self.result_listbox.insert(tk.END, f"📋 Total Doctors: {len(doctors)}")
                self.result_listbox.insert(tk.END, "-" * 70)
                for doc in doctors:
                    self.result_listbox.insert(tk.END, str(doc))
                self.update_status(f"{len(doctors)} doctors displayed.")
            else:
                self.result_listbox.insert(tk.END, "No doctors found.")
                self.update_status("No doctors to display.")
        except Exception as e:
            messagebox.showerror("Display Error", str(e))

    def export_csv(self):
        try:
            doctors = self.tree.inorderTraversal()
            if not doctors:
                messagebox.showinfo("No Data", "There are no doctors to export.")
                return

            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"doctors_report_{now}.csv"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=default_filename
            )

            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Name", "Specialty"])
                    for doc in doctors:
                        writer.writerow([doc.name, doc.specialty])
                logging.info(f"Exported to {file_path}")
                self.update_status(f"Exported to {file_path}")
                messagebox.showinfo("Export Successful", f"Doctors exported to:\n{file_path}")
        except Exception as e:
            logging.error(f"Export Error: {e}")
            messagebox.showerror("Export Error", str(e))