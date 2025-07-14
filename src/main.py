from tkinter import Tk
from src.ui.priorityQueueUI import MainWindow
from src.database.priorityQueue_db_config import initialize_db

def main():
    initialize_db()
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
