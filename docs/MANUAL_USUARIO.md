# Renombramiento Masivo de Fotos y Documentos

Esta aplicación permite renombrar masivamente archivos de fotos y documentos de manera eficiente, utilizando una interfaz gráfica intuitiva.

### Instalación y Requisitos

- **Requisitos del sistema**: Windows con soporte para ejecutables.
- **Ejecución**: Descomprime el ZIP y ejecuta `Renombrador.exe`.

### Uso de la Aplicación

1. **Inicio**: Al ejecutar la aplicación, se abre una ventana con el título "Renombramiento Masivo de Fotos y Docs".

2. **Configuración de Filas**:
   - La aplicación inicia con una fila de configuración.
   - Cada fila permite configurar una tarea de renombramiento independiente.

3. **Campos de Configuración por Fila**:
   - **Elegir Origen**: Haz clic en "📂 Elegir Origen" para seleccionar la carpeta que contiene los archivos a renombrar.
   - **Nombre nuevo**: Ingresa el prefijo para los nuevos nombres de archivo (ej. "Vacaciones").
   - **Tipo**: Selecciona el tipo de archivo de la lista desplegable (Fotos, Word, Pdf, Excel).
   - **Carpeta destino (opcional)**: Si deseas copiar los archivos a otra carpeta en lugar de renombrarlos en la original, selecciona una carpeta destino.

4. **Agregar Más Filas**:
   - Haz clic en "+ Añadir otra fila" para agregar configuraciones adicionales.

5. **Eliminar Filas**:
   - Usa el botón "X" en la esquina superior derecha de cada fila para eliminarla.

6. **Reiniciar**:
   - El botón "Reiniciar" elimina todas las filas y limpia los resultados, permitiendo empezar de nuevo.

7. **Procesar**:
   - Haz clic en "EMPEZAR" para iniciar el proceso de renombramiento.
   - La aplicación validará los campos y mostrará advertencias o errores si faltan datos.
   - Se mostrará una confirmación antes de proceder.

8. **Resultados**:
   - Los resultados se muestran en el cuadro de texto inferior, incluyendo detalles de archivos procesados.
   - Para filas procesadas, se habilita el botón "Restaurar" para revertir los cambios.

9. **Restaurar**:
   - Si se especificó una carpeta destino, "Restaurar" elimina las copias.
   - Si no, renombra los archivos de vuelta a sus nombres originales.

### Notas Importantes

- Los archivos se renombran con el formato: `Nombre_XX.ext` donde XX es un número secuencial.
- Si no se especifica destino, los archivos se renombran en la carpeta de origen.
- La aplicación soporta extensiones: JPG, PNG, JPEG, DOCX, DOC, PDF, XLSX, XLS.
- Se recomienda hacer una copia de seguridad antes de procesar archivos importantes.