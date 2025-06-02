
"""yang li gomez uribe
mao ying gomez uribe
yeison andres villegas pabon"""

import pygame
from mutagen.mp3 import MP3
from mutagen import File
import time
import os

class WMPModel:
    def __init__(self):
        pygame.mixer.init()
        self.track = None
        self.playlist = []  # Lista de canciones
        self.track_duration = 0
        self.start_time = 0

    def load_playlist(self, folder_path):
        """Carga automáticamente todos los archivos de audio de la carpeta."""
        try:
            audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
            self.playlist = []
            
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(file.lower())
                    if ext in audio_extensions:
                        self.playlist.append(file_path)
            
            if self.playlist:
                self.playlist.sort()  # Ordenar alfabéticamente
                print(f"🎶 {len(self.playlist)} canciones cargadas desde {folder_path}")
                return True
            else:
                print("⚠ No se encontraron archivos de audio compatibles.")
                return False
                
        except Exception as e:
            print(f"❌ Error al cargar la lista de reproducción: {e}")
            return False

    def load_track(self, file_path):
        """Carga una pista individual."""
        try:
            pygame.mixer.music.load(file_path)
            self.track = file_path
            
            # Obtener duración usando mutagen
            audio_file = File(file_path)
            if audio_file is not None and hasattr(audio_file, 'info'):
                self.track_duration = audio_file.info.length
            else:
                # Fallback para archivos que mutagen no puede leer
                self.track_duration = 0
                
            print(f"🎵 Pista cargada: {os.path.basename(file_path)}")
            if self.track_duration > 0:
                print(f"⏳ Duración: {self.track_duration:.2f} segundos")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar la pista {file_path}: {e}")
            return False

    def play(self):
        """Reproduce la música."""
        try:
            pygame.mixer.music.play()
            # Solo actualizar start_time si no se ha establecido previamente
            if not hasattr(self, 'start_time') or self.start_time == 0:
                self.start_time = time.time()
            return True
        except Exception as e:
            print(f"❌ Error al reproducir: {e}")
            return False

    def pause(self):
        """Pausa la música."""
        try:
            pygame.mixer.music.pause()
            return True
        except Exception as e:
            print(f"❌ Error al pausar: {e}")
            return False

    def stop(self):
        """Detiene la música."""
        try:
            pygame.mixer.music.stop()
            return True
        except Exception as e:
            print(f"❌ Error al detener: {e}")
            return False

    def get_track_info(self):
        """Obtiene información de la pista actual."""
        if self.track:
            try:
                audio_file = File(self.track)
                info = {
                    'filename': os.path.basename(self.track),
                    'filepath': self.track,
                    'duration': self.track_duration
                }
                
                # Intentar obtener metadatos
                if audio_file is not None:
                    info['title'] = audio_file.get('TIT2', [os.path.basename(self.track)])[0] if audio_file.get('TIT2') else os.path.basename(self.track)
                    info['artist'] = audio_file.get('TPE1', ['Desconocido'])[0] if audio_file.get('TPE1') else 'Desconocido'
                    info['album'] = audio_file.get('TALB', ['Desconocido'])[0] if audio_file.get('TALB') else 'Desconocido'
                else:
                    info['title'] = os.path.basename(self.track)
                    info['artist'] = 'Desconocido'
                    info['album'] = 'Desconocido'
                
                return info
            except Exception as e:
                print(f"Error al obtener información de la pista: {e}")
                
        return {
            'filename': 'Sin canción',
            'filepath': '',
            'duration': 0,
            'title': 'Sin canción',
            'artist': '',
            'album': ''
        }