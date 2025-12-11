# Manual de Distribución

Este manual proporciona los pasos necesarios para convertir el script Python `main.py` en un ejecutable independiente utilizando PyInstaller. El ejecutable resultante puede distribuirse y ejecutarse en máquinas sin Python instalado.

## Requisitos
- Python 3.x instalado.
- Conocimientos básicos de línea de comandos.

## Pasos para Crear el Ejecutable

1. **Crear un Entorno Virtual**:
   ```
   python -m venv venv
   ```

2. **Activar el Entorno Virtual**:
   - En Windows: `venv\Scripts\activate`
   - En macOS/Linux: `source venv/bin/activate`

3. **Instalar PyInstaller**:
   ```
   pip install pyinstaller
   ```

4. **Crear el Ejecutable**:
   ```
   pyinstaller --onedir --windowed main.py
   ```
   - `--onedir`: Crea una carpeta con el ejecutable y dependencias.
   - `--windowed`: Oculta la consola en Windows.

5. **Ubicación del Ejecutable**:
   - El ejecutable estará en `dist/main/main.exe`.
   - Puedes renombrar `main.exe` a `Renombrador.exe` si deseas.

6. **Crear el ZIP para Distribución**:
   - Comprime la carpeta `dist/main/` en un archivo ZIP.
   - Incluye solo el contenido de `dist/main/`, no la carpeta completa.
   - El ZIP contendrá `Renombrador.exe` y archivos auxiliares necesarios.

## Notas Técnicas
- El ejecutable es independiente y no requiere Python en la máquina del usuario.
- Si hay errores, verifica que todas las dependencias estén incluidas.
- Para actualizar, recompila con PyInstaller después de cambios en el código.