import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

from logger import get_app_logger

class FileModel:
    """Modelo para manejar datos y operaciones de archivo."""

    # Diccionario de extensiones
    EXTENSIONES = {
        "Fotos": [".jpg", ".png", ".jpeg"],
        "Word": [".docx", ".doc"],
        "Pdf": [".pdf"],
        "Excel": [".xlsx", ".xls"]
    }

    def __init__(self):
        self.filas_datos: List[Dict[str, Any]] = []
        self.num_fila = 0
        self.logger = get_app_logger()

    def agregar_fila(self) -> Dict[str, Any]:
        """Crea una nueva fila de datos."""
        self.num_fila += 1
        fila = {
            "num": self.num_fila,
            "ruta_origen": "",
            "nombre_nuevo": "",
            "tipo": "",
            "ruta_destino": "",
            "procesados": []
        }
        self.filas_datos.append(fila)
        return fila

    def eliminar_fila(self, fila: Dict[str, Any]) -> None:
        """Elimina una fila de datos."""
        if fila in self.filas_datos:
            self.filas_datos.remove(fila)

    def reiniciar(self) -> None:
        """Reinicia el modelo eliminando todas las filas."""
        self.filas_datos.clear()
        self.num_fila = 0

    def validar_fila(self, fila: Dict[str, Any]) -> str:
        """Valida una fila y retorna mensaje de error o vacío si es válida."""
        if not fila["ruta_origen"]:
            return f"Fila #{fila['num']}: Falta seleccionar la RUTA."
        if not fila["nombre_nuevo"].strip():
            return f"Fila #{fila['num']}: Falta escribir el NOMBRE."
        if not fila["tipo"]:
            return f"Fila #{fila['num']}: Falta seleccionar el TIPO de documento."
        if not os.path.exists(fila["ruta_origen"]):
            return f"Fila #{fila['num']}: La ruta no existe: {fila['ruta_origen']}"
        destino = fila["ruta_destino"].strip() or fila["ruta_origen"]
        if destino != fila["ruta_origen"] and not os.path.exists(destino):
            return f"Fila #{fila['num']}: La carpeta destino no existe: {destino}"
        return ""

    def procesar_filas(self) -> Dict[str, Any]:
        """Procesa todas las filas válidas y retorna resultados."""
        resultados = {
            "errores": [],
            "procesados": {},
            "total_renombrados": 0,
            "detalles": ""
        }

        datos_validos = []
        for fila in self.filas_datos:
            error = self.validar_fila(fila)
            if error:
                resultados["errores"].append(error)
                continue

            extensiones = self.EXTENSIONES[fila["tipo"]]
            destino = fila["ruta_destino"].strip() or fila["ruta_origen"]
            datos_validos.append({
                "fila": fila,
                "ruta": fila["ruta_origen"],
                "destino": destino,
                "nombre": fila["nombre_nuevo"].strip(),
                "tipo": fila["tipo"],
                "exts": extensiones
            })

        if resultados["errores"]:
            return resultados

        # Procesar cada fila válida
        for d in datos_validos:
            fila = d["fila"]
            resultados["detalles"] += f"[FILA {d['fila']['num']}]\n"
            resultados["detalles"] += f"  Ruta origen: {d['ruta']}\n"
            resultados["detalles"] += f"  Ruta destino: {d['destino']}\n"
            resultados["detalles"] += f"  Renombrar a: '{d['nombre']}_XX'\n"
            resultados["detalles"] += f"  Categoría: {d['tipo']}\n"
            resultados["detalles"] += f"  Extensiones objetivo: {d['exts']}\n"

            # Obtener archivos
            carpeta = Path(d['ruta'])
            archivos = [f for f in carpeta.iterdir() if f.is_file() and f.suffix.lower() in d['exts']]
            archivos.sort(key=lambda x: x.name)

            if not archivos:
                resultados["detalles"] += f"  No se encontraron archivos con extensiones {d['exts']}\n"
                continue

            resultados["detalles"] += f"  Encontrados {len(archivos)} archivo(s)\n"

            # Renombrar
            carpeta_destino = Path(d['destino'])
            procesados = []
            for idx, archivo in enumerate(archivos, start=1):
                extension = archivo.suffix
                nuevo_nombre = f"{d['nombre']}_{idx:02d}{extension}"
                nuevo_path = carpeta_destino / nuevo_nombre

                try:
                    if d['destino'] != d['ruta']:
                        shutil.copy2(str(archivo), str(nuevo_path))
                        resultados["detalles"] += f"  {archivo.name} → {nuevo_nombre} (copiado)\n"
                    else:
                        archivo.rename(nuevo_path)
                        resultados["detalles"] += f"  {archivo.name} → {nuevo_nombre} (renombrado)\n"
                    resultados["total_renombrados"] += 1
                    procesados.append({"original_name": archivo.name, "nuevo_name": nuevo_nombre})
                except Exception as e:
                    error_msg = f"Error al procesar {archivo.name}: {e}"
                    resultados["detalles"] += f"  {error_msg}\n"
                    self.logger.error(error_msg)

            resultados["procesados"][fila["num"]] = procesados
            fila["procesados"] = procesados
            resultados["detalles"] += "\n"

        return resultados

    def restaurar_fila(self, fila: Dict[str, Any]) -> int:
        """Restaura una fila a su estado original. Retorna número de archivos restaurados."""
        ruta = fila["ruta_origen"]
        destino = fila["ruta_destino"].strip() or ruta
        restaurados = 0

        for p in fila["procesados"]:
            try:
                if destino != ruta:
                    # Eliminar copia del destino
                    nuevo_path = Path(destino) / p["nuevo_name"]
                    if nuevo_path.exists():
                        nuevo_path.unlink()
                        restaurados += 1
                else:
                    # Renombrar de vuelta
                    original_path = Path(ruta) / p["original_name"]
                    nuevo_path = Path(ruta) / p["nuevo_name"]
                    if nuevo_path.exists():
                        nuevo_path.rename(original_path)
                        restaurados += 1
            except Exception as e:
                error_msg = f"Error al restaurar {p['nuevo_name']}: {e}"
                self.logger.error(error_msg)

        fila["procesados"] = []
        return restaurados