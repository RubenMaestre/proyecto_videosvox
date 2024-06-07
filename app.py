from flask import Flask, request, send_file, render_template, jsonify
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from PIL import Image
from flask_socketio import SocketIO, emit
import threading
import time
import csv
from datetime import datetime
from collections import defaultdict
from io import StringIO
import re

# Inicializamos la aplicación de Flask. Flask es un framework de Python que nos permite crear aplicaciones web.
# Aquí configuramos las rutas para archivos estáticos (CSS, JS, imágenes) y plantillas HTML.
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Configuramos SocketIO para permitir comunicación en tiempo real entre el servidor y el cliente (como mensajes de chat o notificaciones en vivo).
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, async_mode='eventlet')

# Ajustamos una constante en la librería PIL para mejorar la calidad de las imágenes redimensionadas.
# Este es un cambio requerido por una actualización de la librería.
Image.ANTIALIAS = Image.Resampling.LANCZOS

# Función para cargar una lista de municipios desde un archivo de texto.
# Los municipios son nombres de lugares que vamos a necesitar en nuestra aplicación.
def load_municipios():
    try:
        with open('municipios.txt', 'r', encoding='utf-8') as file:
            municipios = [line.strip() for line in file.readlines()]
    except Exception as e:
        municipios = []
    return municipios

# Función para cargar un mapeo (asociaciones) entre nombres de archivos originales y nombres normalizados.
# Esto nos ayuda a encontrar el archivo correcto basado en un nombre más simple o estandarizado.
def load_mapping():
    mapping = {}
    try:
        with open('file_mapping.txt', 'r', encoding='utf-8') as file:
            for line in file:
                original, normalized = line.strip().split(' -> ')
                mapping[original] = normalized
    except Exception as e:
        pass
    return mapping

# Función para convertir videos a formato MP4.
# MP4 es un formato de video muy común que es compatible con la mayoría de los dispositivos.
def convert_to_mp4(input_path, output_path, size=None, fps=None):
    try:
        clip = VideoFileClip(input_path)
        # Si se especifica un tamaño o FPS (frames por segundo), ajustamos el video.
        if size or fps:
            if size:
                clip = clip.resize(size)
            if fps:
                clip = clip.set_fps(fps)
        # Guardamos el video convertido en la ruta de salida especificada.
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return output_path
    except Exception as e:
        print(f"Error al convertir el video: {e}")
        return None

# Función para detectar el sistema operativo del usuario basándonos en el User-Agent.
# El User-Agent es una cadena de texto que envía el navegador web y que nos dice información sobre el dispositivo y el navegador.
def get_operating_system(user_agent):
    user_agent = user_agent.lower()
    
    # Aquí buscamos palabras clave específicas en el User-Agent para identificar el sistema operativo.
    if 'android' in user_agent:
        return 'Android'
    elif 'iphone' in user_agent or 'ipad' in user_agent:
        return 'iOS'
    elif 'windows' in user_agent:
        return 'Windows'
    elif 'macintosh' in user_agent:
        return 'MacOS'
    elif 'linux' in user_agent:
        return 'Linux'
    else:
        return 'Otro'

# Función para registrar la creación de un video en un archivo CSV (Comma Separated Values).
# Un archivo CSV es como una hoja de cálculo simple que podemos abrir en Excel o Google Sheets.
def log_video_creation(municipio, formato, dispositivo, ip, duracion, resolucion, estado):
    filepath = 'static/estadisticas/video_statistics.csv'
    fieldnames = ['municipio', 'formato', 'dispositivo', 'ip', 'duracion', 'resolucion', 'estado', 'created_at']

    # Verificamos si el archivo ya existe.
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Si el archivo no existe, escribimos el encabezado.
        if not file_exists:
            writer.writeheader()

        # Registramos la hora actual en formato UTC (Tiempo Universal Coordinado).
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Escribimos una nueva línea en el archivo CSV con los detalles del video.
        writer.writerow({
            'municipio': municipio,
            'formato': formato,
            'dispositivo': dispositivo,
            'ip': ip,
            'duracion': duracion,
            'resolucion': resolucion,
            'estado': estado,
            'created_at': current_time
        })

# Función para redimensionar y recortar el video según el formato deseado (cuadrado, vertical, horizontal).
# Esto es útil para adaptar el video a diferentes plataformas que pueden tener requisitos específicos de tamaño.
def resize_and_crop(clip, format):
    if format == 'square':
        crop_size = min(clip.size)
        clip = clip.crop(width=crop_size, height=crop_size, x_center=clip.w/2, y_center=clip.h/2)
    elif format == 'vertical':
        width, height = clip.size
        new_width = min(width, int(height * 9 / 16))
        new_height = int(new_width * 16 / 9)
        clip = clip.crop(width=new_width, height=new_height, x_center=clip.w/2, y_center=clip.h/2)
        clip = clip.resize(height=1920)
    elif format == 'horizontal':
        width, height = clip.size
        new_height = min(height, int(width * 9 / 16))
        new_width = int(new_height * 16 / 9)
        clip = clip.crop(width=new_width, height=new_height, x_center=clip.w/2, y_center=clip.h/2)
    return clip

# Función principal para procesar el video subido por el usuario.
# Aquí hacemos varias cosas: convertir el video, ajustar el formato, añadir un video de cierre y registrar estadísticas.
def process_video(municipio, video_path, format, sid, dispositivo, sistema_operativo, ip):
    # Emitimos un mensaje de progreso al cliente indicando que el video ha sido subido.
    socketio.emit('progress', {'progress': 10, 'message': 'Video subido'}, to=sid)

    # Simulamos un pequeño retraso para mostrar progreso.
    time.sleep(1)
    socketio.emit('progress', {'progress': 20, 'message': 'Verificando formato del video'}, to=sid)

    # Verificamos si el video ya está en formato MP4.
    if video_path.lower().endswith('.mp4'):
        mp4_video_path = video_path
    else:
        # Si no está en MP4, lo convertimos.
        mp4_video_path = os.path.join('static', 'videos', 'uploaded', f'{os.path.splitext(os.path.basename(video_path))[0]}.mp4')
        converted_video_path = convert_to_mp4(video_path, mp4_video_path)

        if not converted_video_path:
            os.remove(video_path)
            socketio.emit('progress', {'progress': 100, 'message': 'Error: No se pudo convertir el video a MP4.'}, to=sid)
            return

    socketio.emit('progress', {'progress': 30, 'message': 'Video convertido a MP4'}, to=sid)

    # Otro pequeño retraso para mostrar progreso.
    time.sleep(1)
    socketio.emit('progress', {'progress': 45, 'message': 'Cargando datos de mapeo'}, to=sid)

    # Cargamos el mapeo de archivos para encontrar el video de cierre correspondiente.
    mapping = load_mapping()
    original_filename = f"{municipio}.mp4"
    normalized_filename = mapping.get(original_filename, None)

    if not normalized_filename:
        os.remove(video_path)
        if mp4_video_path != video_path:
            os.remove(mp4_video_path)
        socketio.emit('progress', {'progress': 100, 'message': f'Error: No se encontró el video de cierre para {municipio}'}, to=sid)
        return

    cierre_video_path = os.path.join('static', 'videos', 'cierre', normalized_filename)

    if not os.path.exists(cierre_video_path):
        os.remove(video_path)
        if mp4_video_path != video_path:
            os.remove(mp4_video_path)
        socketio.emit('progress', {'progress': 100, 'message': f'Error: El video de cierre no se encuentra en la ruta {cierre_video_path}'}, to=sid)
        return

    # Cargamos los clips de video del video subido y del video de cierre.
    input_clip = VideoFileClip(mp4_video_path)
    cierre_clip = VideoFileClip(cierre_video_path)

    # Ajustamos el tamaño y la velocidad de fotogramas del video de cierre para que coincida con el video subido.
    if input_clip.size != cierre_clip.size or input_clip.fps != cierre_clip.fps:
        cierre_clip = cierre_clip.resize(input_clip.size).set_fps(input_clip.fps)
    
    # Aplicamos el redimensionamiento y recorte según el formato seleccionado.
    input_clip = resize_and_crop(input_clip, format)
    cierre_clip = resize_and_crop(cierre_clip, format)

    socketio.emit('progress', {'progress': 70, 'message': 'Videos ajustados'}, to=sid)

    # Definimos la ruta para el video final procesado.
    final_video_path = os.path.join('static', 'videos', 'output', f'final_{os.path.basename(video_path)}')

    try:
        # Concatenamos los clips de video (video subido + video de cierre) y lo guardamos.
        final_clip = concatenate_videoclips([input_clip, cierre_clip])
        final_clip.write_videofile(
            final_video_path,
            codec='libx264',
            bitrate="2000k",  # Ajustamos el bitrate para reducir la calidad si es necesario.
            audio_codec='aac',
            preset='fast'  # Usamos un preset rápido para la codificación.
        )

        # Obtenemos la duración y resolución del video final.
        duracion = final_clip.duration
        resolucion = f"{final_clip.size[0]}x{final_clip.size[1]}"

        # Registramos la creación del video en el archivo CSV.
        log_video_creation(municipio, format, f'{dispositivo} ({sistema_operativo})', ip, duracion, resolucion, 'éxito')

        socketio.emit('progress', {'progress': 90, 'message': 'Video finalizado'}, to=sid)

        # Enviamos un mensaje al cliente indicando que el proceso ha sido completado y proporcionamos el enlace de descarga.
        socketio.emit('progress', {'progress': 100, 'message': 'Proceso completado'}, to=sid)
        socketio.emit('download', {'url': f'/static/videos/output/final_{os.path.basename(video_path)}'}, to=sid)

    except Exception as e:
        # Si ocurre un error durante el procesamiento, lo registramos y notificamos al cliente.
        print(f"Error procesando el video: {e}")
        log_video_creation(municipio, format, f'{dispositivo} ({sistema_operativo})', ip, None, None, f'error: {e}')
        socketio.emit('progress', {'progress': 100, 'message': f'Error procesando el video: {e}'}, to=sid)

# Función para limpiar archivos temporales después de un tiempo.
# Esto es importante para no llenar el disco duro con archivos temporales.
def clean_up_files(video_path, mp4_video_path, cierre_resized_path, final_video_path):
    time.sleep(600)  # Esperamos 10 minutos antes de limpiar
    try:
        os.remove(video_path)
        if mp4_video_path != video_path:
            os.remove(mp4_video_path)
        if cierre_resized_path:
            os.remove(cierre_resized_path)
        os.remove(final_video_path)
    except Exception as e:
        print(f"Error al eliminar archivos temporales: {e}")

# Ruta principal para cargar la página inicial.
# Esta función carga una lista de municipios y renderiza (muestra) la plantilla HTML index.html.
@app.route('/')
def index():
    municipios = load_municipios()
    return render_template('index.html', municipios=municipios)

# Ruta para subir videos.
# Esta función maneja la subida de videos por parte del usuario.
@app.route('/videos/uploaded', methods=['POST'])
def upload_video():
    municipio = request.form['municipio']
    video_file = request.files['file']
    format = request.form['format']
    sid = request.form['sid']
    
    if not municipio or not video_file or not format or not sid:
        return jsonify(message="Faltan datos requeridos."), 400

    user_agent = request.headers.get('User-Agent').lower()
    dispositivo = 'móvil' if 'mobile' in user_agent else 'computadora'
    sistema_operativo = get_operating_system(user_agent)

    ip = request.remote_addr

    # Guardamos el video subido en la ruta especificada.
    video_path = os.path.join('static', 'videos', 'uploaded', video_file.filename)
    video_file.save(video_path)

    print(f"Video guardado en: {video_path}")

    # Iniciamos un hilo separado para procesar el video, así no bloqueamos el servidor mientras se procesa.
    thread = threading.Thread(target=process_video, args=(municipio, video_path, format, sid, dispositivo, sistema_operativo, ip))
    thread.start()

    return jsonify(message="Procesando el video, por favor espera...")

# Ruta para descargar las estadísticas en formato CSV.
@app.route('/download_statistics', methods=['GET'])
def download_statistics():
    # Usamos defaultdict para contar las estadísticas de videos por municipio, formato, dispositivo y mes.
    statistics = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    with open('static/estadisticas/video_statistics.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            municipio = row['municipio']
            formato = row['formato']
            dispositivo = row['dispositivo']
            month = row['created_at'][:7]  # Extraer YYYY-MM del campo de fecha
            statistics[municipio][formato][dispositivo][month] += 1

    # Preparamos el archivo CSV para descarga.
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Municipio', 'Formato', 'Dispositivo', 'Mes', 'Total'])

    for municipio, formatos in statistics.items():
        for formato, dispositivos in formatos.items():
            for dispositivo, months in dispositivos.items():
                for month, count in months.items():
                    writer.writerow([municipio, formato, dispositivo, month, count])

    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        attachment_filename='video_statistics.csv',
        as_attachment=True
    )

# Evento que se dispara cuando un cliente se conecta a SocketIO.
# Aquí simplemente imprimimos un mensaje y emitimos un evento de conexión.
@socketio.on('connect')
def handle_connect():
    print(f"Cliente conectado: {request.sid}")
    emit('connected', {'sid': request.sid})

# Iniciamos la aplicación. Si ejecutamos este script directamente (no importado como módulo), iniciamos el servidor.
if __name__ == '__main__':
    socketio.run(app, debug=True)
