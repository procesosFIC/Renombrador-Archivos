from tkinter import filedialog
from typing import Dict, Any
import os

import messages
from logger import get_app_logger
from models.file_model import FileModel
from views.main_view import MainView

class RenamerController:
    """Controlador que maneja la lógica de negocio entre modelo y vista."""

    def __init__(self, model: FileModel, view: MainView):
        self.model = model
        self.view = view
        self.logger = get_app_logger()
        self._setup_callbacks()

        # Populate panel type selector (if view provides it)
        try:
            if hasattr(self.view, "panel_type_combo"):
                self.view.panel_type_combo["values"] = list(self.model.EXTENSIONES.keys())
        except Exception:
            # Non-fatal: log and continue
            self.logger.error("Could not initialize panel type combo values", exc_info=True)
 
        # Agregar primera fila
        self.add_row()

    def _setup_callbacks(self):
        """Configura los callbacks de la vista."""
        self.view.on_add_row = self.add_row
        self.view.on_delete_row = self.delete_row
        self.view.on_select_path = self.select_path
        self.view.on_process = self.process
        self.view.on_reset = self.reset
        self.view.on_detect_folders = self.detect_folders
        self.view.on_restore = self.restore_row

    def add_row(self) -> None:
        """Agrega una nueva fila."""
        fila = self.model.agregar_fila()
        fila["extensiones"] = self.model.EXTENSIONES  # Para el combobox
        self.view.add_row(fila)

    def delete_row(self, fila_data: Dict[str, Any]) -> None:
        """Elimina una fila."""
        self.model.eliminar_fila(fila_data)
        self.view.remove_row(fila_data)

    def select_path(self, var) -> None:
        """Selecciona una ruta usando el diálogo."""
        ruta = filedialog.askdirectory()
        if ruta:
            # Normalize path to use OS-native separators before storing in the StringVar
            var.set(os.path.normpath(ruta))

    def detect_folders(self) -> None:
        """Recorre recursivamente la carpeta origen y crea filas automáticas para carpetas que contengan archivos del tipo seleccionado."""
        try:
            src = getattr(self.view, "panel_src_var", None)
            if not src or not src.get().strip():
                self.view.show_error(messages.EMPTY_PROCESS_TITLE, "Seleccione una carpeta origen.")
                return

            raw_src = src.get().strip()
            src_path = os.path.normpath(raw_src)
            if not os.path.exists(src_path) or not os.path.isdir(src_path):
                self.view.show_error(messages.ERROR_DIALOG_TITLE, f"La ruta no existe o no es una carpeta: {src_path}")
                return

            selected_type = getattr(self.view, "panel_type_combo", None)
            tipo = selected_type.get() if selected_type else ""
            if not tipo:
                self.view.show_error(messages.ERROR_DIALOG_TITLE, "Seleccione un tipo de archivo.")
                return

            exts = [e.lower() for e in self.model.EXTENSIONES.get(tipo, [])]
            matches = []

            for dirpath, dirnames, filenames in os.walk(src_path):
                for f in filenames:
                    if any(f.lower().endswith(ext) for ext in exts):
                        matches.append(dirpath)
                        break  # found a matching file in this folder -> add folder once

            if not matches:
                self.view.show_info(messages.PANEL_TITLE, messages.PANEL_NO_MATCHES)
                return

            # Crear filas para cada carpeta encontrada.
            # Decisión de destino:
            # - Si el usuario especificó una carpeta destino en el panel, se replicará la estructura relativa dentro de esa carpeta
            #   (destino_calculado = os.path.join(dest_root, rel) cuando rel != "." o dest_root cuando rel == ".")
            # - Si no especificó destino, dejaremos ruta_destino = "" para indicar renombrado in-place (comportamiento por defecto).
            base_name = os.path.basename(src_path.rstrip(os.sep))
            dest_root = getattr(self.view, "panel_dest_var", None)
            dest_root_val = ""
            if dest_root and dest_root.get().strip():
                dest_root_val = os.path.normpath(dest_root.get().strip())
            for folder in sorted(set(matches)):
                rel = os.path.relpath(folder, src_path)
                if rel == ".":
                    name = base_name
                else:
                    name = base_name + "_" + rel.replace(os.sep, "_")

                # Calcular destino:
                # - If the user supplied a destination base, use that exact path for every generated row.
                #   DO NOT append subfolders or alter the provided destination.
                # - If no destination base is provided, leave ruta_destino empty to indicate renaming in-place.
                if dest_root_val:
                    destino_calculado = dest_root_val
                else:
                    destino_calculado = ""  # in-place (default)

                # Validar que la ruta_destino calculada existe si no está vacía; si no existe, mostrar advertencia y dejar en blanco.
                if destino_calculado and not os.path.exists(destino_calculado):
                    # Mostrar advertencia al usuario pero continuar creando la fila con ruta_destino vacía
                    # para que el usuario pueda corregirla manualmente.
                    self.view.show_warning(messages.WARNING_DIALOG_TITLE,
                                           f"La carpeta destino calculada no existe: {destino_calculado}. La fila se creará con ruta_destino vacía para renombrado in-place.")
                    destino_calculado = ""

                # Crear fila completamente poblada para evitar filas "vacías" en la UI
                fila = self.model.agregar_fila()
                fila["extensiones"] = self.model.EXTENSIONES
                # Normalize origin path to the OS-native format before showing/storing it
                fila["ruta_origen"] = os.path.normpath(str(folder))
                fila["nombre_nuevo"] = name
                fila["tipo"] = tipo
                fila["ruta_destino"] = destino_calculado

                # Entregar un dict completo a la vista para que add_row inicialice widgets con estos valores
                self.view.add_row(fila)
        except Exception:
            self.logger.error("Error al detectar carpetas para renombramiento masivo", exc_info=True)
            self.view.show_error(messages.ERROR_DIALOG_TITLE, messages.PROCESS_EXCEPTION_MESSAGE)

    def process(self) -> None:
        """Procesa todas las filas."""
        try:
            if not self.model.filas_datos:
                self.view.show_error(messages.EMPTY_PROCESS_TITLE, messages.EMPTY_PROCESS_MESSAGE)
                return

            # Sincronizar datos del modelo con valores actuales de widgets
            for fila in self.model.filas_datos:
                fila["ruta_origen"] = fila["path_var"].get().strip()
                fila["nombre_nuevo"] = fila["entry_nombre"].get().strip()
                fila["tipo"] = fila["combo_tipo"].get()
                fila["ruta_destino"] = fila["path_destino_var"].get().strip()

            # Verificar campos completos
            campos_completos = all(
                fila["ruta_origen"] and
                fila["nombre_nuevo"] and
                fila["tipo"]
                for fila in self.model.filas_datos
            )

            # Verificar advertencia por destino vacío (antes de confirmación)
            if any(not fila["ruta_destino"] for fila in self.model.filas_datos):
                self.view.show_warning(messages.WARNING_DIALOG_TITLE, messages.WARNING_DEST_EMPTY_MESSAGE)

            if campos_completos:
                if not self.view.ask_yes_no(messages.CONFIRMATION_TITLE, messages.CONFIRMATION_MESSAGE):
                    return

            # Procesar
            resultados = self.model.procesar_filas()

            if resultados["errores"]:
                for error in resultados["errores"]:
                    self.view.show_error(messages.ERROR_DIALOG_TITLE, error)
                return

            # Mostrar resultados
            texto_resultados = messages.format_process_results(
                total=resultados["total_renombrados"],
                details=resultados["detalles"]
            )
            self.view.show_results(texto_resultados)

            # Habilitar botones de restaurar
            for fila in self.model.filas_datos:
                if fila["num"] in resultados["procesados"] and resultados["procesados"][fila["num"]]:
                    self.view.enable_restore_button(fila)
        except Exception:
            self.logger.error("Error al procesar filas", exc_info=True)
            self.view.show_error(messages.ERROR_DIALOG_TITLE, messages.PROCESS_EXCEPTION_MESSAGE)

    def reset(self) -> None:
        """Reinicia la aplicación."""
        self.model.reiniciar()
        self.view.clear_all_rows()
        self.view.clear_results()
        self.add_row()  # Agregar primera fila

    def restore_row(self, fila_data: Dict[str, Any]) -> None:
        """Restaura una fila."""
        try:
            restaurados = self.model.restaurar_fila(fila_data)
            self.view.disable_restore_button(fila_data)

            # Mostrar cartel informativo
            self.view.show_info(
                messages.RESTORE_COMPLETE_TITLE,
                messages.format_restore_info_message(fila_data["num"], restaurados)
            )

            # Mostrar en resultados también
            self.view.append_result(messages.format_restore_result_header(fila_data["num"]))
            self.view.append_result(messages.format_restore_result_summary(restaurados))
        except Exception:
            self.logger.error(
                "Error al restaurar fila %s", fila_data.get("num"), exc_info=True
            )
            self.view.show_error(messages.ERROR_DIALOG_TITLE, messages.RESTORE_EXCEPTION_MESSAGE)