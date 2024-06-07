# Constructor de vídeos VOX - Provincia de Alicante

## Descripción del proyecto

Este proyecto es una solución personal que he creado para resolver un problema recurrente que he detectado como responsable provincial de comunicación del partido político VOX. Muchos responsables locales y concejales tenían dificultades a la hora de crear sus vídeos para redes sociales y me pedían ayuda para un proceso que es, en gran medida, mecánico. Mi objetivo con este proyecto es agilizar y automatizar dicho proceso.

La aplicación permitirá que los responsables o concejales suban sus vídeos, como una intervención en pleno o explicando cualquier cosa, y automáticamente se añadirá el cierre correspondiente del municipio, transformándolo en un vídeo oficial. Además, permitirá seleccionar el formato del vídeo (horizontal, vertical y cuadrado) para adaptarse a los requisitos de las diferentes redes sociales.

Para consumo interno, he desarrollado un sistema de estadísticas que permitirá visualizar la cantidad de descargas por municipio, sistema operativo, formato y fechas. Esto me ayudará a llevar un registro de la actividad realizada y a medir para futuras funcionalidades.

## Funcionalidades

- **Subida de vídeos**: Permitirá a los usuarios subir vídeos desde sus dispositivos.
- **Conversión y edición de vídeos**: Convertirá los vídeos subidos a formato MP4, si no lo están ya, y añadirá automáticamente el cierre correspondiente del municipio.
- **Formatos de vídeo**: Permitirá seleccionar entre formatos horizontal, vertical y cuadrado, adaptándose a diferentes plataformas de redes sociales.
- **Estadísticas internas**: Un sistema de estadísticas que permitirá monitorizar la actividad de descargas por municipio, sistema operativo, formato y fecha.

## Uso

1. **Seleccionar municipio**: Los usuarios seleccionarán su municipio desde un menú desplegable.
2. **Subir vídeo**: Subirán su vídeo desde su dispositivo.
3. **Seleccionar formato**: Elegirán el formato del vídeo (horizontal, vertical, cuadrado).
4. **Procesar vídeo**: El sistema procesará el vídeo, añadirá el cierre del municipio y lo convertirá al formato seleccionado.
5. **Descargar vídeo**: Una vez completado el procesamiento, el usuario podrá descargar el vídeo finalizado.

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

- **Vídeos de cierre**: En este repositorio solo incluyo el vídeo de cierre para Alicante. Los vídeos de cierre para otros municipios no están disponibles.
- **Estadísticas**: Las estadísticas generadas son para consumo interno y no están expuestas públicamente.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o envía un pull request con tus mejoras.

## Enlace a la aplicación online

voxvideos.rubenmaestre.com
---

**Realizado por Rubén Maestre**

