import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import datetime
import csv

from ..ds.priorityQueue import PriorityQueue
from ..database.priorityQueue_dao import add_patient_to_db, get_all_patients


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Priority Queue System")
        self.root.geometry("700x500")
        self.queue = PriorityQueue()

        # UI Frames
        top_frame = tk.Frame(root, padx=20, pady=10)
        top_frame.pack(fill="x")

        mid_frame = tk.Frame(root, padx=20, pady=10)
        mid_frame.pack(fill="x")

        list_frame = tk.Frame(root, padx=20, pady=10)
        list_frame.pack(fill="both", expand=True)

        log_frame = tk.Frame(root, padx=20, pady=10)
        log_frame.pack(fill="both", expand=True)

        # --- Top Input Form ---
        tk.Label(top_frame, text="Patient Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(top_frame)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(top_frame, text="Priority (1-5):").grid(row=0, column=2, sticky="e")
        self.priority_entry = tk.Entry(top_frame)
        self.priority_entry.grid(row=0, column=3, padx=10)

        tk.Button(top_frame, text="Add Patient", bg="#27ae60", fg="white", command=self.add_patient).grid(row=0, column=4, padx=10)
        tk.Button(top_frame, text="Serve Next", bg="#e67e22", fg="white", command=self.serve_patient).grid(row=0, column=5, padx=10)

        # --- Mid Buttons ---
        tk.Button(mid_frame, text="Show Arrival Order", bg="#2980b9", fg="white", command=self.show_arrival_order).grid(row=0, column=0, padx=5)
        tk.Button(mid_frame, text="Show Priority Order", bg="#8e44ad", fg="white", command=self.show_priority_order).grid(row=0, column=1, padx=5)
        tk.Button(mid_frame, text="Clear Console", bg="#95a5a6", command=self.clear_console).grid(row=0, column=2, padx=5)
        tk.Button(mid_frame, text="Export to CSV", bg="#34495e", fg="white", command=self.export_to_csv).grid(row=0, column=3, padx=5)

        # --- Patient List Display ---
        tk.Label(list_frame, text="Patient Queue:").pack(anchor="w")
        self.patient_list = tk.Listbox(list_frame, height=8, font=('Courier', 10))
        self.patient_list.pack(fill="both", expand=True, pady=(0, 10))

        # --- Console Output ---
        tk.Label(log_frame, text="Console Log:").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(log_frame, height=10, bg="#2c3e50", fg="#ecf0f1")
        self.log_box.pack(fill="both", expand=True)

        self.arrival_order = []  # [(name, priority, timestamp)]
        self.update_display()

    def log(self, message):
        """ Append messages to console log box """
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def add_patient(self):
        """ Handle patient input, validate and insert into queue """
        name = self.name_entry.get().strip()
        try:
            priority = int(self.priority_entry.get())
            if not name or not (1 <= priority <= 5):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a name and a priority (1-5).")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.queue.insert(name, priority)
        self.arrival_order.append((name, priority, timestamp))  # now includes timestamp
        add_patient_to_db(name, priority)

        self.name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.log(f"✅ Added: {name} (Priority {priority}) at {timestamp}")
        self.show_arrival_order()

    def serve_patient(self):
        """ Remove highest priority patient from queue """
        patient = self.queue.remove_highest_priority()
        if patient:
            self.log(f"🚑 Serving {patient.name} (Priority {patient.priority})")
            self.arrival_order = [p for p in self.arrival_order if p[0] != patient.name]
            self.show_arrival_order()
        else:
            messagebox.showinfo("Queue Empty", "No patients in the queue.")

    def show_arrival_order(self):
        """ Display patients in order they were added """
        self.patient_list.delete(0, tk.END)
        self.log("👥 Showing in Arrival Order")
        for i, (name, priority, timestamp) in enumerate(self.arrival_order, 1):
            entry = f"{i:>2}. {name:<15} Priority: {priority}  Time: {timestamp}"
            self.patient_list.insert(tk.END, entry)

    def show_priority_order(self):
        """ Display patients sorted by priority """
        self.patient_list.delete(0, tk.END)
        self.log("🔢 Showing in Priority Order")
        sorted_patients = sorted(self.arrival_order, key=lambda x: x[1])  # sort by priority
        for i, (name, priority, timestamp) in enumerate(sorted_patients, 1):
            entry = f"{i:>2}. {name:<15} Priority: {priority}  Time: {timestamp}"
            self.patient_list.insert(tk.END, entry)

    def export_to_csv(self):
        """ Export the patient arrival list to a CSV file """
        if not self.arrival_order:
            messagebox.showinfo("No Data", "No patient records to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")],
                                                 title="Save Report As")
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Priority", "Timestamp"])
                for name, priority, timestamp in self.arrival_order:
                    writer.writerow([name, priority, timestamp])
            self.log(f"📄 Report saved to {file_path}")
            messagebox.showinfo("Export Successful", f"Report saved to:\n{file_path}")
        except Exception as e:
            self.log(f"❌ Error exporting report: {str(e)}")
            messagebox.showerror("Export Failed", f"An error occurred:\n{str(e)}")

    def clear_console(self):
        self.log_box.delete("1.0", tk.END)
        self.log("🧹 Console cleared")

    def update_display(self):
        self.show_arrival_order()


# Run the app if this file is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
