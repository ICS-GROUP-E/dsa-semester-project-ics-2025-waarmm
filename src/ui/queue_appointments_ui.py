import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import csv
import datetime
from tkinter import ttk
import os

from src.ds.queue_appointments import AppointmentQueue


class AppointmentTab(ttk.Frame):
    def _init_(self, parent):
        super()._init_(parent)
        self.log_box = None
        self.queue_listbox = None
        self.name_entry = None
        self.queue = AppointmentQueue()
        self.arrival_order = []  # [(name, timestamp)]

        self.setup_ui()

    def setup_ui(self):

        # --- UI Frames ---
        top_frame = tk.Frame(self, padx=20, pady=10)
        top_frame.pack(fill="x")

        btn_frame = tk.Frame(self, padx=20, pady=10)
        btn_frame.pack(fill="x")

        list_frame = tk.Frame(self, padx=20, pady=10)
        list_frame.pack(fill="both", expand=True)

        log_frame = tk.Frame(self, padx=20, pady=10)
        log_frame.pack(fill="both", expand=True)

        # --- Top Input ---
        tk.Label(top_frame, text="Patient Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(top_frame, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Button(top_frame, text="➕ Add Patient", bg="#27ae60", fg="white",
                  command=self.add_patient).grid(row=0, column=2, padx=10)

        tk.Button(top_frame, text="⏭ Serve Next", bg="#e67e22", fg="white",
                  command=self.serve_patient).grid(row=0, column=3, padx=10)

        # --- Buttons ---
        tk.Button(btn_frame, text="⬇ Export Queue to CSV", bg="#34495e", fg="white",
                  command=self.export_to_csv).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="🧹 Clear Console", bg="#95a5a6", fg="black",
                  command=self.clear_console).grid(row=0, column=1, padx=5)

        # --- Queue Display ---
        tk.Label(list_frame, text="🧑‍⚕ Current Queue:").pack(anchor="w")
        self.queue_listbox = tk.Listbox(list_frame, height=8, font=('Courier', 10))
        self.queue_listbox.pack(fill="both", expand=True, pady=(0, 10))

        # --- Console Log ---
        tk.Label(log_frame, text="📜 Console Log:").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(log_frame, height=10, bg="#2c3e50", fg="#ecf0f1")
        self.log_box.pack(fill="both", expand=True)

        self.update_display()

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def add_patient(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a patient name.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.queue.enqueue(name)
        self.arrival_order.append((name, timestamp))
        self.name_entry.delete(0, tk.END)

        self.log(f"✅ Added: {name} at {timestamp}")
        self.update_display()

    def serve_patient(self):
        served = self.queue.dequeue()
        if served:
            self.arrival_order = [entry for entry in self.arrival_order if entry[0] != served]
            self.log(f"🚑 Served: {served}")
            self.update_display()
        else:
            messagebox.showinfo("Queue Empty", "No patients to serve.")
            self.log("⚠ Tried to serve, but queue was empty.")

    def update_display(self):
        self.queue_listbox.delete(0, tk.END)
        for i, (name, timestamp) in enumerate(self.arrival_order, start=1):
            entry = f"{i:>2}. {name:<20} Time: {timestamp}"
            self.queue_listbox.insert(tk.END, entry)

    def export_to_csv(self):
        if not self.arrival_order:
            messagebox.showinfo("No Data", "Queue is empty. Nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save Queue As")
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Patient Name", "Timestamp"])
                for name, timestamp in self.arrival_order:
                    writer.writerow([name, timestamp])
            self.log(f"📄 Queue exported to: {file_path}")
            messagebox.showinfo("Export Successful", f"Queue saved to:\n{file_path}")
        except Exception as e:
            self.log(f"❌ Error exporting CSV: {str(e)}")
            messagebox.showerror("Export Failed", f"An error occurred:\n{str(e)}")

    def clear_console(self):
        self.log_box.delete("1.0", tk.END)
        self.log("🧹 Console cleared")