# Renombramiento Masivo de Fotos y Documentos

Esta aplicación permite renombrar archivos de manera masiva en una carpeta seleccionada. Está desarrollada en Python con una interfaz gráfica de usuario (GUI) utilizando Tkinter. Soporta filtrado por tipo de archivo (fotos, documentos Word, PDFs, Excel), procesamiento manual de filas, y **generación automática de tareas** mediante el escaneo recursivo de directorios.

## Características Principales

- **Generación Automática**: Escanea recursivamente una carpeta origen y crea automáticamente filas de configuración para todas las subcarpetas que contengan archivos del tipo seleccionado.
- **Renombrado Masivo**: Renombra múltiples archivos con un patrón personalizado (ej. nombre_01.ext, nombre_02.ext).
- **Filtrado por Tipo**: Opciones para procesar solo fotos, documentos o todos los archivos.
- **Copia o Renombrado**: Puede renombrar en la misma carpeta o copiar a una carpeta destino.
- **Restauración**: Permite revertir los cambios realizados.
- **Interfaz Intuitiva**: GUI scrollable para configurar múltiples operaciones.
- **Ejecutable Independiente**: Puede distribuirse como un archivo .exe sin requerir Python instalado.

## Requisitos

- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

## Instalación y Uso

1. Clona o descarga el repositorio.
2. Ejecuta `python main.py` para iniciar la aplicación.
3. Configura las filas de renombramiento y presiona "EMPEZAR".

## Documentación

- [Manual de Usuario](docs/MANUAL_USUARIO.md): Guía completa para usar la aplicación.
- [Manual Técnico](docs/MANUAL_TECNICO.md): Detalles técnicos sobre la implementación y arquitectura.
- [Manual de Distribución](docs/MANUAL_DISTRIBUCION.md): Instrucciones para crear un ejecutable distribuible con PyInstaller.

## Contribución

Si deseas contribuir, revisa los manuales técnicos y asegúrate de seguir las mejores prácticas de Python.

## Licencia

Este proyecto es de código abierto. Consulta los términos de uso en los manuales.
