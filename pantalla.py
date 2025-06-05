import time
import digitalio
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ili9341

# Configuración de pines SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs_pin = digitalio.DigitalInOut(board.D8)    # GPIO8 (CE0)
dc_pin = digitalio.DigitalInOut(board.D25)   # GPIO25
reset_pin = digitalio.DigitalInOut(board.D24) # GPIO24

# Inicializar la pantalla
display = adafruit_ili9341.ILI9341(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    width=320,
    height=240,
    baudrate=24000000,
    rotation=90  # Rotación vertical
)

# Cargar fuentes (puedes cambiar el tamaño)
try:
    # Intenta cargar una fuente más grande
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except:
    # Si falla, usa las fuentes por defecto (más pequeñas)
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

def mostrar_mensaje_centrado(titulo, subtitulo="", color_fondo="navy", color_texto="white"):
    """Muestra un mensaje centrado en la pantalla"""
    imagen = Image.new("RGB", (display.height, display.width))
    dibujo = ImageDraw.Draw(imagen)
    
    # Dibujar fondo
    dibujo.rectangle((0, 0, display.height, display.width), fill=color_fondo)
    
    # Dibujar borde decorativo
    dibujo.rectangle((5, 5, display.height-5, display.width-5), outline="gold", width=3)
    
    # Calcular posiciones del texto
    ancho_titulo, alto_titulo = dibujo.textsize(titulo, font=font_large)
    ancho_sub, alto_sub = dibujo.textsize(subtitulo, font=font_medium) if subtitulo else (0, 0)
    
    # Dibujar título
    dibujo.text(
        ((display.height - ancho_titulo) // 2, (display.width - alto_titulo - alto_sub) // 2),
        titulo,
        font=font_large,
        fill=color_texto
    )
    
    # Dibujar subtítulo si existe
    if subtitulo:
        dibujo.text(
            ((display.height - ancho_sub) // 2, (display.width + alto_titulo - alto_sub) // 2 + 10),
            subtitulo,
            font=font_medium,
            fill=color_texto
        )
    
    # Mostrar en pantalla
    display.image(imagen)

def mostrar_mensaje_animado(titulo, subtitulo=""):
    """Muestra un mensaje con animación de entrada"""
    for i in range(0, 255, 5):
        imagen = Image.new("RGB", (display.height, display.width))
        dibujo = ImageDraw.Draw(imagen)
        
        # Fondo con transparencia simulada
        dibujo.rectangle((0, 0, display.height, display.width), fill=(i//2, i//3, i//4))
        
        # Texto que aparece gradualmente
        color_texto = (i, i, i) if i < 200 else (255, 255, 255)
        ancho_titulo, alto_titulo = dibujo.textsize(titulo, font=font_large)
        dibujo.text(
            ((display.height - ancho_titulo) // 2, (display.width - alto_titulo) // 2),
            titulo,
            font=font_large,
            fill=color_texto
        )
        
        if subtitulo and i > 100:
            color_sub = (min(i+50, 255), min(i+50, 255), min(i+50, 255))
            ancho_sub, alto_sub = dibujo.textsize(subtitulo, font=font_medium)
            dibujo.text(
                ((display.height - ancho_sub) // 2, (display.width + alto_titulo) // 2 + 10),
                subtitulo,
                font=font_medium,
                fill=color_sub
            )
        
        display.image(imagen)
        time.sleep(0.02)

def mostrar_mensaje_personalizado():
    """Muestra un mensaje con diseño más elaborado"""
    imagen = Image.new("RGB", (display.height, display.width))
    dibujo = ImageDraw.Draw(imagen)
    
    # Fondo degradado
    for y in range(display.width):
        r = int(50 + y/display.width*150)
        g = int(50 + y/display.width*100)
        b = int(150 - y/display.width*100)
        dibujo.line((0, y, display.height, y), fill=(r, g, b))
    
    # Marco decorativo
    dibujo.rectangle((10, 10, display.height-10, display.width-10), outline="white", width=2)
    dibujo.rectangle((15, 15, display.height-15, display.width-15), outline="gold", width=1)
    
    # Título principal
    titulo = "¡Bienvenido!"
    ancho_titulo, alto_titulo = dibujo.textsize(titulo, font=font_large)
    dibujo.text(
        ((display.height - ancho_titulo) // 2, 50),
        titulo,
        font=font_large,
        fill="white"
    )
    
    # Subtítulo
    subtitulo = "Sistema Raspberry Pi 4"
    ancho_sub, alto_sub = dibujo.textsize(subtitulo, font=font_medium)
    dibujo.text(
        ((display.height - ancho_sub) // 2, 100),
        subtitulo,
        font=font_medium,
        fill="gold"
    )
    
    # Mensaje adicional
    mensaje = "Pantalla TFT 320x240"
    ancho_msg, alto_msg = dibujo.textsize(mensaje, font=font_small)
    dibujo.text(
        ((display.height - ancho_msg) // 2, 150),
        mensaje,
        font=font_small,
        fill="white"
    )
    
    # Pie de página
    pie = "Inicializando sistema..."
    dibujo.text(
        (20, display.width - 30),
        pie,
        font=font_small,
        fill="silver"
    )
    
    # Mostrar en pantalla
    display.image(imagen)

# Mostrar diferentes mensajes de bienvenida
try:
    # Mensaje animado de entrada
    mostrar_mensaje_animado("Hola Mundo", "Raspberry Pi 4")
    time.sleep(2)
    
    # Mensaje con diseño centrado
    mostrar_mensaje_centrado("Bienvenido", "al sistema de control", "darkgreen", "white")
    time.sleep(2)
    
    # Mensaje personalizado más elaborado
    mostrar_mensaje_personalizado()
    time.sleep(3)
    
    # Mensaje final
    mostrar_mensaje_centrado("Listo!", "Sistema operativo", "purple", "white")
    
    print("Mensajes mostrados correctamente")

except KeyboardInterrupt:
    display.fill(0)
    print("Programa terminado")