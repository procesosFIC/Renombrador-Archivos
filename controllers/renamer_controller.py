from tkinter import filedialog
from typing import Dict, Any

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

        # Agregar primera fila
        self.add_row()

    def _setup_callbacks(self):
        """Configura los callbacks de la vista."""
        self.view.on_add_row = self.add_row
        self.view.on_delete_row = self.delete_row
        self.view.on_select_path = self.select_path
        self.view.on_process = self.process
        self.view.on_reset = self.reset
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
            var.set(ruta)

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