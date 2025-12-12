import tkinter as tk
from models.file_model import FileModel
from views.main_view import MainView
from controllers.renamer_controller import RenamerController

if __name__ == "__main__":
    root = tk.Tk()

    # Instanciar MVC
    model = FileModel()
    view = MainView(root)
    controller = RenamerController(model, view)

    root.mainloop()