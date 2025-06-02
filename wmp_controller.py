#mao ying gomez uribe   
#yang li gomez uribe
#yeison andres villegas pabon




import tkinter as tk
from tkinter import filedialog, messagebox
from wmp_view import WMPView
from wmp_model import WMPModel
import pygame
import time
import os

class WMPController:
    def __init__(self):
        pygame.mixer.init()

        self.ventana = tk.Tk()
        self.ventana.title("Windows Media Player 11 - Réplica")
        self.ventana.geometry("800x600")

        self.model = WMPModel()
        self.view = WMPView(self.ventana, self)

        self.current_track_index = 0
        self.is_paused = False

        self.ventana.after(500, self.sync_progress)  # Sincroniza la barra de progreso
        self.ventana.mainloop()

    def load_track(self):
        """Permite cargar una canción individual o una carpeta completa."""
        choice = messagebox.askyesnocancel(
            "Cargar Música", 
            "¿Deseas cargar una carpeta completa?\n\nSí = Carpeta\nNo = Archivo individual\nCancelar = Cancelar"
        )
        
        if choice is True:  # Cargar carpeta
            folder_path = filedialog.askdirectory(title="Seleccionar carpeta con música")
            if folder_path:
                self.model.load_playlist(folder_path)
                if self.model.playlist:
                    self.current_track_index = 0
                    self.load_current_track()
                    self.view.update_track_info(self.get_current_track_name())
                    messagebox.showinfo("Éxito", f"Se cargaron {len(self.model.playlist)} canciones")
        
        elif choice is False:  # Cargar archivo individual
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo de audio",
                filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
            )
            if file_path:
                # Crear una playlist con un solo archivo
                self.model.playlist = [file_path]
                self.current_track_index = 0
                self.load_current_track()
                self.view.update_track_info(self.get_current_track_name())

    def load_current_track(self):
        """Carga la canción actual de la playlist."""
        if self.model.playlist and 0 <= self.current_track_index < len(self.model.playlist):
            current_file = self.model.playlist[self.current_track_index]
            self.model.load_track(current_file)
            return True
        return False

    def get_current_track_name(self):
        """Obtiene el nombre de la canción actual."""
        if self.model.playlist and 0 <= self.current_track_index < len(self.model.playlist):
            file_path = self.model.playlist[self.current_track_index]
            return os.path.basename(file_path)
        return "Sin canción"

    def play(self):
        """Reproduce la música."""
        if not self.model.playlist:
            messagebox.showwarning("Advertencia", "No hay canciones cargadas")
            return
            
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            if self.load_current_track():
                self.model.play()
                self.view.update_track_info(self.get_current_track_name())

    def pause(self):
        """Pausa la música."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        """Detiene la música."""
        pygame.mixer.music.stop()
        self.is_paused = False

    def next_track(self):
        """Avanza a la siguiente canción."""
        if not self.model.playlist:
            return
            
        self.current_track_index = (self.current_track_index + 1) % len(self.model.playlist)
        if self.load_current_track():
            self.model.play()
            self.view.update_track_info(self.get_current_track_name())
            print(f"▶ Reproduciendo: {self.get_current_track_name()}")

    def prev_track(self):
        """Retrocede a la canción anterior."""
        if not self.model.playlist:
            return
            
        self.current_track_index = (self.current_track_index - 1) % len(self.model.playlist)
        if self.load_current_track():
            self.model.play()
            self.view.update_track_info(self.get_current_track_name())
            print(f"⏮ Reproduciendo: {self.get_current_track_name()}")

    def forward(self):
        """Avanza 10 segundos en la canción."""
        if not pygame.mixer.music.get_busy() or not hasattr(self.model, 'start_time'):
            return
            
        try:
            # Calcular posición actual y nueva posición
            current_elapsed = time.time() - self.model.start_time
            new_position = min(current_elapsed + 10, self.model.track_duration)
            
            # Detener la música actual
            pygame.mixer.music.stop()
            
            # Recargar la canción
            if self.load_current_track():
                # Reproducir desde la nueva posición ajustando el start_time
                pygame.mixer.music.play(start=new_position)
                self.model.start_time = time.time() - new_position
                print(f"⏩ Avanzando a {new_position:.1f}s")
        except Exception as e:
            # Fallback: recargar y ajustar tiempo manualmente
            try:
                pygame.mixer.music.stop()
                if self.load_current_track():
                    pygame.mixer.music.play()
                    self.model.start_time = time.time() - new_position
                    print(f"⏩ Avanzando a {new_position:.1f}s (fallback)")
            except:
                print(f"Error al avanzar: {e}")

    def rewind(self):
        """Retrocede 10 segundos en la canción."""
        if not pygame.mixer.music.get_busy() or not hasattr(self.model, 'start_time'):
            return
            
        try:
            # Calcular posición actual y nueva posición
            current_elapsed = time.time() - self.model.start_time
            new_position = max(current_elapsed - 10, 0)
            
            # Detener la música actual
            pygame.mixer.music.stop()
            
            # Recargar la canción
            if self.load_current_track():
                # Reproducir desde la nueva posición ajustando el start_time
                pygame.mixer.music.play(start=new_position)
                self.model.start_time = time.time() - new_position
                print(f"⏪ Retrocediendo a {new_position:.1f}s")
        except Exception as e:
            # Fallback: recargar y ajustar tiempo manualmente
            try:
                pygame.mixer.music.stop()
                if self.load_current_track():
                    pygame.mixer.music.play()
                    self.model.start_time = time.time() - new_position
                    print(f"⏪ Retrocediendo a {new_position:.1f}s (fallback)")
            except:
                print(f"Error al retroceder: {e}")

    def sync_progress(self):
        """Sincroniza la barra de progreso con la reproducción de audio."""
        if pygame.mixer.music.get_busy() and hasattr(self.model, 'track_duration'):
            # Calcular progreso basado en el tiempo transcurrido
            if hasattr(self.model, 'start_time'):
                elapsed_time = time.time() - self.model.start_time
                if self.model.track_duration > 0:
                    progress_percent = min((elapsed_time / self.model.track_duration) * 100, 100)
                    self.view.update_progress(progress_percent)
                    self.view.update_time_display(elapsed_time, self.model.track_duration)
        elif not pygame.mixer.music.get_busy() and hasattr(self.model, 'track_duration'):
            # Si la canción terminó, pasar a la siguiente automáticamente
            if not self.is_paused and self.model.playlist and len(self.model.playlist) > 1:
                self.next_track()

        self.ventana.after(500, self.sync_progress)  # Llamar cada 500ms

    def set_volume(self, value):
        """Ajusta el volumen de la música."""
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

