import pygame
import random

# Configuración de PyGame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalla Espacial: Carlos Jiménez")

# Colores y fuentes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(None, 36)

# Velocidad de actualización de FPS
FPS = 60
clock = pygame.time.Clock()

# Clase para la nave del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Clase para los enemigos (asteroides)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(3, 6)

# Clase para los proyectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:  # Eliminar el proyectil si sale de la pantalla
            self.kill()

# Función para mostrar el menú principal
def show_menu():
    screen.fill(BLACK)
    title_text = FONT.render("Batalla Espacial: Carlos Jiménez", True, WHITE)
    screen.blit(title_text, (WIDTH // 4, HEIGHT // 4))
    prompt_text = FONT.render("Presiona ENTER para empezar", True, WHITE)
    screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Función para mostrar el mensaje de fin del juego
def game_over():
    screen.fill(BLACK)
    game_over_text = FONT.render("¡Juego Terminado!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
    restart_text = FONT.render("Presiona ENTER para reiniciar o ESC para salir", True, WHITE)
    screen.blit(restart_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    main_game()  # Reiniciar el juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Función principal del juego
def main_game():
    # Crear grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Crear jugador
    player = Player()
    all_sprites.add(player)

    # Crear enemigos
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Variables del juego
    score = 0
    lives = 2
    running = True

    # Temporizador para agregar puntos cada 30 segundos
    start_time = pygame.time.get_ticks()  # Tiempo inicial en milisegundos

    while running:
        # Control de FPS
        clock.tick(FPS)

        # Tiempo transcurrido en milisegundos
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= 30000:  # Cada 30,000 ms (30 segundos)
            score += 10  # Sumar 10 puntos por cada 30 segundos
            start_time = pygame.time.get_ticks()  # Reiniciar el temporizador

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Disparar con barra espaciadora
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Actualización de sprites
        all_sprites.update()

        # Verificar colisiones entre proyectiles y enemigos
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 5  # Incrementar la puntuación por enemigo destruido
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Verificar colisiones entre el jugador y los enemigos
        if pygame.sprite.spritecollideany(player, enemies):
            lives -= 1
            if lives == 0:
                running = False  # Fin del juego

        # Dibujar en pantalla
        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = FONT.render(f"Puntuación: {score}", True, WHITE)
        lives_text = FONT.render(f"Vidas: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))

        pygame.display.flip()

    # Mostrar mensaje de fin del juego
    game_over()

# Bucle principal
show_menu()
main_game()
pygame.quit()
