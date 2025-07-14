from tkinter import *
from ds.queue_appointments import AppointmentQueue
from database.db_connection import get_connection

def launch_gui():
    queue=AppointmentQueue()

    def add_patient():
        name=entry_name.get()
        if name:
            queue.enqueue(name)
            update_display()
            entry_name.delete(0,END)

    def serve_patient():
        served=queue.dequeue()
        update_display()
        label_served.config(text=f"Served:{served if served else 'None'}")

    def update_display():
        current_queue=queue.viewQueue()
        listbox_queue.delete(0,END)
        for patient in current_queue:
            listbox_queue.insert(END,patient)

    root = Tk()
    root.title("Appointment Queue")

    Label(root, text="Patient Name").pack(pady=10)
    entry_name = Entry(root)
    entry_name.pack(pady=5)

    Button(root, text="Add to Queue",command=add_patient).pack()
    Button(root, text="Serve Next Patient",command=serve_patient).pack()

    label_served = Label(root, text="Served:")
    label_served.pack()

    listbox_queue = Listbox(root,height=5,width=50)
    listbox_queue.pack(pady=10)

    root.mainloop()