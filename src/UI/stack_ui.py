import tkinter as tk
from tkinter import simpledialog, messagebox
from src.ds.undo_redo_stack import Stack
from src.database.stacks_db import init_db, save_input, get_input, load_input

class DoctorNoteEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Note editor")

        init_db()

        self.undo_stack = Stack()
        self.redo_stack = Stack()

        self.text_area = tk.Text(root, wrap="word", undo=False )
        self.text_area.pack(expand=True, fill="both")

        self.log = tk.Listbox(root, height=5)
        self.log.pack(fill="x")

        self.add_buttons()
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.undo_stack.push("")

    def add_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Undo", command=self.undo).pack(side="left", padx=5)
        tk.Button(frame, text="Redo", command=self.redo).pack(side="left", padx=5)
        tk.Button(frame, text="Save to DB", command=self.save_to_db).pack(side="left", padx=5)
        tk.Button(frame, text="load from DB", command=self.load_from_db).pack(side="left", padx=5)
        tk.Button(frame, text="Clear", command=self.clear).pack(side="left", padx=5)

    def log_action(self, message):
        self.log.insert("end", message)
        self.log.yview("end")

    def on_text_change(self, event=None):
        current_text = self.text_area.get("1.0", "end-1c")

        if self.undo_stack.peek() != current_text:
            self.undo_stack.push(current_text)
            self.redo_stack.clear()
            self.log_action("Typed - stack updated")

    def undo(self):
        if self.undo_stack.size() > 1:
            current_text = self.undo_stack.pop()
            self.redo_stack.push(current_text)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", self.undo_stack.peek())
            self.log_action("Undo done")
        else:
            self.log_action("Nothing to undo")

    def redo(self):
        if not self.redo_stack.is_empty():
            current_text = self.redo_stack.pop()
            self.undo_stack.push(current_text)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", current_text)
            self.log_action("Redo done")
        else:
            self.log_action("Nothing to redo")

    def save_to_db(self):
        content = self.text_area.get("1.0", "end-1c")
        title = tk.simpledialog.askstring("Name", "Enter a Name for this content!")
        
        if title:
            save_input(title, content)
            self.log_action("Saved to DB")

    def load_from_db(self):
        inputs = get_input()
        if not inputs:
            messagebox.showerror("Error", "No data saved yet")
            return

        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select a data file to open")

        listbox = tk.Listbox(selection_window, width=50)
        listbox.pack(padx=10, pady=10)

        for data in inputs:
            listbox.insert("end", f"{data[0]} - {data[1]} ({data[2][:19]})")

        def open_selected_file():
            selection = listbox.curselection()
            if selection:
                selected = inputs[selection[0]]
                content = load_input(selected[0])
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", content)
                self.undo_stack.clear()
                self.redo_stack.clear()
                self.undo_stack.push(content)
                self.log_action(f"Loaded data '{selected[1]}' from db")
                selection_window.destroy()

        tk.Button(selection_window, text="Open", command=open_selected_file).pack(padx=5)


    def clear(self):
        self.text_area.delete("1.0", "end")
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.undo_stack.push("")
        self.log_action("Cleared editor")


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = DoctorNoteEditor(root)
    root.mainloop()
