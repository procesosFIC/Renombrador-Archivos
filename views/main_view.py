import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Dict, Any

class MainView:
    """Vista para la interfaz de usuario usando Tkinter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Renombramiento Masivo de Fotos y Docs")
        self.root.geometry("515x700")
        self.root.resizable(False, False)

        # Callbacks para eventos
        self.on_add_row: Callable[[], None] = None
        self.on_delete_row: Callable[[Dict[str, Any]], None] = None
        self.on_select_path: Callable[[tk.StringVar], None] = None
        self.on_process: Callable[[], None] = None
        self.on_reset: Callable[[], None] = None
        self.on_restore: Callable[[Dict[str, Any]], None] = None

        # Componentes de la interfaz
        self.filas_frames: Dict[int, tk.Frame] = {}
        self.text_resultados: tk.Text = None
        self.btn_empezar: tk.Button = None

        self._setup_ui()

    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Título
        titulo = tk.Label(self.root, text="Configuración de Renombramiento", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # Botón Reiniciar
        btn_reiniciar = tk.Button(self.root, text="Reiniciar", command=self._on_reset)
        btn_reiniciar.pack(anchor="w", padx=10, pady=(0,10))

        # Área scrollable
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.filas_frame = tk.Frame(self.scrollable_frame)
        self.filas_frame.pack(fill="both", expand=True)

        self.botones_frame = tk.Frame(self.scrollable_frame)
        self.botones_frame.pack(fill="x", pady=10)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Habilitar scroll con rueda del ratón
        def _on_mousewheel(event):
            # Verificar si el mouse está sobre el text widget de resultados
            x, y = self.root.winfo_pointerxy()
            tx, ty = self.text_resultados.winfo_rootx(), self.text_resultados.winfo_rooty()
            tw, th = self.text_resultados.winfo_width(), self.text_resultados.winfo_height()

            if (tx <= x <= tx + tw) and (ty <= y <= ty + th):
                # Si está sobre el text widget, dejar que maneje su propio scroll
                return

            # Verificar si el mouse está sobre el canvas
            cx, cy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
            cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()

            if (cx <= x <= cx + cw) and (cy <= y <= cy + ch):
                # Solo hacer scroll si hay contenido que se extienda más allá del área visible
                scrollregion = self.canvas.cget('scrollregion')
                if scrollregion:
                    x1, y1, x2, y2 = [int(coord) for coord in scrollregion.split()]
                    canvas_height = self.canvas.winfo_height()
                    if y2 > canvas_height:  # Hay contenido que se extiende verticalmente
                        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind al canvas y a la ventana raíz para capturar todos los eventos
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.root.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        # Botones de control
        self.btn_add = tk.Button(self.botones_frame, text="+ Añadir otra fila", command=self._on_add_row)
        self.btn_add.pack(anchor="center", pady=5)

        self.btn_empezar = tk.Button(self.botones_frame, text="EMPEZAR", command=self._on_process,
                                     bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        self.btn_empezar.pack(anchor="center", pady=5)

        # Cuadro de resultados
        self.text_resultados = tk.Text(self.botones_frame, height=15, width=50, state="disabled")
        self.text_resultados.pack(pady=10)

    def add_row(self, fila_data: Dict[str, Any]) -> None:
        """Agrega una fila visual a la interfaz."""
        num = fila_data["num"]

        # Marco contenedor
        row_frame = tk.Frame(self.filas_frame, bd=2, relief="groove", pady=5, padx=5)
        row_frame.pack(fill="x", pady=5, padx=5, expand=True)

        # Línea 1: Ruta y Eliminar
        line1 = tk.Frame(row_frame)
        line1.pack(fill="x", pady=2)

        path_var = tk.StringVar()
        btn_ruta = tk.Button(line1, text="📂 Elegir Origen", command=lambda: self._on_select_path(path_var))
        btn_ruta.pack(side="left")

        entry_ruta = tk.Entry(line1, textvariable=path_var, state="readonly", width=50)
        entry_ruta.pack(side="left", padx=5)

        btn_eliminar = tk.Button(line1, text="X", bg="#ffcccc", fg="red", font=("Arial", 8, "bold"))
        btn_eliminar.pack(side="right", padx=5)

        # Línea 2: Nombre y Tipo
        line2 = tk.Frame(row_frame)
        line2.pack(fill="x", pady=5)

        tk.Label(line2, text="Nombre nuevo:").pack(side="left")
        entry_nombre = tk.Entry(line2, width=25)
        entry_nombre.pack(side="left", padx=5)

        tk.Label(line2, text="Tipo:").pack(side="left", padx=(15, 5))
        combo_tipo = ttk.Combobox(line2, values=list(fila_data.get("extensiones", {}).keys()), state="readonly", width=10)
        combo_tipo.pack(side="left")

        # Línea 3: Destino
        line3 = tk.Frame(row_frame)
        line3.pack(fill="x", pady=5)

        tk.Label(line3, text="Carpeta destino (opcional):").pack(side="left")
        path_destino_var = tk.StringVar()
        btn_destino = tk.Button(line3, text="📂 Elegir Destino", command=lambda: self._on_select_path(path_destino_var))
        btn_destino.pack(side="left", padx=5)
        entry_destino = tk.Entry(line3, textvariable=path_destino_var, state="readonly", width=30)
        entry_destino.pack(side="left", padx=5)

        # Línea 4: Restaurar
        line4 = tk.Frame(row_frame)
        line4.pack(fill="x", pady=5)

        btn_restaurar = tk.Button(line4, text="Restaurar", state="disabled", command=lambda: self._on_restore(fila_data))
        btn_restaurar.pack(side="right", padx=5)

        # Guardar referencias
        fila_data.update({
            "frame": row_frame,
            "path_var": path_var,
            "entry_nombre": entry_nombre,
            "combo_tipo": combo_tipo,
            "path_destino_var": path_destino_var,
            "entry_destino": entry_destino,
            "btn_restaurar": btn_restaurar
        })

        self.filas_frames[num] = row_frame
        btn_eliminar.config(command=lambda: self._on_delete_row(fila_data))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def remove_row(self, fila_data: Dict[str, Any]) -> None:
        """Elimina una fila visual."""
        if fila_data["num"] in self.filas_frames:
            self.filas_frames[fila_data["num"]].destroy()
            del self.filas_frames[fila_data["num"]]
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_all_rows(self) -> None:
        """Limpia todas las filas visuales."""
        for frame in self.filas_frames.values():
            frame.destroy()
        self.filas_frames.clear()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_results(self, text: str) -> None:
        """Muestra resultados en el cuadro de texto."""
        self.text_resultados.config(state="normal")
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, text)
        self.text_resultados.config(state="disabled")

    def append_result(self, text: str) -> None:
        """Agrega texto a los resultados."""
        self.text_resultados.config(state="normal")
        self.text_resultados.insert(tk.END, text)
        self.text_resultados.config(state="disabled")

    def clear_results(self) -> None:
        """Limpia el cuadro de resultados."""
        self.text_resultados.config(state="normal")
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.config(state="disabled")

    def show_error(self, title: str, message: str) -> None:
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str) -> None:
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)

    def ask_yes_no(self, title: str, message: str) -> bool:
        """Pregunta sí/no al usuario."""
        return messagebox.askyesno(title, message)

    def show_info(self, title: str, message: str) -> None:
        """Muestra un mensaje informativo."""
        messagebox.showinfo(title, message)

    def enable_restore_button(self, fila_data: Dict[str, Any]) -> None:
        """Habilita el botón de restaurar para una fila."""
        fila_data["btn_restaurar"].config(state="normal")

    def disable_restore_button(self, fila_data: Dict[str, Any]) -> None:
        """Deshabilita el botón de restaurar para una fila."""
        fila_data["btn_restaurar"].config(state="disabled")

    # Métodos privados para callbacks
    def _on_add_row(self):
        if self.on_add_row:
            self.on_add_row()

    def _on_delete_row(self, fila_data):
        if self.on_delete_row:
            self.on_delete_row(fila_data)

    def _on_select_path(self, var):
        if self.on_select_path:
            self.on_select_path(var)

    def _on_process(self):
        if self.on_process:
            self.on_process()

    def _on_reset(self):
        if self.on_reset:
            self.on_reset()

    def _on_restore(self, fila_data):
        if self.on_restore:
            self.on_restore(fila_data)