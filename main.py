import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from pathlib import Path

# Diccionario de extensiones
EXTENSIONES = {
    "Fotos": [".jpg", ".png", ".jpeg"],
    "Word": [".docx", ".doc"],
    "Pdf": [".pdf"],
    "Excel": [".xlsx", ".xls"]
}

class RenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Renombramiento Masivo de Fotos y Docs")
        self.root.geometry("515x700")
        self.root.resizable(False, False)

        # Lista para guardar los datos de cada fila
        self.filas_datos = []

        # --- Título ---
        titulo = tk.Label(root, text="Configuración de Renombramiento", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # --- Botón Reiniciar ---
        btn_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        btn_reiniciar.pack(anchor="w", padx=10, pady=(0,10))

        # --- Área de desplazamiento (Canvas) para muchas filas ---
        # Esto permite añadir muchas filas sin que la ventana se rompa
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Frame para las filas
        self.filas_frame = tk.Frame(self.scrollable_frame)
        self.filas_frame.pack(fill="both", expand=True)

        # Frame para los botones
        self.botones_frame = tk.Frame(self.scrollable_frame)
        self.botones_frame.pack(fill="x", pady=10)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Habilitar scroll con rueda del ratón
        self.canvas.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        # Agregar la primera fila al iniciar
        self.agregar_fila()

        # --- Botones de Control (dentro del área scrollable, abajo) ---
        self.btn_add = tk.Button(self.botones_frame, text="+ Añadir otra fila", command=self.agregar_fila)
        self.btn_add.pack(anchor="center", pady=5)

        self.btn_empezar = tk.Button(self.botones_frame, text="EMPEZAR", command=self.procesar_datos,
                                     bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        self.btn_empezar.pack(anchor="center", pady=5)

        # --- Cuadro de texto para resultados ---
        self.text_resultados = tk.Text(self.botones_frame, height=15, width=50, state="disabled")
        self.text_resultados.pack(pady=10)

    def agregar_fila(self):
        """Crea un bloque visual con los campos requeridos"""

        # Número de fila
        if not hasattr(self, 'num_fila'):
            self.num_fila = 0
        self.num_fila += 1

        # Marco contenedor de la fila (con borde para agrupar visualmente)
        row_frame = tk.Frame(self.filas_frame, bd=2, relief="groove", pady=5, padx=5)
        row_frame.pack(fill="x", pady=5, padx=5, expand=True)

        # --- Línea 1: Ruta y Botón Eliminar ---
        line1 = tk.Frame(row_frame)
        line1.pack(fill="x", pady=2)

        path_var = tk.StringVar()
        
        btn_ruta = tk.Button(line1, text="📂 Elegir Origen", 
                             command=lambda: self.seleccionar_ruta(path_var))
        btn_ruta.pack(side="left")

        entry_ruta = tk.Entry(line1, textvariable=path_var, state="readonly", width=50)
        entry_ruta.pack(side="left", padx=5)

        # Botón Eliminar (Rojo)
        btn_eliminar = tk.Button(line1, text="X", bg="#ffcccc", fg="red", font=("Arial", 8, "bold"))
        btn_eliminar.pack(side="right", padx=5)

        # --- Línea 2: Nombre y Tipo de Archivo ---
        line2 = tk.Frame(row_frame)
        line2.pack(fill="x", pady=5)

        # Nombre
        tk.Label(line2, text="Nombre nuevo:").pack(side="left")
        entry_nombre = tk.Entry(line2, width=25)
        entry_nombre.pack(side="left", padx=5)

        # Lista Desplegable (Combobox)
        tk.Label(line2, text="Tipo:").pack(side="left", padx=(15, 5))
        combo_tipo = ttk.Combobox(line2, values=list(EXTENSIONES.keys()), state="readonly", width=10)
        combo_tipo.pack(side="left")

        # --- Línea 3: Carpeta Destino (opcional) ---
        line3 = tk.Frame(row_frame)
        line3.pack(fill="x", pady=5)

        tk.Label(line3, text="Carpeta destino (opcional):").pack(side="left")
        path_destino_var = tk.StringVar()
        btn_destino = tk.Button(line3, text="📂 Elegir Destino",
                                command=lambda: self.seleccionar_ruta(path_destino_var))
        btn_destino.pack(side="left", padx=5)
        entry_destino = tk.Entry(line3, textvariable=path_destino_var, state="readonly", width=30)
        entry_destino.pack(side="left", padx=5)

        line4 = tk.Frame(row_frame)
        line4.pack(fill="x", pady=5)

        # Botón Restaurar
        btn_restaurar = tk.Button(line4, text="Restaurar", state="disabled", command=lambda: self.restaurar_fila(datos_fila))
        btn_restaurar.pack(side="right", padx=5)

        # Objeto de datos para esta fila
        datos_fila = {
            "num": self.num_fila,     # Número de fila
            "frame": row_frame,       # Referencia al widget visual
            "path_var": path_var,     # Variable de la ruta origen
            "entry_nombre": entry_nombre, # Widget del nombre
            "combo_tipo": combo_tipo,  # Widget del combobox
            "path_destino_var": path_destino_var,  # Variable del destino
            "entry_destino": entry_destino,  # Widget del destino
            "btn_restaurar": btn_restaurar,  # Botón restaurar
            "procesados": []  # Lista de archivos procesados para restaurar
        }

        # Guardamos en la lista principal
        self.filas_datos.append(datos_fila)

        # Configuramos el botón eliminar pasando este objeto específico
        btn_eliminar.config(command=lambda: self.eliminar_fila(datos_fila))

        # Actualizar el canvas por si cambió el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def seleccionar_ruta(self, var):
        ruta = filedialog.askdirectory()
        if ruta:
            var.set(ruta)

    def eliminar_fila(self, datos_obj):
        """Elimina visualmente la fila y borra sus datos de la lista"""
        # Eliminar el widget visual
        datos_obj["frame"].destroy()
        # Eliminar de la lista de memoria
        if datos_obj in self.filas_datos:
            self.filas_datos.remove(datos_obj)
        
        # Actualizar el canvas por si cambió el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def restaurar_fila(self, datos_fila):
        """Restaura los archivos de una fila a su estado original"""
        ruta = datos_fila["path_var"].get()
        destino = datos_fila["path_destino_var"].get().strip() or ruta
        restaurados = 0
        for p in datos_fila["procesados"]:
            if destino != ruta:
                # Eliminar la copia del destino
                nuevo_path = Path(destino) / p["nuevo_name"]
                if nuevo_path.exists():
                    nuevo_path.unlink()
                    restaurados += 1
            else:
                # Renombrar de vuelta en origen
                original_path = Path(ruta) / p["original_name"]
                nuevo_path = Path(ruta) / p["nuevo_name"]
                if nuevo_path.exists():
                    nuevo_path.rename(original_path)
                    restaurados += 1
        datos_fila["procesados"] = []
        datos_fila["btn_restaurar"].config(state="disabled")
        # Mostrar en el cuadro de información
        self.text_resultados.config(state="normal")
        self.text_resultados.insert(tk.END, f"\n[FILA {datos_fila['num']}]\n")
        self.text_resultados.insert(tk.END, f"  {restaurados} archivo(s) restaurados(s).")
        self.text_resultados.config(state="disabled")

    def reiniciar(self):
        """Reinicia la aplicación: elimina todas las filas y limpia los resultados"""
        for fila in self.filas_datos[:]:
            self.eliminar_fila(fila)
        self.text_resultados.config(state="normal")
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.config(state="disabled")
        # Agregar la primera fila
        self.agregar_fila()

    def procesar_datos(self):
        """Valida y renombra los archivos"""
        if not self.filas_datos:
            messagebox.showwarning("Vacío", "No hay filas para procesar.")
            return

        print("\n" + "="*40)
        print(" INICIANDO PROCESO DE RENOMBRAMIENTO")
        print("="*40)

        datos_validos = []
        errores = False

        for i, fila in enumerate(self.filas_datos):
            num = i + 1
            ruta = fila["path_var"].get()
            nombre = fila["entry_nombre"].get().strip()
            tipo = fila["combo_tipo"].get()

            # --- VALIDACIONES ---
            if not ruta:
                messagebox.showerror("Error", f"Fila #{num}: Falta seleccionar la RUTA.")
                errores = True
                break
            if not nombre:
                messagebox.showerror("Error", f"Fila #{num}: Falta escribir el NOMBRE.")
                errores = True
                break
            if not tipo:
                messagebox.showerror("Error", f"Fila #{num}: Falta seleccionar el TIPO de documento.")
                errores = True
                break
            if not os.path.exists(ruta):
                messagebox.showerror("Error", f"Fila #{num}: La ruta no existe: {ruta}")
                errores = True
                break
            
            # Si pasa validación, guardamos para procesar
            extensiones = EXTENSIONES[tipo]
            destino = fila["path_destino_var"].get().strip() or fila["path_var"].get()
            if destino != ruta and not os.path.exists(destino):
                messagebox.showerror("Error", f"Fila #{num}: La carpeta destino no existe: {destino}")
                errores = True
                break
            datos_validos.append({
                "fila": num,
                "ruta": ruta,
                "destino": destino,
                "nombre": nombre,
                "tipo": tipo,
                "exts": extensiones
            })

        if not errores:
            # Verificar advertencia por destino vacío
            if any(not fila["path_destino_var"].get().strip() for fila in self.filas_datos):
                messagebox.showwarning("Advertencia", "En algunas filas no se especificó carpeta destino. Los archivos se renombrarán en la carpeta de origen.")

            # Verificar si todos los campos requeridos están llenos para doble confirmación
            campos_completos = all(
                fila["path_var"].get().strip() and
                fila["entry_nombre"].get().strip() and
                fila["combo_tipo"].get()
                for fila in self.filas_datos
            )
            if campos_completos:
                if not messagebox.askyesno("Confirmación", "¿Estás seguro de proceder con el renombramiento?"):
                    return

            # Procesar cada carpeta y renombrar archivos
            total_renombrados = 0
            resultados_texto = ""
            procesados_por_fila = {d["fila"]: [] for d in datos_validos}

            for d in datos_validos:
                resultados_texto += f"[FILA {d['fila']}]\n"
                resultados_texto += f"  Ruta origen: {d['ruta']}\n"
                resultados_texto += f"  Ruta destino: {d['destino']}\n"
                resultados_texto += f"  Renombrar a: '{d['nombre']}_XX'\n"
                resultados_texto += f"  Categoría: {d['tipo']}\n"
                resultados_texto += f"  Extensiones objetivo: {d['exts']}\n"

                # Obtener todos los archivos de la carpeta con las extensiones correctas
                carpeta = Path(d['ruta'])
                archivos = []

                for archivo in carpeta.iterdir():
                    if archivo.is_file() and archivo.suffix.lower() in d['exts']:
                        archivos.append(archivo)

                # Ordenar archivos por nombre para mantener consistencia
                archivos.sort(key=lambda x: x.name)

                if not archivos:
                    resultados_texto += f"  No se encontraron archivos con extensiones {d['exts']}\n"
                    continue

                resultados_texto += f"  Encontrados {len(archivos)} archivo(s)\n"

                # Renombrar cada archivo
                carpeta_destino = Path(d['destino'])
                for idx, archivo in enumerate(archivos, start=1):
                    extension = archivo.suffix
                    nuevo_nombre = f"{d['nombre']}_{idx:02d}{extension}"
                    nuevo_path = carpeta_destino / nuevo_nombre

                    try:
                        # Copiar o renombrar el archivo
                        if d['destino'] != d['ruta']:
                            shutil.copy2(str(archivo), str(nuevo_path))
                            resultados_texto += f"  {archivo.name} → {nuevo_nombre} (copiado)\n"
                        else:
                            archivo.rename(nuevo_path)
                            resultados_texto += f"  {archivo.name} → {nuevo_nombre} (renombrado)\n"
                        total_renombrados += 1
                        procesados_por_fila[d["fila"]].append({"original_name": archivo.name, "nuevo_name": nuevo_nombre})
                    except Exception as e:
                        resultados_texto += f"  Error al procesar {archivo.name}: {e}\n"
                        messagebox.showerror("Error", f"No se pudo procesar {archivo.name}: {e}")

                resultados_texto += "\n"

            # Mostrar resultados en el cuadro de texto
            self.text_resultados.config(state="normal")
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Proceso completado.\n{total_renombrados} archivo(s) procesado(s).\n\nDetalles:\n{resultados_texto}")
            self.text_resultados.config(state="disabled")

            # Habilitar botones de restaurar para filas procesadas
            for fila in self.filas_datos:
                if fila["num"] in procesados_por_fila and procesados_por_fila[fila["num"]]:
                    fila["procesados"] = procesados_por_fila[fila["num"]]
                    fila["btn_restaurar"].config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = RenamerApp(root)
    root.mainloop()