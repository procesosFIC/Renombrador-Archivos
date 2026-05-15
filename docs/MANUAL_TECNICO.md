# Manual Técnico - Aplicación de Renombramiento Masivo

Esta aplicación está desarrollada en Python siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC) para una mejor separación de responsabilidades, escalabilidad y mantenibilidad. Utiliza Tkinter para la interfaz gráfica de usuario y permite renombrar archivos de manera masiva en una carpeta seleccionada, con opciones para filtrar por tipo de archivo. Incluye funcionalidades de generación automática de tareas mediante escaneo recursivo, restauración y distribución como ejecutable independiente.

### Arquitectura MVC

La aplicación sigue el patrón Modelo-Vista-Controlador (MVC) para separar responsabilidades:

- **Modelo (`models/file_model.py`)**: Gestiona los datos y la lógica de negocio relacionada con archivos.
- **Vista (`views/main_view.py`)**: Maneja la interfaz de usuario con Tkinter.
- **Controlador (`controllers/renamer_controller.py`)**: Coordina entre modelo y vista, manejando eventos y lógica de aplicación.

### Componentes Principales

- **Interfaz Gráfica**: Utiliza widgets de Tkinter incluyendo un panel superior para la generación automática de filas basada en detección de carpetas, y una interfaz scrollable para gestionar múltiples configuraciones individuales.
- **Procesamiento de Archivos**: Emplea `pathlib` y `shutil` para manejar rutas y operaciones de archivo de manera segura, soportando renombrado in-situ o copia a destino.
- **Validación**: Incluye validaciones exhaustivas antes del procesamiento para evitar errores, incluyendo verificación de rutas, nombres y tipos.
- **Diccionario de Extensiones**: `FileModel.EXTENSIONES` define los tipos de archivo soportados.

### Clases Principales

#### FileModel (Modelo)

Gestiona los datos de filas y operaciones de archivo:

- **Atributos**: `filas_datos`, `num_fila`, `EXTENSIONES`
- **Métodos**: `agregar_fila()`, `eliminar_fila()`, `validar_fila()`, `procesar_filas()`, `restaurar_fila()`, `reiniciar()`

#### MainView (Vista)

Maneja la interfaz de usuario:

- **Atributos**: `root`, `canvas`, `scrollbar`, `text_resultados`, `filas_frames`, `panel_src_var`, `panel_dest_var`, `panel_type_combo`
- **Métodos**: `add_row()`, `remove_row()`, `show_results()`, `show_error()`, `ask_yes_no()`, `_on_detect()`

#### RenamerController (Controlador)

Coordina modelo y vista:

- **Atributos**: `model`, `view`
- **Métodos**: `add_row()`, `delete_row()`, `select_path()`, `process()`, `reset()`, `restore_row()`, `detect_folders()`

### Diagrama de Arquitectura MVC

```mermaid
graph TD
    A[main.py] --> B
    B --> C
    B --> D

    C --> B
    D --> B

    subgraph "Modelo"
        D["FileModel<br/>- filas_datos<br/>- EXTENSIONES<br/>+ procesar_filas()<br/>+ restaurar_fila()"]
    end

    subgraph "Vista"
        C["MainView<br/>- root<br/>- canvas<br/>- text_resultados<br/>+ add_row()<br/>+ show_results()"]
    end

    subgraph "Controlador"
        B["RenamerController<br/>- model<br/>- view<br/>+ process()<br/>+ detect_folders()"]
    end
```

### Diagrama de Clases

```mermaid
classDiagram
    class FileModel {
        +filas_datos: List[Dict]
        +num_fila: int
        +EXTENSIONES: Dict
        +agregar_fila()
        +eliminar_fila(fila)
        +validar_fila(fila)
        +procesar_filas()
        +restaurar_fila(fila)
        +reiniciar()
    }

    class MainView {
        +root: Tk
        +canvas: Canvas
        +text_resultados: Text
        +filas_frames: Dict
        +panel_src_var: StringVar
        +panel_dest_var: StringVar
        +panel_type_combo: Combobox
        +add_row(fila_data)
        +remove_row(fila_data)
        +show_results(text)
        +show_error(title, message)
        +ask_yes_no(title, message)
    }

    class RenamerController {
        +model: FileModel
        +view: MainView
        +add_row()
        +delete_row(fila_data)
        +select_path(var)
        +process()
        +reset()
        +restore_row(fila_data)
        +detect_folders()
    }

    RenamerController --> FileModel
    RenamerController --> MainView
```

### Flujo de Procesamiento

1. **Generación Automática (Opcional)**: El usuario puede usar `detect_folders()` para escanear recursivamente una carpeta origen. Esto genera filas automáticamente para cada subcarpeta que contenga archivos del tipo especificado.
   - Si se define carpeta destino global, se calcula la estructura de subcarpetas correspondiente.
   - Si no, se configura para renombrar in-situ (ruta destino vacía).
2. **Validación**: Se verifican rutas, nombres y tipos para cada fila. Para el tipo "Todos", no se filtra por extensión.
3. **Confirmación**: Se solicita confirmación del usuario antes de proceder.
4. **Procesamiento**: Se itera sobre cada fila, encontrando archivos según el tipo seleccionado (filtrados por extensión o todos los archivos), y renombrándolos o copiándolos al destino especificado.
5. **Registro**: Se actualiza la lista de archivos procesados para permitir restauración a nombres originales.
6. **Resultados**: Se muestran detalles del procesamiento en la interfaz, incluyendo archivos afectados y posibles errores.

### Consideraciones Técnicas

- **Arquitectura MVC**: Separación clara de responsabilidades facilita el mantenimiento, testing y escalabilidad.
- **Manejo de Errores**: Utiliza bloques try-except para operaciones de archivo, capturando excepciones y mostrando mensajes de error al usuario.
- **Rendimiento**: Los archivos se ordenan alfabéticamente antes del procesamiento para asegurar consistencia en el renombrado secuencial.
- **Seguridad**: Evita sobrescrituras accidentales mediante validaciones previas; utiliza copias cuando se especifica una carpeta destino diferente.
- **Extensibilidad**: El diccionario `FileModel.EXTENSIONES` facilita la adición de nuevos tipos de archivo. La arquitectura modular permite agregar nuevas vistas o controladores fácilmente.
- **Interfaz de Usuario**: Diseño scrollable para manejar múltiples filas de configuración; incluye botones de restauración para revertir cambios.
- **Sistema de Logging**: Los errores durante el procesamiento y restauración de archivos se registran automáticamente en `logs/renombramiento.log` con timestamps detallados.
- **Distribución**: Compatible con creación de ejecutables independientes usando PyInstaller, permitiendo distribución sin instalación de Python.