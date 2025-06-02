import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pygame
import time
from Tooltip import Tooltip

class WMPView:
    def __init__(self, ventana, controller):
        self.ventana = ventana
        self.controller = controller

        # Crear Frame principal
        self.framePrincipal = tk.Frame(self.ventana, width=800, height=600)
        self.framePrincipal.pack(fill='both', expand=True)

        # Cargar imagen de fondo optimizada
        self.fondo_label = tk.Label(self.framePrincipal)
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background(r'WhatsApp-Image-2025-05-30-at-7.41.37-PM.png')

        # Crear área para mostrar información de la canción
        self.info_frame = tk.Frame(self.framePrincipal, bg="#1a1a1a", width=600, height=80)
        self.info_frame.place(x=100, y=70)

        # Etiqueta para el nombre de la canción
        self.track_name_label = tk.Label(
            self.info_frame, 
            text="Sin canción cargada", 
            font=("Arial", 14, "bold"), 
            fg="#00aaff", 
            bg="#1a1a1a",
            wraplength=580
        )
        self.track_name_label.place(x=10, y=10)

        # Etiqueta para información adicional
        self.track_info_label = tk.Label(
            self.info_frame, 
            text="Selecciona una canción o carpeta para comenzar", 
            font=("Arial", 10), 
            fg="white", 
            bg="#1a1a1a",
            wraplength=580
        )
        self.track_info_label.place(x=10, y=40)

        # Crear barra de progreso minimalista
        self.progress_frame = tk.Frame(self.framePrincipal, bg="#1c1c1c", width=600, height=30)
        self.progress_frame.place(x=100, y=420)

        self.progress_canvas = tk.Canvas(self.progress_frame, bg="#1c1c1c", width=600, height=30, highlightthickness=0)
        self.progress_canvas.pack(fill="both", expand=True)

        # Dibujar la barra de progreso y la bolita azul
        self.progress_bar = self.progress_canvas.create_rectangle(0, 14, 600, 16, fill="#004c90", outline="")
        self.progress_circle = self.progress_canvas.create_oval(-5, 5, 15, 25, fill="#00aaff", outline="")

        # Crear etiqueta para mostrar tiempo transcurrido y duración
        self.time_label = tk.Label(self.framePrincipal, text="00:00 / 00:00", font=("Arial", 12), fg="white", bg="black")
        self.time_label.place(x=350, y=390)
        Tooltip(self.time_label, "Tiempo transcurrido / duración total")


        # Cargar imágenes redondas para los botones
        icon_paths = {
            "play": r'iconos reproductor\play.png',
            "pause": r'iconos reproductor\pause.png',
            "stop": r'iconos reproductor\stop.png',
            "next": r'iconos reproductor\next.png',
            "prev": r'iconos reproductor\prev.png',
            "forward": r'iconos reproductor\forward.png',
            "rewind": r'iconos reproductor\rewind.png'
        }
        
        self.icons = {key: self.create_round_button_image(path, 40) for key, path in icon_paths.items()}
        
        # Crear botones con imágenes circulares
        self.buttons = {
            "play": self.create_button(self.icons["play"], self.controller.play),
            "pause": self.create_button(self.icons["pause"], self.controller.pause),
            "stop": self.create_button(self.icons["stop"], self.controller.stop),
            "next": self.create_button(self.icons["next"], self.controller.next_track),
            "prev": self.create_button(self.icons["prev"], self.controller.prev_track),
            "forward": self.create_button(self.icons["forward"], self.controller.forward),
            "rewind": self.create_button(self.icons["rewind"], self.controller.rewind)
        }
        
        # Botón para cargar música
        self.load_icon = self.create_round_button_image(r'iconos reproductor\library.png', 40)
        self.load_button = self.create_button(self.load_icon, self.controller.load_track)
        self.load_button.place(x=200, y=460, width=40, height=40)
        Tooltip(self.load_button, "Presione para cargar canciones desde archivo.")
                
        # Ubicar botones en la interfaz
        positions = {
            "play": (450, 460), "pause": (350, 460), "stop": (400, 460),
            "next": (550, 465), "prev": (250, 465), "forward": (500, 465), "rewind": (310, 465)
        }
        for key, (x, y) in positions.items():
            self.buttons[key].place(x=x, y=y, width=40, height=40 if key in ["play", "pause", "stop"] else 30)
            Tooltip(self.buttons["play"], "Reproducir [Alt + R]")
            Tooltip(self.buttons["pause"], "Pausar [Alt + P]")
            Tooltip(self.buttons["stop"], "Detener [Alt + S]")
            Tooltip(self.buttons["next"], "Siguiente canción [Alt + N]")
            Tooltip(self.buttons["prev"], "Canción anterior [Alt + B]")
            Tooltip(self.buttons["forward"], "Avanzar 5s [→]")
            Tooltip(self.buttons["rewind"], "Retroceder 5s [←]")


        # Agregar control de volumen
        self.volume_label = tk.Label(self.framePrincipal, text="Volumen:", font=("Arial", 10), fg="white", bg="black")
        self.volume_label.place(x=280, y=520)
        
        
        self.volume_slider = tk.Scale(
            self.framePrincipal, 
            from_=0, 
            to=100, 
            orient="horizontal", 
            command=self.controller.set_volume,
            bg="#1c1c1c",
            fg="white",
            activebackground="#00aaff",
            highlightthickness=0
        )
        self.volume_slider.set(70)  # Volumen inicial
        self.volume_slider.place(x=350, y=510)
        Tooltip(self.volume_slider, "Ajustar volumen")


        # Vincular eventos del teclado (Hotkeys)
        self.ventana.bind("<Alt-r>", lambda event: self.controller.play())
        self.ventana.bind("<Alt-p>", lambda event: self.controller.pause())
        self.ventana.bind("<Alt-s>", lambda event: self.controller.stop())
        self.ventana.bind("<Alt-n>", lambda event: self.controller.next_track())
        self.ventana.bind("<Alt-b>", lambda event: self.controller.prev_track())
        self.ventana.bind("<Alt-l>", lambda event: self.controller.load_track())
        self.ventana.bind("<Right>", lambda event: self.controller.forward())
        self.ventana.bind("<Left>", lambda event: self.controller.rewind())
        self.ventana.bind("<space>", lambda event: self.toggle_play_pause())

        # Hacer que la ventana pueda recibir el foco para los hotkeys
        self.ventana.focus_set()

    def update_background(self, image_path):
        """Carga y optimiza la imagen de fondo."""
        try:
            fondo_imagen = Image.open(image_path).resize((800, 600))
            fondo_foto = ImageTk.PhotoImage(fondo_imagen)
            self.fondo_label.image = None  # Liberar memoria
            self.fondo_label.image = fondo_foto
            self.fondo_label.configure(image=fondo_foto)
        except Exception as e:
            print(f"Error al cargar imagen de fondo: {e}")

    def create_round_button_image(self, image_path, size):
        """Carga una imagen y la convierte en circular."""
        try:
            img = Image.open(image_path).convert("RGBA").resize((size, size))
            mask = Image.new("L", img.size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            img.putalpha(mask)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar icono {image_path}: {e}")
            # Crear un icono por defecto si falla
            return self.create_default_icon(size)

    def create_default_icon(self, size):
        """Crea un icono por defecto si no se puede cargar la imagen."""
        img = Image.new("RGBA", (size, size), (0, 170, 255, 255))
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    def create_button(self, icon, command):
        """Crea un botón redondo con una imagen."""
        button = tk.Button(
            self.framePrincipal, 
            image=icon, 
            command=command,
            borderwidth=0, 
            highlightthickness=0, 
            bg="black", 
            activebackground="gray",
            cursor="hand2"
        )
        button.image = icon  # Mantener referencia
        return button

    def update_progress(self, position):
        """Actualiza la posición de la bolita azul según el avance de la canción."""
        x_pos = max(0, min(int((position / 100) * 600), 600))  # Limitar movimiento
        self.progress_canvas.coords(self.progress_circle, x_pos-5, 5, x_pos+15, 25)

    def update_time_display(self, current_time, total_time):
        """Actualiza la visualización del tiempo."""
        current_str = time.strftime('%M:%S', time.gmtime(current_time))
        total_str = time.strftime('%M:%S', time.gmtime(total_time))
        self.time_label.config(text=f"{current_str} / {total_str}")

    def update_track_info(self, track_name):
        """Actualiza la información de la canción en la interfaz."""
        # Actualizar nombre de la canción
        self.track_name_label.config(text=track_name)
        
        # Actualizar información adicional
        if track_name != "Sin canción":
            playlist_info = f"Canción {self.controller.current_track_index + 1} de {len(self.controller.model.playlist)}"
            self.track_info_label.config(text=playlist_info)
        else:
            self.track_info_label.config(text="Selecciona una canción o carpeta para comenzar")

    def toggle_play_pause(self):
        """Alterna entre play y pause con la barra espaciadora."""
        if pygame.mixer.music.get_busy():
            self.controller.pause()
        else:
            self.controller.play()

    def sync_progress(self):
        """Sincroniza la barra de progreso con la reproducción de audio."""
        if pygame.mixer.music.get_busy():
            position = time.time() - self.controller.model.start_time  # Tiempo transcurrido
            duration = self.controller.model.track_duration

            if duration > 0:
                progress_percent = (position / duration) * 100
                self.update_progress(progress_percent)
                self.update_time_display(position, duration)

        self.ventana.after(500, self.sync_progress)