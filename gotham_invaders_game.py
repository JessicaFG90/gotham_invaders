# =============================================================================
# GOTHAM INVADERS
# Juego tipo Space Invaders con temática de Batman / Harley Quinn
# Desarrollado con Python y pygame
# Autora: Jessica Fort González
# =============================================================================

# =============================================================================
# IMPORTACIONES
# =============================================================================

import pygame # Librería principal para el desarrollo del videojuego
import random # Para generar posiciones y eventos aleatorios
import os # Para manejar rutas de archivos del sistema operativo
import numpy as np # Para generar el efecto de estática en la pantalla de Game Over

# =============================================================================
# CONFIGURACIÓN INICIAL DEL SISTEMA DE ARCHIVOS
# Obtiene la ruta absoluta de la carpeta donde está el script y establece
# esa carpeta como directorio de trabajo. Así, todas las rutas relativas
# (imágenes, sonidos, fuentes) funcionan independientemente de desde dónde
# se ejecute el programa.
# =============================================================================

carpeta_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(carpeta_script)

# =============================================================================
# INICIALIZACIÓN DE PYGAME
# pygame.init() activa todos los módulos de pygame (gráficos, sonido, eventos).
# Debe llamarse antes de usar cualquier otra función de pygame.
# =============================================================================

pygame.init()

# =============================================================================
# CONFIGURACIÓN DE LA VENTANA
# pygame.display.Info() obtiene información del monitor actual ANTES de crear
# la ventana. current_w y current_h devuelven la resolución nativa del monitor.
# pygame.FULLSCREEN crea la ventana a pantalla completa con esas dimensiones,
# adaptándose automáticamente a cualquier resolución sin deformar el contenido.
# =============================================================================

info = pygame.display.Info()
ANCHO = info.current_w # Anchura nativa del monitor en píxeles
ALTO  = info.current_h # Altura nativa del monitor en píxeles
VENTANA = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("🏙 GOTHAM INVADERS 🏙") # Título que aparece en la barra superior de la ventana

# =============================================================================
# PALETA DE COLORES
# Los colores en pygame se definen como tuplas RGB (Rojo, Verde, Azul),
# con valores entre 0 y 255 para cada canal.
# =============================================================================

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
FUCSIA = (255, 0, 255)
ROSA_PASTEL = (255, 182, 193)
AZUL_CLARO = (135, 206, 235)
MENTA = (152, 255, 152)
AMARILLO_PASTEL = (255, 255, 153)
LAVANDA = (230, 230, 250)
MELOCOTON = (255, 218, 185)

# =============================================================================
# RELOJ DEL JUEGO
# pygame.time.Clock() controla la velocidad de actualización del juego (FPS).
# Se usa clock.tick(60) en el bucle principal para limitar a 60 FPS,
# lo que garantiza que el juego vaya a la misma velocidad en todos los equipos.
# =============================================================================

clock = pygame.time.Clock()

# =============================================================================
# CARGA DE IMÁGENES
# pygame.image.load() carga una imagen desde disco y la convierte en una
# superficie de pygame que puede dibujarse en la ventana.
# Todas las imágenes están en la subcarpeta Img/.
# =============================================================================

fondo = pygame.image.load("Img/gotham.png") # Fondo de la ciudad de Gotham
jugador_img = pygame.image.load("Img/harley.png") # Sprite del jugador (Harley Quinn)
enemigo_img = pygame.image.load("Img/batman.png") # Sprite del enemigo (Batman)
bala_img = pygame.image.load("Img/bate.png") # Sprite del proyectil del jugador (bate de béisbol)
vidaLlena_img = pygame.image.load("Img/vida_llena.png") # Corazón lleno para el HUD de vidas
vidaVacia_img = pygame.image.load("Img/vida_vacia.png") # Corazón vacío para el HUD de vidas
murcielago_img = pygame.image.load("Img/murcielago.png") # Sprite del proyectil enemigo (murciélago)
potion_img = pygame.image.load("Img/potion_bottle_shine.png") # Sprite del power-up (poción de vida)

# =============================================================================
# CARGA DE SONIDOS
# pygame.mixer.Sound() carga efectos de sonido cortos que pueden reproducirse
# en cualquier momento con .play() y detenerse con .stop().
# Todos los sonidos están en la subcarpeta Sonidos/.
# =============================================================================

sonido_disparo = pygame.mixer.Sound("Sonidos/whoosh.mp3") # Sonido al disparar el bate
sonido_impacto = pygame.mixer.Sound("Sonidos/slime.mp3") # Sonido al impactar bala o colisión
sonido_pocion_cae = pygame.mixer.Sound("Sonidos/potion-music.wav") # Sonido mientras la poción cae
sonido_pocion_recoge = pygame.mixer.Sound("Sonidos/potion-drink.wav") # Sonido al recoger la poción
sonido_pocion_suelo = pygame.mixer.Sound("Sonidos/glitter-sparkle.mp3") # Sonido mientras la poción está en el suelo
sonido_next_level = pygame.mixer.Sound("Sonidos/level_complete.mp3") # Sonido al pasar de oleada

# =============================================================================
# ESCALADO DE IMÁGENES
# pygame.transform.scale() redimensiona una imagen a las dimensiones indicadas.
# pygame.transform.smoothscale() hace lo mismo pero con suavizado bilineal,
# lo que evita el efecto pixelado en imágenes escaladas.
# El fondo se escala al tamaño exacto de la ventana.
# =============================================================================

fondo = pygame.transform.scale(fondo, (ANCHO, ALTO)) # Fondo a pantalla completa
jugador_img = pygame.transform.smoothscale(jugador_img, (100, 100)) # Jugador: 100x100 px con suavizado
enemigo_img = pygame.transform.smoothscale(enemigo_img, (50, 50)) # Enemigo: 50x50 px con suavizado
bala_img = pygame.transform.smoothscale(bala_img, (50, 50)) # Bate: 50x50 px con suavizado
vidaLlena_img = pygame.transform.scale(vidaLlena_img, (19, 19)) # Corazón lleno: 19x19 px
vidaVacia_img = pygame.transform.scale(vidaVacia_img, (19, 19)) # Corazón vacío: 19x19 px
murcielago_img = pygame.transform.scale(murcielago_img, (50, 50)) # Murciélago: 50x50 px
potion_img = pygame.transform.scale(potion_img, (50, 50)) # Poción: 50x50 px

# =============================================================================
# MÚSICA DE FONDO
# pygame.mixer.music gestiona la música de fondo (diferente a los efectos).
# play(-1) reproduce la música en bucle infinito.
# set_volume() controla el volumen entre 0.0 (silencio) y 1.0 (máximo).
# La música se carga después de crear la ventana y las imágenes para que
# empiece a sonar en cuanto el jugador ve la pantalla del menú.
# =============================================================================

pygame.mixer.music.load("Sonidos/arcade.mp3") # Carga el archivo de música
pygame.mixer.music.play(-1) # Reproduce en bucle infinito

volumen = 0.7 # Volumen inicial al 70%
pygame.mixer.music.set_volume(volumen) # Aplica el volumen inicial

# =============================================================================
# DIMENSIONES DE SPRITES
# get_rect().size devuelve una tupla (ancho, alto) con las dimensiones
# de la imagen ya escalada. Se guardan en variables para usarlas en
# cálculos de posición y colisión a lo largo del código.
# =============================================================================

jugador_ancho, jugador_alto = jugador_img.get_rect().size # Dimensiones del jugador: (100, 100)
enemigo_ancho, enemigo_alto = enemigo_img.get_rect().size # Dimensiones del enemigo: (50, 50)

# =============================================================================
# CONFIGURACIÓN DEL JUGADOR
# El jugador se posiciona centrado horizontalmente y cerca del borde inferior.
# jugador_x: posición horizontal (se actualiza con las teclas izquierda/derecha)
# jugador_y: posición vertical (fija durante el juego)
# jugador_velocidad: píxeles que se mueve por frame al pulsar una tecla
# vidas: número de vidas iniciales del jugador
# =============================================================================

jugador_x = ANCHO // 2 - jugador_ancho // 2 # Centra horizontalmente al jugador
jugador_y = ALTO - jugador_alto - 20 # Lo sitúa 20px por encima del borde inferior
jugador_velocidad = 5 # Velocidad de movimiento en píxeles/frame
vidas = 3 # Número de vidas iniciales

# =============================================================================
# CONFIGURACIÓN DE LAS BALAS DEL JUGADOR
# balas: lista que contiene los proyectiles activos del jugador.
#        Cada bala es un diccionario con "x", "y" y "angulo".
# balas_enemigo: lista con los proyectiles activos de los enemigos.
#               Cada bala enemiga tiene "x", "y" y "velocidad".
# bala_ancho/bala_alto: dimensiones del hitbox de la bala (coinciden con el sprite 50x50).
# bala_velocidad: píxeles que sube la bala por frame.
# ultimo_disparo: timestamp del último disparo para el cooldown.
# cooldown_disparo: tiempo mínimo entre disparos en milisegundos.
# ultimo_dano: timestamp del último daño recibido para el cooldown de invencibilidad.
# cooldown_dano: tiempo de invencibilidad tras recibir daño en milisegundos.
# =============================================================================

balas = [] # Lista de balas activas del jugador
balas_enemigo = [] # Lista de balas activas de los enemigos
bala_ancho = 50 # Anchura del hitbox de la bala (igual que el sprite)
bala_alto = 50 # Altura del hitbox de la bala (igual que el sprite)
bala_velocidad = 7 # Píxeles que sube la bala por frame
ultimo_disparo = 0 # Timestamp del último disparo (milisegundos desde inicio pygame)
cooldown_disparo = 1000 # Cooldown entre disparos: 1 segundo (1000ms)
ultimo_dano = 0 # Timestamp del último daño recibido
cooldown_dano = 2000 # Invencibilidad tras daño: 2 segundos (2000ms)

# =============================================================================
# VARIABLES GENERALES DEL JUEGO
# fuente: fuente gótica usada en pantallas de Game Over y Victoria.
# powerups: lista de power-ups activos (pociones de vida).
# frame: contador de frames desde el inicio, usado para animaciones de parpadeo.
# =============================================================================

fuente = pygame.font.Font("Fuentes/Gothical.ttf", 30) # Fuente gótica tamaño 30 (reservada)
powerups = [] # Lista de power-ups activos en pantalla
frame = 0 # Contador de frames para animaciones

# =============================================================================
# CONFIGURACIÓN INICIAL DE ENEMIGOS
# num_enemigos: número de enemigos en la oleada actual.
#               Empieza en 0 porque la primera oleada se genera al detectar
#               que la lista enemigos está vacía (len(enemigos) == 0) en el
#               primer frame del bucle principal.
# oleada: número de oleada actual. Empieza en 0 por la misma razón.
# enemigos: lista de enemigos activos. Cada enemigo es un diccionario con:
#   - "x", "y": posición actual en píxeles
#   - "vel_x": velocidad horizontal (puede ser negativa para ir a la izquierda)
#   - "vel_y": velocidad vertical (0 en oleadas 1-5, positivo en oleadas 6-10)
#   - "ultimo_disparo_enemigo": timestamp del último disparo para el cooldown
# =============================================================================

num_enemigos = 0 # Se incrementa al generar cada oleada
oleada = 0 # Se incrementa cuando la lista enemigos queda vacía
enemigos = [] # Lista vacía; la primera oleada se genera en el primer frame

# Nota: el bucle de creación inicial está vacío (range(0)) porque num_enemigos = 0.
# Se mantiene por coherencia estructural con las oleadas siguientes.
for i in range(num_enemigos):
    enemigo_x = random.randint(0, ANCHO - enemigo_ancho)
    enemigo_y = random.randint(50, 200)
    enemigo_velocidad = 2
    enemigos.append({
        "x": enemigo_x,
        "y": enemigo_y,
        "vel_x": enemigo_velocidad,
        "vel_y": enemigo_velocidad * 0.5 if oleada >= 6 else 0,
        "ultimo_disparo_enemigo": 0
    })

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def dibujar_jugador(x, y):
    """
    Dibuja el sprite del jugador en la posición (x, y).
    VENTANA.blit() coloca una superficie (imagen) encima de otra.
    """
    VENTANA.blit(jugador_img, (x, y))

def dibujar_bala(x, y, angulo):
    """
    Dibuja el bate rotado en la posición (x, y).
    pygame.transform.rotate() devuelve una nueva imagen rotada el número
    de grados indicado. El ángulo aumenta 5 grados por frame para
    simular que el bate gira mientras vuela.
    """
    bala_rotada = pygame.transform.rotate(bala_img, angulo)
    VENTANA.blit(bala_rotada, (x, y))

def dibujar_enemigo(enemigo):
    """
    Dibuja el sprite del enemigo en su posición actual.
    Accede a las coordenadas desde el diccionario del enemigo.
    """
    VENTANA.blit(enemigo_img, (enemigo["x"], enemigo["y"]))

def dibujar_bala_enemigo(x, y):
    """
    Dibuja el sprite del murciélago (proyectil enemigo) en la posición (x, y).
    """
    VENTANA.blit(murcielago_img, (x, y))

def hay_colision(rect1, rect2):
    """
    Comprueba si dos rectángulos (pygame.Rect) se solapan.
    colliderect() devuelve True si hay intersección entre ambos rectángulos.
    Se usa para detectar colisiones entre balas y enemigos, balas enemigas
    y el jugador, enemigos y el jugador, y power-ups y el jugador.
    """
    return rect1.colliderect(rect2)

def actualizar_volumen_efectos(volumen):
    """
    Actualiza el volumen de todos los efectos de sonido simultáneamente.
    Se llama cada vez que el jugador pulsa + o - para cambiar el volumen,
    aplicando el mismo nivel a todos los sonidos del juego.
    pygame.mixer.music.set_volume() controla la música de fondo por separado.
    """
    sonido_disparo.set_volume(volumen)
    sonido_impacto.set_volume(volumen)
    sonido_pocion_cae.set_volume(volumen)
    sonido_pocion_recoge.set_volume(volumen)
    sonido_pocion_suelo.set_volume(volumen)
    sonido_next_level.set_volume(volumen)

def mostrar_tabla(puntuaciones_ordenadas):
    """
    Muestra la pantalla del Top 10 de puntuaciones.
    Lee las puntuaciones ya ordenadas y las presenta en columnas
    con posiciones X fijas para evitar desalineaciones causadas
    por fuentes proporcionales.
    El bucle while True mantiene la pantalla hasta que el jugador
    pulsa cualquier tecla o cierra la ventana.
    """
    fuente_tabla = pygame.font.Font("Fuentes/ari.ttf", 25) # Fuente pixel para las filas
    fuente_titulo = pygame.font.Font("Fuentes/Gothical.ttf", 80) # Fuente gótica para el título

    while True:
        VENTANA.fill(NEGRO) # Fondo negro

        # Título centrado en la parte superior
        titulo = fuente_titulo.render("TOP TEN PUNTUACIONES", True, ROJO)
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

        # Cabecera de columnas con posiciones X fijas
        VENTANA.blit(fuente_tabla.render("POS", True, BLANCO), (ANCHO // 2 - 400, 200))
        VENTANA.blit(fuente_tabla.render("NOMBRE", True, BLANCO), (ANCHO // 2 - 200, 200))
        VENTANA.blit(fuente_tabla.render("PUNTOS", True, BLANCO), (ANCHO // 2,       200))
        VENTANA.blit(fuente_tabla.render("TIEMPO", True, BLANCO), (ANCHO // 2 + 200, 200))
        VENTANA.blit(fuente_tabla.render("OLEADA", True, BLANCO), (ANCHO // 2 + 400, 200))

        # Filas de datos: enumerate() proporciona índice (i) y valor (linea)
        for i, linea in enumerate(puntuaciones_ordenadas):
            datos = linea.strip().split(",") # Separa los campos por coma
            if len(datos) == 4: # Solo procesa líneas con 4 campos válidos
                y_fila = 260 + i * 40 # Posición Y de cada fila (40px entre filas)
                VENTANA.blit(fuente_tabla.render(f"{i+1}", True, AMARILLO_PASTEL), (ANCHO // 2 - 400, y_fila))
                VENTANA.blit(fuente_tabla.render(datos[0], True, AMARILLO_PASTEL), (ANCHO // 2 - 200, y_fila))
                VENTANA.blit(fuente_tabla.render(datos[1], True, AMARILLO_PASTEL), (ANCHO // 2, y_fila))
                VENTANA.blit(fuente_tabla.render(f"{datos[2]}s", True, AMARILLO_PASTEL), (ANCHO // 2 + 200, y_fila))
                VENTANA.blit(fuente_tabla.render(datos[3], True, AMARILLO_PASTEL), (ANCHO // 2 + 400, y_fila))

        # Instrucción para salir
        texto_salir = fuente_tabla.render("Pulsa cualquier tecla para salir", True, BLANCO)
        VENTANA.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, ALTO - 50))

        pygame.display.flip() # Actualiza la pantalla
        clock.tick(60) # Limita a 60 FPS

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:
                pygame.quit()
                exit()

# =============================================================================
# VARIABLES DE ESTADO DEL JUEGO
# Se definen antes del bucle principal para que estén disponibles en todo
# el flujo del programa (bucle principal, pantallas finales, tabla).
# =============================================================================

ejecutando = True # Controla el bucle principal; False detiene el juego
salir_juego = False # True si el jugador cierra la ventana con la X durante la partida
pausado = False # True mientras el juego está en pausa (tecla ESC)
puntuaje = 0 # Puntuación acumulada (1 punto por enemigo eliminado)
game_over = False # True si el jugador pierde todas las vidas
victoria = False # True si el jugador completa las 10 oleadas

fuente_hud = pygame.font.Font("Fuentes/ari.ttf", 20) # Fuente pixel tamaño 20 para el HUD
fuente_hud_grande = pygame.font.Font("Fuentes/ari.ttf", 80) # Fuente pixel tamaño 80 para nombre
tiempo_inicio = pygame.time.get_ticks() # Timestamp de inicio para el temporizador

# =============================================================================
# MENÚ PRINCIPAL
# Muestra el título del juego, instrucciones y control de volumen.
# El bucle while True + else/continue/break es el patrón estándar de pygame
# para salir de un bucle for-evento desde dentro — sin él, el break del
# for solo rompería el for, no el while.
# =============================================================================

while True:
    VENTANA.blit(fondo, (0, 0)) # Dibuja el fondo de Gotham

    # Título principal
    fuente_grande = pygame.font.Font("Fuentes/Gothical.ttf", 250)
    texto = fuente_grande.render("GOTHAM INVADERS", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

    # Instrucción para empezar
    texto_inicio = fuente_hud.render("Pulsa ENTER para jugar", True, BLANCO)
    VENTANA.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, ALTO // 2 + 150))

    # Indicador de volumen con fondo semitransparente para legibilidad
    texto_volumen = fuente_hud.render(f"Volumen: {int(volumen * 100)}%  [+/-]", True, BLANCO)
    ancho_texto = texto_volumen.get_width()
    superficie_fondo = pygame.Surface((ancho_texto + 20, 35), pygame.SRCALPHA) # SRCALPHA permite transparencia
    superficie_fondo.fill((0, 0, 0, 150)) # Negro con 150/255 de opacidad
    VENTANA.blit(superficie_fondo, (ANCHO // 2 - ancho_texto // 2 - 10, ALTO // 2 + 242))
    VENTANA.blit(texto_volumen, (ANCHO // 2 - ancho_texto // 2, ALTO // 2 + 250))

    pygame.display.flip() # Muestra el frame dibujado
    clock.tick(60) # Limita a 60 FPS

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN: # Pulsando ENTER empieza el juego
                break
            if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                volumen = min(1.0, volumen + 0.1) # Sube el volumen (máximo 1.0)
                pygame.mixer.music.set_volume(volumen)
                actualizar_volumen_efectos(volumen)
            if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                volumen = max(0.0, volumen - 0.1) # Baja el volumen (mínimo 0.0)
                pygame.mixer.music.set_volume(volumen)
                actualizar_volumen_efectos(volumen)
    else:
        continue # Si el for terminó sin break, continúa el while
    break # Si el for terminó con break (ENTER pulsado), sale del while

# =============================================================================
# BUCLE PRINCIPAL DEL JUEGO
# Se ejecuta 60 veces por segundo mientras ejecutando sea True.
# Cada iteración: procesa eventos → actualiza lógica → dibuja en pantalla.
# =============================================================================

while ejecutando:

    clock.tick(60) # Limita a 60 FPS para velocidad consistente
    tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000 # Segundos transcurridos
    frame += 1 # Incrementa el contador de frames para animaciones de parpadeo

    # -------------------------------------------------------------------------
    # PROCESADO DE EVENTOS
    # pygame.event.get() devuelve todos los eventos pendientes (teclado, ratón,
    # cierre de ventana, etc.). Se procesan en un único for para evitar que
    # pygame los descarte si hay dos bucles de eventos en el mismo frame.
    # -------------------------------------------------------------------------

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # El jugador cierra la ventana con la X
            ejecutando = False
            salir_juego = True # Marca que la salida fue manual (no Game Over ni Victoria)

        if evento.type == pygame.KEYDOWN: # Pulsar + para subir el volumen y - para bajarlo
            if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                volumen = min(1.0, volumen + 0.1)
                pygame.mixer.music.set_volume(volumen)
                actualizar_volumen_efectos(volumen)

            if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                volumen = max(0.0, volumen - 0.1)
                pygame.mixer.music.set_volume(volumen)
                actualizar_volumen_efectos(volumen)

            if evento.key == pygame.K_SPACE: # Disparo del jugador
                tiempo_ahora = pygame.time.get_ticks()
                if tiempo_ahora - ultimo_disparo >= cooldown_disparo: # Comprueba cooldown
                    sonido_disparo.play()
                    balas.append({
                        "x": jugador_x + jugador_ancho // 2 - bala_ancho // 2, # Centrado respecto al jugador
                        "y": jugador_y, # Sale desde la posición vertical del jugador
                        "angulo": 0 # Ángulo inicial de rotación
                    })
                    ultimo_disparo = tiempo_ahora # Actualiza el timestamp del último disparo

            if evento.key == pygame.K_ESCAPE: # Pausa/reanuda el juego
                pausado = not pausado # Alterna entre True y False

    # -------------------------------------------------------------------------
    # PANTALLA DE PAUSA
    # Mientras pausado sea True, el bucle principal se congela aquí.
    # El while pausado tiene su propio bucle de eventos para detectar
    # ESC (reanudar), permitir ajuste de volumen durante la pausa y
    # Q (salir del juego).
    # -------------------------------------------------------------------------

    while pausado:
        VENTANA.blit(fondo, (0, 0)) # Fondo de Gotham detrás del menú de pausa

        # Texto de pausa centrado
        fuente_grande = pygame.font.Font("Fuentes/Gothical.ttf", 170)
        texto = fuente_grande.render("PAUSA", True, BLANCO)
        VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

        # Instrucción para reanudar
        texto_reanudar = fuente_hud.render("Pulsa ESC para reanudar la partida", True, BLANCO)
        VENTANA.blit(texto_reanudar, (ANCHO // 2 - texto_reanudar.get_width() // 2, ALTO // 2 + 120))
        
        # Instrucción para salir del juego
        texto_salir = fuente_hud.render("Pulsa Q para salir del juego", True, ROJO)
        VENTANA.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, ALTO // 2 + 160))

        # Control de volumen con fondo semitransparente
        texto_volumen = fuente_hud.render(f"Volumen: {int(volumen * 100)}%  [+/-]", True, BLANCO)
        ancho_texto = texto_volumen.get_width()
        superficie_fondo = pygame.Surface((ancho_texto + 20, 35), pygame.SRCALPHA)
        superficie_fondo.fill((0, 0, 0, 150))
        VENTANA.blit(superficie_fondo, (ANCHO // 2 - ancho_texto // 2 - 10, ALTO // 2 + 242))
        VENTANA.blit(texto_volumen, (ANCHO // 2 - ancho_texto // 2, ALTO // 2 + 250))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                    volumen = min(1.0, volumen + 0.1)
                    pygame.mixer.music.set_volume(volumen)
                    actualizar_volumen_efectos(volumen)
                if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    volumen = max(0.0, volumen - 0.1)
                    pygame.mixer.music.set_volume(volumen)
                    actualizar_volumen_efectos(volumen)
                if evento.key == pygame.K_ESCAPE:
                    pausado = False # Sale del while pausado y reanuda el juego
                if evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

    # -------------------------------------------------------------------------
    # MOVIMIENTO DEL JUGADOR
    # pygame.key.get_pressed() devuelve el estado actual de todas las teclas.
    # A diferencia de los eventos KEYDOWN (que se disparan una vez),
    # get_pressed() detecta si la tecla está siendo mantenida pulsada,
    # lo que permite movimiento continuo y suave.
    # -------------------------------------------------------------------------

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jugador_x -= jugador_velocidad # Mueve a la izquierda restando velocidad
    if teclas[pygame.K_RIGHT]:
        jugador_x += jugador_velocidad # Mueve a la derecha sumando velocidad

    # Limita al jugador dentro de los bordes horizontales de la ventana
    if jugador_x < 0:
        jugador_x = 0 # No puede salir por la izquierda
    if jugador_x + jugador_ancho > ANCHO:
        jugador_x = ANCHO - jugador_ancho # No puede salir por la derecha

    # -------------------------------------------------------------------------
    # MOVIMIENTO DE LAS BALAS DEL JUGADOR
    # balas[:] crea una copia de la lista para poder eliminar elementos
    # mientras se itera — si se iterase sobre la lista original y se
    # eliminase un elemento, Python se saltaría el siguiente.
    # -------------------------------------------------------------------------

    for bala in balas[:]:
        bala["y"] -= bala_velocidad # La bala sube (resta en Y porque Y aumenta hacia abajo)
        bala["angulo"] += 5 # Rota 5 grados por frame para efecto de giro
        if bala["y"] + bala_alto < 0: # Si la bala sale por arriba de la pantalla...
            balas.remove(bala) # ...se elimina de la lista

    # -------------------------------------------------------------------------
    # MOVIMIENTO DE ENEMIGOS Y DETECCIÓN DE COLISIONES
    # jugador_rect se calcula una vez fuera del for para que esté disponible
    # tanto en las colisiones enemigo-jugador como en las de bala enemiga-jugador.
    # -------------------------------------------------------------------------

    jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)

    for enemigo in enemigos[:]: # Copia de la lista para poder eliminar enemigos
        # Actualiza posición del enemigo según sus velocidades
        enemigo["x"] += enemigo["vel_x"] # Movimiento horizontal
        enemigo["y"] += enemigo["vel_y"] # Movimiento vertical (0 en oleadas 1-5)

        # Rebote horizontal: invierte vel_x al tocar los bordes izquierdo o derecho
        # En oleadas 1-5 (vel_y = 0), además baja 20px al rebotar (movimiento clásico Space Invaders)
        if enemigo["x"] <= 0 or enemigo["x"] + enemigo_ancho >= ANCHO:
            enemigo["vel_x"] = -enemigo["vel_x"]
            if enemigo["vel_y"] == 0:
                enemigo["y"] += 40 # Solo baja 40px si no tiene movimiento diagonal

        # Rebote vertical: en oleadas 6-10, el enemigo rebota en el borde superior
        if enemigo["vel_y"] != 0 and enemigo["y"] <= 50:
            enemigo["vel_y"] = -enemigo["vel_y"] # Invierte la dirección vertical

        # Rectángulo de colisión del enemigo actual
        enemigo_rect = pygame.Rect(enemigo["x"], enemigo["y"], enemigo_ancho, enemigo_alto)

        # Disparo enemigo: probabilidad aleatoria con cooldown por enemigo individual
        # En oleadas 6-10 la probabilidad es menor (900 vs 450) para compensar
        # el movimiento diagonal que ya dificulta esquivarlos.
        probabilidad_disparo = 900 if oleada >= 6 else 450
        tiempo_ahora = pygame.time.get_ticks()
        if (random.randint(0, probabilidad_disparo) == 0 and
                tiempo_ahora - enemigo["ultimo_disparo_enemigo"] >= 2000):
            balas_enemigo.append({
                "x": enemigo["x"] + enemigo_ancho // 2, # Sale del centro del enemigo
                "y": enemigo["y"] + enemigo_alto, # Sale desde la parte inferior del enemigo
                "velocidad": 3 # Velocidad fija de caída
            })
            enemigo["ultimo_disparo_enemigo"] = tiempo_ahora # Actualiza el cooldown

        # Colisión bala-enemigo: se itera sobre balas[:] (copia) para poder eliminar.
        # El for-else de Python ejecuta el bloque else solo si el for termina sin break.
        # Si una bala impacta al enemigo, el break evita que el else se ejecute,
        # lo que previene que un enemigo ya eliminado siga comprobando colisiones.
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala["x"], bala["y"], bala_ancho, bala_alto)
            if hay_colision(bala_rect, enemigo_rect):
                sonido_impacto.play()
                puntuaje += 1 # Suma 1 punto por enemigo eliminado
                balas.remove(bala) # Elimina la bala que impactó
                enemigos.remove(enemigo) # Elimina al enemigo de la lista
                break # Sale del for bala (activa el else)
        else:
            # Solo se ejecuta si ninguna bala impactó al enemigo
            # Comprueba si el enemigo salió por abajo o tocó al jugador
            if enemigo["y"] > ALTO or hay_colision(jugador_rect, enemigo_rect):
                if hay_colision(jugador_rect, enemigo_rect):
                    tiempo_ahora = pygame.time.get_ticks()
                    if tiempo_ahora - ultimo_dano >= cooldown_dano: # Comprueba invencibilidad
                        vidas -= 1
                        ultimo_dano = tiempo_ahora
                        sonido_impacto.play()
                    if vidas == 0:
                        game_over = True
                        ejecutando = False
                        sonido_pocion_cae.stop()
                        sonido_pocion_suelo.stop()
                # Reposiciona al enemigo en la zona superior (tanto si tocó al jugador como si salió por abajo de la pantalla)
                enemigo["x"] = random.randint(0, ANCHO - enemigo_ancho)
                enemigo["y"] = random.randint(50, 150)
                if enemigo["vel_y"] != 0:
                    enemigo["vel_y"] = abs(enemigo["vel_y"]) # Asegura que vuelva a caer hacia abajo

    # -------------------------------------------------------------------------
    # MOVIMIENTO DE BALAS ENEMIGAS Y COLISIÓN CON EL JUGADOR
    # Este bucle está fuera del for enemigo para que cada bala se mueva
    # exactamente una vez por frame, independientemente del número de enemigos.
    # -------------------------------------------------------------------------

    for bala in balas_enemigo[:]:
        bala["y"] += bala["velocidad"] # La bala cae hacia abajo (suma en Y)
        if bala["y"] > ALTO: # Si sale por abajo de la pantalla...
            balas_enemigo.remove(bala) # ...se elimina

        bala_rect = pygame.Rect(bala["x"], bala["y"], bala_ancho, bala_alto)
        if hay_colision(bala_rect, jugador_rect):
            sonido_impacto.play()
            vidas -= 1
            balas_enemigo.remove(bala) # Elimina la bala al impactar
            if vidas == 0:
                game_over = True
                ejecutando = False
                sonido_pocion_cae.stop()
                sonido_pocion_suelo.stop()

    # -------------------------------------------------------------------------
    # GESTIÓN DE OLEADAS
    # Cuando la lista de enemigos queda vacía, se incrementa el contador de
    # oleada. Si supera 10, activa la victoria. Si no, genera una nueva oleada
    # con más enemigos y mayor velocidad.
    # A partir de la oleada 6, los enemigos se mueven en diagonal (vel_y != 0)
    # y solo se añade 1 enemigo por oleada en lugar de 2.
    # A partir de la oleada 2, aparecen 2 power-ups de poción por oleada.
    # -------------------------------------------------------------------------

    if len(enemigos) == 0:
        oleada += 1
        balas_enemigo.clear() # Limpia las balas enemigas al cambiar de oleada

        if oleada > 10: # El jugador ha completado las 10 oleadas
            ejecutando = False
            victoria = True
            sonido_pocion_cae.stop()
            sonido_pocion_suelo.stop()
        else:
            sonido_next_level.play() if oleada > 1 else None # Sonido de nuevo nivel desde la oleada 2 hasta la 10.

            # A partir de la oleada 6, solo se añade 1 enemigo por oleada
            if oleada >= 6:
                num_enemigos += 1
            else:
                num_enemigos += 2

            # Genera los enemigos de la nueva oleada
            for i in range(num_enemigos):
                enemigo_x = random.randint(0, ANCHO - enemigo_ancho)
                enemigo_y = random.randint(50, 200)
                enemigo_velocidad = 1 + oleada * 0.4 # La velocidad aumenta gradualmente con la oleada
                enemigos.append({
                    "x": enemigo_x,
                    "y": enemigo_y,
                    "vel_x": enemigo_velocidad,
                    "vel_y": enemigo_velocidad * 0.5 if oleada >= 6 else 0, # Diagonal desde oleada 6
                    "ultimo_disparo_enemigo": 0
                })

            # Genera 2 power-ups a partir de la oleada 2
            if oleada >= 2:
                sonido_pocion_cae.stop() # Por si había una poción activa al cambiar de oleada
                sonido_pocion_suelo.stop()
                powerups.clear() # Elimina power-ups de la oleada anterior
                for i in range(2):
                    powerups.append({
                        "x": random.randint(0, ANCHO - 30),
                        "y": -30, # Empieza fuera de pantalla por arriba
                        "velocidad": 2,  # Velocidad de caída en píxeles/frame
                        # El primer power-up aparece 5s después del inicio de la oleada.
                        # El segundo aparece 20s después del primero (i * 20000ms).
                        "tiempo_aparicion": pygame.time.get_ticks() + 5000 + i * 20000,
                        "activo": False, # No visible hasta que llegue su tiempo_aparicion
                        "en_suelo": False, # True cuando ha llegado a la base del jugador
                        "tiempo_en_suelo": 0 # Timestamp para el temporizador de 7 segundos (desaparece 7 segundos después de tocar el suelo)
                    })

    # -------------------------------------------------------------------------
    # LÓGICA Y MOVIMIENTO DE POWER-UPS
    # Cada power-up tiene su propio ciclo de vida:
    # 1. Inactivo: esperando a que llegue su tiempo_aparicion
    # 2. Cayendo: se mueve hacia abajo hasta llegar a la base del jugador
    # 3. En suelo: permanece estático 7 segundos antes de desaparecer
    # El jugador puede recogerlo en cualquier fase 2 o 3.
    # -------------------------------------------------------------------------

    for powerup in powerups[:]:
        if pygame.time.get_ticks() >= powerup["tiempo_aparicion"]:
            if not powerup["activo"]: # Primera vez que se activa
                powerup["activo"] = True
                powerup["tiempo_activado"] = pygame.time.get_ticks()
                sonido_pocion_cae.play(-1) # Sonido en bucle mientras cae

            powerup["y"] += powerup["velocidad"] # Cae hacia abajo

            # Comprueba si ha llegado a la base del jugador
            if powerup["y"] + 50 > jugador_y + jugador_alto:
                powerup["y"] = jugador_y + jugador_alto - 50 # Lo fija en la base
                powerup["velocidad"] = 0 # Deja de moverse
                if not powerup["en_suelo"]: # Primera vez que toca el suelo
                    powerup["en_suelo"] = True
                    powerup["tiempo_en_suelo"] = pygame.time.get_ticks()
                    sonido_pocion_cae.stop() # Para el sonido de caída
                    sonido_pocion_suelo.play(-1) # Activa el sonido de suelo en bucle

            # Si lleva 7 segundos en el suelo, desaparece
            if powerup["en_suelo"]:
                if pygame.time.get_ticks() - powerup["tiempo_en_suelo"] >= 7000:
                    sonido_pocion_suelo.stop() # Para el sonido cuando desaparece
                    powerups.remove(powerup)
                    continue # Salta al siguiente powerup sin comprobar colisión

        # Comprueba si el jugador recoge el power-up
        powerup_rect = pygame.Rect(powerup["x"], powerup["y"], 50, 50)
        if hay_colision(powerup_rect, jugador_rect):
            sonido_pocion_cae.stop()
            sonido_pocion_recoge.play()
            sonido_pocion_suelo.stop()
            vidas += 1
            if vidas > 3:
                vidas = 3 # Máximo 3 vidas
            powerups.remove(powerup)
            continue

    # -------------------------------------------------------------------------
    # DIBUJADO EN PANTALLA
    # El orden de los blit() determina qué se dibuja encima de qué.
    # El fondo siempre va primero (capas más profundas) y el HUD al final
    # (capa más superficial, siempre visible encima de todo).
    # -------------------------------------------------------------------------

    VENTANA.blit(fondo, (0, 0)) # Fondo de Gotham
    dibujar_jugador(jugador_x, jugador_y) # Sprite del jugador

    # Power-ups con efecto de parpadeo: visible 10 frames, invisible 10 frames
    for powerup in powerups:
        if powerup["activo"]:
            if frame % 20 < 10: # Alterna cada 10 frames (a 60fps = ~3 veces/segundo)
                VENTANA.blit(potion_img, (powerup["x"], powerup["y"]))

    # Balas del jugador
    for bala in balas:
        dibujar_bala(bala["x"], bala["y"], bala["angulo"])

    # Sprites de los enemigos
    for enemigo in enemigos:
        dibujar_enemigo(enemigo)

    # Balas enemigas (murciélagos)
    for bala in balas_enemigo:
        dibujar_bala_enemigo(bala["x"], bala["y"])

    # HUD: vidas, puntuación, tiempo y oleada
    for i in range(3):
        if i < vidas:
            VENTANA.blit(vidaLlena_img, (20 + i * 25, 50)) # Corazón lleno
        else:
            VENTANA.blit(vidaVacia_img, (20 + i * 25, 50)) # Corazón vacío

    texto_puntuaje = fuente_hud.render(f"Puntos: {puntuaje}", True, BLANCO)
    VENTANA.blit(texto_puntuaje, (10, 20))

    texto_tiempo = fuente_hud.render(f"Tiempo de juego: {tiempo_actual}", True, BLANCO)
    VENTANA.blit(texto_tiempo, (ANCHO - 235, 20))

    texto_oleada = fuente_hud.render(f"Oleada actual: {oleada}", True, BLANCO)
    VENTANA.blit(texto_oleada, (ANCHO - 235, 50))

    pygame.display.flip() # Muestra en pantalla todo lo dibujado este frame

# =============================================================================
# SALIDA MANUAL (X de la ventana durante la partida)
# Si el jugador cerró la ventana con la X, salir_juego es True y el programa
# termina aquí sin mostrar ninguna pantalla final ni registrar puntuación.
# =============================================================================

if salir_juego:
    pygame.quit()
    exit()

# =============================================================================
# PANTALLA DE INTRODUCCIÓN DE NOMBRE
# El jugador introduce 3 letras para identificar su puntuación en la tabla.
# La interfaz muestra 3 líneas (una por letra) con estilo arcade:
# - La línea de la posición actual parpadea (frame % 60 < 30)
# - Al escribir una letra, la línea se sustituye por la letra
# - BACKSPACE borra la última letra introducida
# - El bucle termina automáticamente cuando se introducen las 3 letras
# =============================================================================

nombre_jugador = ""

while len(nombre_jugador) < 3:
    frame += 1
    VENTANA.fill(NEGRO)

    fuente_grande = pygame.font.Font("Fuentes/Gothical.ttf", 100)
    texto = fuente_grande.render("INTRODUCE TU NOMBRE", True, BLANCO)
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 150))

    for i in range(3):
        x_linea = ANCHO // 2 - 90 + i * 70 # Posición X de cada línea/letra
        y_linea = ALTO // 2 + 70 # Posición Y de las líneas

        if i < len(nombre_jugador):
            # Posición ya rellenada: muestra la letra
            letra = fuente_hud_grande.render(nombre_jugador[i], True, AMARILLO_PASTEL)
            VENTANA.blit(letra, (x_linea, ALTO // 2 + 10))
        elif i == len(nombre_jugador):
            # Posición actual: línea parpadeante (cursor)
            if frame % 60 < 30:
                pygame.draw.line(VENTANA, BLANCO, (x_linea, y_linea), (x_linea + 40, y_linea), 3)
        else:
            # Posición futura: línea fija
            pygame.draw.line(VENTANA, BLANCO, (x_linea, y_linea), (x_linea + 40, y_linea), 3)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1] # Elimina el último carácter
            elif len(nombre_jugador) < 3 and evento.unicode.isalpha():
                nombre_jugador += evento.unicode.upper() # Añade la letra en mayúsculas

    pygame.display.flip()
    clock.tick(60)

# =============================================================================
# GUARDADO Y LECTURA DE PUNTUACIONES
# Las puntuaciones se guardan en puntuaciones.txt con formato CSV (separado
# por comas, sin espacios) para facilitar su lectura y ordenación.
# Formato de cada línea: NOMBRE, PUNTOS, TIEMPO, OLEADA
# Se usa modo "a" (append) para no borrar las puntuaciones anteriores.
# obtener_puntos() extrae el campo PUNTOS de cada línea para ordenarlas.
# sorted() con reverse=True ordena de mayor a menor puntuación.
# [:10] limita el resultado a los 10 mejores.
# =============================================================================

with open("puntuaciones.txt", "a") as archivo:
    archivo.write(f"{nombre_jugador},{puntuaje},{tiempo_actual},{oleada - 1}\n")
    # oleada - 1 porque oleada se incrementó al detectar len(enemigos) == 0, por lo que su valor actual es 1 más que la última oleada jugada.

with open("puntuaciones.txt", "r") as archivo:
    puntuaciones = archivo.readlines() # Lee todas las líneas como lista de strings

def obtener_puntos(linea):
    """
    Función auxiliar para sorted(). Extrae el número de puntos de una línea
    del archivo de puntuaciones. El try/except maneja líneas malformadas
    devolviendo 0 para que se ordenen al final.
    """
    try:
        return int(linea.strip().split(",")[1]) # El índice 1 es el campo PUNTOS
    except:
        return 0

puntuaciones_ordenadas = sorted(puntuaciones, key=obtener_puntos, reverse=True)[:10]

# =============================================================================
# PANTALLA DE GAME OVER
# Fondo de estática de televisión generado con numpy:
# - np.random.randint crea un array 2D de valores aleatorios 0-255
# - np.stack duplica ese array en 3 canales (R, G, B iguales = escala de grises)
# - pygame.surfarray.make_surface convierte el array numpy en una superficie pygame
# El while not salir mantiene la pantalla hasta que el jugador pulsa una tecla.
# =============================================================================

if game_over:
    salir = False
    while not salir:
        # Genera un frame de estática de televisión en escala de grises
        ruido = np.random.randint(0, 255, (ANCHO, ALTO), dtype=np.uint8)
        ruido_rgb = np.stack([ruido, ruido, ruido], axis=2) # Mismo valor en R, G, B
        statica = pygame.surfarray.make_surface(ruido_rgb)
        VENTANA.blit(statica, (0, 0))

        fuente_grande = pygame.font.Font("Fuentes/Gothical.ttf", 200)
        texto = fuente_grande.render("GAME OVER", True, ROJO)
        VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

        texto_puntuaciones = fuente_hud.render("Pulsa cualquier tecla para ver las PUNTUACIONES", True, BLANCO)
        VENTANA.blit(texto_puntuaciones, (ANCHO // 2 - texto_puntuaciones.get_width() // 2, ALTO - 100))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                salir = True # Cualquier tecla sale de la pantalla de Game Over

    mostrar_tabla(puntuaciones_ordenadas)

# =============================================================================
# PANTALLA DE VICTORIA
# Animación de confeti: 100 partículas con posición, velocidad y color aleatorios.
# Cada partícula cae hacia abajo y reaparece por arriba al salir por el borde
# inferior, creando un efecto de lluvia de confeti continua.
# =============================================================================

elif victoria:
    confeti = []
    for _ in range(100): # El guión bajo _ indica que la variable del bucle no se usa
        confeti.append({
            "x": random.randint(0, ANCHO), # Posición horizontal aleatoria
            "y": random.randint(-ALTO, 0), # Empieza fuera de pantalla por arriba
            "velocidad": random.randint(2, 6), # Velocidad aleatoria (profundidad visual)
            "color": random.choice([ROSA_PASTEL, AZUL_CLARO, MENTA, AMARILLO_PASTEL, LAVANDA, MELOCOTON])
        })

    salir = False
    while not salir:
        VENTANA.fill(BLANCO) # Fondo blanco para la victoria

        for p in confeti:
            p["y"] += p["velocidad"] # Cae hacia abajo
            if p["y"] > ALTO: # Si sale por abajo...
                p["y"] = random.randint(-50, 0) # ...reaparece por arriba
                p["x"] = random.randint(0, ANCHO)
            pygame.draw.rect(VENTANA, p["color"], (p["x"], p["y"], 8, 8)) # Cuadrado de 8x8 px

        fuente_grande = pygame.font.Font("Fuentes/Gothical.ttf", 200)
        texto = fuente_grande.render("YOU WIN!", True, FUCSIA)
        VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

        texto_puntuaciones = fuente_hud.render("Pulsa cualquier tecla para ver las PUNTUACIONES", True, NEGRO)
        VENTANA.blit(texto_puntuaciones, (ANCHO // 2 - texto_puntuaciones.get_width() // 2, ALTO - 100))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                salir = True

    mostrar_tabla(puntuaciones_ordenadas)
