# Constructor de Vídeos VOX - Provincia de Alicante

## Descripción del Proyecto

Este proyecto es una solución personal creada para resolver un problema recurrente que he detectado como responsable provincial de comunicación del partido político VOX. Muchos responsables locales y concejales enfrentan dificultades al crear vídeos para redes sociales, solicitando ayuda para un proceso que es en gran medida mecánico. Este proyecto tiene como objetivo agilizar y automatizar ese proceso.

La aplicación permite que los responsables o concejales puedan subir sus vídeos, como una intervención en pleno o explicaciones diversas, y automáticamente se añade el cierre correspondiente del municipio, transformándolo en un vídeo oficial. Además, proporciona opciones para seleccionar el formato del vídeo (horizontal, vertical y cuadrado) adaptándose a los requisitos de diferentes redes sociales.

Para propósitos internos, he desarrollado un sistema de estadísticas que permite visualizar la cantidad de descargas por municipio, sistema operativo, formato, fechas, etc. Esto me ayuda a llevar un registro de la actividad realizada y a medir para futuras funcionalidades.

## Funcionalidades

- **Subida de Vídeos**: Permite a los usuarios subir vídeos desde sus dispositivos.
- **Conversión y Edición de Vídeos**: Convierte los vídeos subidos a formato MP4, si no lo están ya, y añade automáticamente el cierre correspondiente del municipio.
- **Formatos de Vídeo**: Opción para seleccionar entre formatos horizontal, vertical y cuadrado, adaptándose a diferentes plataformas de redes sociales.
- **Estadísticas Internas**: Sistema de estadísticas para monitorizar la actividad de descargas por municipio, sistema operativo, formato y fecha.

## Uso

1. **Seleccionar Municipio**: Los usuarios seleccionan su municipio desde un menú desplegable.
2. **Subir Vídeo**: Suben su vídeo desde su dispositivo.
3. **Seleccionar Formato**: Eligen el formato del vídeo (horizontal, vertical, cuadrado).
4. **Procesar Vídeo**: El sistema procesa el vídeo, añade el cierre del municipio y lo convierte al formato seleccionado.
5. **Descargar Vídeo**: Una vez completado el procesamiento, el usuario puede descargar el vídeo finalizado.

## Requisitos

- **Python 3.8+**
- **Flask**
- **Flask-SocketIO**
- **MoviePy**
- **Pillow**
- **Eventlet**

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/constructor-videos-vox.git
    cd constructor-videos-vox
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```bash
    flask run
    ```

## Archivos Importantes

- **app.py**: El archivo principal de la aplicación, donde se configuran las rutas y la lógica del servidor.
- **templates/index.html**: La plantilla HTML para la página principal.
- **static/**: Carpeta que contiene archivos estáticos como CSS, JS y logos.

## Notas

- **Vídeos de Cierre**: En este repositorio solo se incluye el vídeo de cierre para Alicante. Los vídeos de cierre para otros municipios no están disponibles.
- **Estadísticas**: Las estadísticas generadas son para consumo interno y no están expuestas públicamente.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o envía un pull request con tus mejoras.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

**Realizado por Rubén Maestre**
