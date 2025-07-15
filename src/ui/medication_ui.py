import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from tkcalendar import DateEntry
from src.ds.LinkedList_medication import MedicationHistory


class MedicationTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize the data structure
        self.log_output = None
        self.entry_date = None
        self.entry_dosage = None
        self.entry_name = None
        self.entry_pid = None
        self.med_manager = MedicationHistory()

        # Tooltip label (hidden by default)
        self.tooltip = tk.Label(self, text="", bg="#1e293b", fg="white", font=("Poppins", 9), bd=1, relief="solid", padx=5,
                           pady=2)

        self.setup_ui()

    # UI Setup
    def setup_ui(self):
        self.config(bg="#0f172a")

        # Fonts and style presets
        font_header = ("Poppins", 12, "bold")
        font_input = ("Poppins", 10)
        btn_style = {"font": font_input, "padx": 10, "pady": 5, "width": 18}

        # ------------------- Sidebar -------------------
        sidebar = tk.Frame(self, bg="#1e293b", width=150)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="🧬 Menu", font=("Poppins", 13, "bold"), bg="#1e293b", fg="white").pack(pady=(20, 10))
        tk.Label(sidebar, text="💊 Add", font=font_input, bg="#1e293b", fg="#10b981").pack(pady=2)
        tk.Label(sidebar, text="📜 History", font=font_input, bg="#1e293b", fg="#3b82f6").pack(pady=2)
        tk.Label(sidebar, text="❌ Delete", font=font_input, bg="#1e293b", fg="#ef4444").pack(pady=2)

        # ------------------- Main Content -------------------
        main_frame = tk.Frame(self, bg="#0f172a", padx=20, pady=20)
        main_frame.pack(side="left", fill="both", expand=True)

        # Row 1: Patient ID
        tk.Label(main_frame, text="Patient ID", font=font_header, fg="white", bg="#0f172a").grid(row=0, column=0,
                                                                                                 sticky="w", pady=5)
        self.entry_pid = tk.Entry(main_frame, font=font_input)
        self.entry_pid.grid(row=0, column=1, pady=5, padx=10)

        # Row 2: Medication Name
        tk.Label(main_frame, text="Medication Name", font=font_header, fg="white", bg="#0f172a").grid(row=1, column=0,
                                                                                                      sticky="w",
                                                                                                      pady=5)
        self.entry_name = tk.Entry(main_frame, font=font_input)
        self.entry_name.grid(row=1, column=1, pady=5, padx=10)

        # Row 3: Dosage
        tk.Label(main_frame, text="Dosage", font=font_header, fg="white", bg="#0f172a").grid(row=2, column=0,
                                                                                             sticky="w", pady=5)
        self.entry_dosage = tk.Entry(main_frame, font=font_input)
        self.entry_dosage.grid(row=2, column=1, pady=5, padx=10)

        # Row 4: Date Picker
        tk.Label(main_frame, text="Date", font=font_header, fg="white", bg="#0f172a").grid(row=3, column=0, sticky="w",
                                                                                           pady=5)
        self.entry_date = DateEntry(main_frame, width=18, background="#2563eb", foreground="white", borderwidth=2,
                               date_pattern='yyyy-mm-dd', font=font_input)
        self.entry_date.grid(row=3, column=1, pady=5, padx=10)

        # Row 5: Buttons
        btn_add = tk.Button(main_frame, text="Add Medication", command=self.add_med, bg="#10b981", fg="white", **btn_style)
        btn_add.grid(row=4, column=0, pady=15)
        btn_add.bind("<Enter>", lambda e: self.show_tooltip(e, "Add new medication entry"))
        btn_add.bind("<Leave>", self.hide_tooltip)

        btn_delete = tk.Button(main_frame, text="Delete Medication", command=self.del_med, bg="#ef4444", fg="white",
                               **btn_style)
        btn_delete.grid(row=4, column=1, pady=15)
        btn_delete.bind("<Enter>", lambda e: self.show_tooltip(e, "Delete medication by name"))
        btn_delete.bind("<Leave>", self.hide_tooltip)

        btn_show = tk.Button(main_frame, text="Show History", command=self.show_history, bg="#3b82f6", fg="white",
                             **btn_style)
        btn_show.grid(row=4, column=2, pady=15)
        btn_show.bind("<Enter>", lambda e: self.show_tooltip(e, "Display full medication history"))
        btn_show.bind("<Leave>", self.hide_tooltip)

        # Row 6: Log Output
        self.log_output = scrolledtext.ScrolledText(main_frame, height=10, bg="#1e293b", fg="#22c55e",
                                               insertbackground="#22c55e", font=("Courier New", 10))
        self.log_output.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)

        # Expand log box when window grows
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

    # ------------------- Functions -------------------
    def add_med(self):
        pid = self.entry_pid.get()
        name = self.entry_name.get()
        dose = self.entry_dosage.get()
        date = self.entry_date.get()

        if pid and name and dose and date:
            self.med_manager.add_medication(pid, name, dose, date)
            self.log_output.insert(tk.END, f"✔ Added: {name} ({dose}) on {date}\n")
        else:
            messagebox.showwarning("Missing info", "Please fill in all fields.")

    def del_med(self):
        pid = self.entry_pid.get()
        name = self.entry_name.get()

        if pid and name:
            self.med_manager.delete_medication(pid, name)
            self.log_output.insert(tk.END, f"❌ Deleted: {name} for {pid}\n")
        else:
            messagebox.showwarning("Missing info", "Patient ID and Medication Name required.")


    def show_history(self):
        pid = self.entry_pid.get().strip()
        if pid:
            meds = self.med_manager.show_medication_history(pid)
            self.log_output.insert(tk.END, f"\n📜 History for {pid}:\n")
        else:
            meds = self.med_manager.show_medication_history()
            self.log_output.insert(tk.END, f"\n📜 Full Medication History:\n")

        for med in meds:
            self.log_output.insert(tk.END, f"  • Patient: {med[0]} — {med[1]} ({med[2]}) on {med[3]}\n")


    def show_tooltip(self, event, text):
        self.tooltip.config(text=text)
        self.tooltip.place(x=event.x_root - self.winfo_rootx() + 20, y=event.y_root - self.winfo_rooty() + 10)

    def hide_tooltip(self,event):
        self.tooltip.place_forget()