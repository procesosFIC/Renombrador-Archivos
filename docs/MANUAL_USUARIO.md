# Renombramiento Masivo de Fotos y Documentos

Esta aplicación permite renombrar masivamente archivos de fotos y documentos de manera eficiente, utilizando una interfaz gráfica intuitiva.

### Instalación y Requisitos

- **Requisitos del sistema**: Windows con soporte para ejecutables.
- **Ejecución**: Descomprime el ZIP y ejecuta `Renombrador.exe`.

### Uso de la Aplicación

1. **Inicio**: Al ejecutar la aplicación, se abre una ventana con el título "Renombramiento Masivo de Fotos y Docs".

2. **Generación Automática de Filas (Panel Superior)**:
   - **Carpeta origen**: Selecciona la carpeta raíz donde buscar subcarpetas con archivos.
   - **Carpeta destino (opcional)**: Selecciona una carpeta base para guardar los archivos renombrados. Si se deja vacío, se renombrarán en su ubicación original.
   - **Tipo**: Elige el tipo de archivo a buscar (Fotos, Word, Pdf, Excel).
   - **Generar**: Al hacer clic, la aplicación buscará recursivamente carpetas que contengan archivos del tipo seleccionado y creará automáticamente una fila de configuración para cada una.

3. **Configuración Manual de Filas**:
   - Puedes agregar filas manualmente o editar las generadas automáticamente.
   - **Elegir Origen**: Selecciona la carpeta con los archivos a renombrar.
   - **Nombre nuevo**: Ingresa el prefijo para los archivos (ej. "Vacaciones"). En la generación automática, esto se completa basado en el nombre de la carpeta.
   - **Tipo**: Selecciona el tipo de archivo.
   - **Carpeta destino**: Opcional.
   - **Eliminar**: Usa el botón "X" para quitar una fila.

4. **Agregar Más Filas**:
   - Haz clic en "+ Añadir otra fila" para agregar configuraciones manuales adicionales.

5. **Reiniciar**:
   - El botón "Reiniciar" limpia todas las filas (manuales y generadas) y los resultados.

6. **Procesar**:
   - Haz clic en "EMPEZAR" para iniciar el proceso de renombramiento.
   - La aplicación validará los campos y pedirá confirmación.

7. **Resultados**:
   - Los detalles del proceso se muestran en el cuadro de texto inferior.
   - Se habilitará el botón "Restaurar" en cada fila procesada exitosamente.

8. **Restaurar**:
   - Si se especificó una carpeta destino, "Restaurar" elimina las copias creadas.
   - Si se renombró en la carpeta original, "Restaurar" devuelve los archivos a sus nombres originales.

### Notas Importantes

- Los archivos se renombran con el formato: `Nombre_XX.ext` donde XX es un número secuencial.
- Si no se especifica destino, los archivos se renombran en la carpeta de origen.
- La aplicación soporta extensiones: JPG, PNG, JPEG, DOCX, DOC, PDF, XLSX, XLS.
- Se recomienda hacer una copia de seguridad antes de procesar archivos importantes.