APP_TITLE = "Renombramiento Masivo de Fotos y Docs"
VIEW_TITLE = "Configuración de Renombramiento"
BUTTON_RESET = "Reiniciar"
BUTTON_ADD_ROW = "+ Añadir otra fila"
BUTTON_PROCESS = "EMPEZAR"
BUTTON_SELECT_ORIGIN = "📂 Elegir Origen"
BUTTON_SELECT_DEST = "📂 Elegir Destino"
BUTTON_RESTORE = "Restaurar"
LABEL_NEW_NAME = "Nombre nuevo:"
LABEL_TYPE = "Tipo:"
LABEL_DESTINATION = "Carpeta destino (opcional):"

PANEL_TITLE = "Renombramiento masivo de carpetas"
PANEL_SRC_LABEL = "Carpeta origen:"
PANEL_DEST_LABEL = "Carpeta destino (opcional):"
PANEL_DETECT_BUTTON = "Generar"
PANEL_NO_MATCHES = "No se encontraron carpetas con archivos del tipo seleccionado."

EMPTY_PROCESS_TITLE = "Vacío"
EMPTY_PROCESS_MESSAGE = "No hay filas para procesar."
WARNING_DIALOG_TITLE = "Advertencia"
WARNING_DEST_EMPTY_MESSAGE = (
    "En algunas filas no se especificó carpeta destino. Los archivos se renombrarán en la carpeta de origen."
)
CONFIRMATION_TITLE = "Confirmación"
CONFIRMATION_MESSAGE = "¿Estás seguro de proceder con el renombramiento?"
ERROR_DIALOG_TITLE = "Error"
PROCESS_EXCEPTION_MESSAGE = "Ocurrió un error inesperado al procesar los archivos. Revisa los logs para más detalles."
RESTORE_EXCEPTION_MESSAGE = "Ocurrió un error al restaurar los archivos. Revisa los logs para más detalles."
RESTORE_COMPLETE_TITLE = "Restauración Completada"

FILENAME_TOO_LONG_TITLE = "Nombre demasiado largo"
FILENAME_TOO_LONG_MESSAGE = "El nombre generado excede los {max} caracteres: {name}"

RESULTS_TEMPLATE = (
    "Proceso completado.\n"
    "{total} archivo(s) procesado(s).\n\n"
    "Detalles:\n"
    "{details}"
)
RESTORE_RESULT_HEADER_TEMPLATE = "\n[FILA {fila}]\n"
RESTORE_RESULT_SUMMARY_TEMPLATE = "  {restaurados} archivo(s) restaurado(s).\n"

def format_process_results(total: int, details: str) -> str:
    return RESULTS_TEMPLATE.format(total=total, details=details)

def format_restore_info_message(fila_num: int, restaurados: int) -> str:
    return f"Se restauraron {restaurados} archivo(s) de la fila {fila_num}."

def format_restore_result_header(fila_num: int) -> str:
    return RESTORE_RESULT_HEADER_TEMPLATE.format(fila=fila_num)

def format_restore_result_summary(restaurados: int) -> str:
    return RESTORE_RESULT_SUMMARY_TEMPLATE.format(restaurados=restaurados)