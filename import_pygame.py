import pygame
import random

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Cores
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
GREEN = (34, 139, 34)
GRAY = (180, 180, 180)
YELLOW = (255, 223, 0)
PETAL_RED = (255, 20, 147)
SKIN_TONE = (255, 224, 189)

# Constantes
JUMP_HEIGHT = 100
PLATFORM_GAP = 90
BASE_FALL_SPEED = 2
INITIAL_PLATFORM_WIDTH = 100
MIN_PLATFORM_WIDTH = 30
NUM_PLATFORMS = 7

# ----------------------- FUNÇÕES DE FUNDO ----------------------- #
def init_clouds():
    clouds = []
    for _ in range(5):
        cloud = {
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT // 3),
            'speed': random.uniform(0.2, 0.5),
            'size': random.randint(30, 60)
        }
        clouds.append(cloud)
    return clouds

def update_clouds(clouds):
    for cloud in clouds:
        cloud['x'] -= cloud['speed']
        if cloud['x'] + cloud['size'] < 0:
            cloud['x'] = WIDTH
            cloud['y'] = random.randint(0, HEIGHT // 3)
            cloud['size'] = random.randint(30, 60)

def draw_background(surface, clouds):
    surface.fill(SKY_BLUE)
    for cloud in clouds:
        cloud_rect = pygame.Rect(int(cloud['x']), int(cloud['y']), int(cloud['size']), int(cloud['size'] // 2))
        pygame.draw.ellipse(surface, WHITE, cloud_rect)

# ----------------------- FUNÇÃO DE DESENHO DA GAROTINHA ----------------------- #
def draw_girl(surface, x, bottom, jumping, vel_y, vel_x):
    head_radius = 8
    head_center = (x, bottom - 50)
    pygame.draw.circle(surface, SKIN_TONE, head_center, head_radius)
    hair_rect = pygame.Rect(x - head_radius, head_center[1] - head_radius, head_radius * 2, head_radius)
    pygame.draw.ellipse(surface, BLACK, hair_rect)
    ponytail_base = (x + head_radius - 2, head_center[1])
    ponytail_points = [
        ponytail_base,
        (ponytail_base[0] + 5 + vel_x * 0.5, ponytail_base[1] + 4 - vel_y * 0.3),
        (ponytail_base[0] + 3 + vel_x * 0.3, ponytail_base[1] + 16 - vel_y * 0.5),
        (ponytail_base[0] - 1 + vel_x * 0.2, ponytail_base[1] + 10 - vel_y * 0.2)
    ]
    pygame.draw.polygon(surface, BLACK, ponytail_points)
    pygame.draw.circle(surface, WHITE, (x - 3, head_center[1] - 2), 1)
    pygame.draw.circle(surface, WHITE, (x + 3, head_center[1] - 2), 1)
    pygame.draw.arc(surface, BLACK, (x - 4, head_center[1], 8, 5), 3.14, 2 * 3.14, 1)
    dress_top = bottom - 45
    point_left_shoulder = (x - 12, dress_top)
    point_right_shoulder = (x + 12, dress_top)
    point_right_waist = (x + 8, bottom - 5)
    point_center_bottom = (x, bottom + 5)
    point_left_waist = (x - 8, bottom - 5)
    dress_points = [point_left_shoulder, point_right_shoulder, point_right_waist, point_center_bottom, point_left_waist]
    pygame.draw.polygon(surface, RED, dress_points)
    pygame.draw.lines(surface, DARK_RED, True, dress_points, 1)
    pygame.draw.line(surface, DARK_RED, (x - 8, bottom - 5), (x, bottom + 5), 1)
    pygame.draw.line(surface, DARK_RED, (x, bottom + 5), (x + 8, bottom - 5), 1)
    if jumping:
        pygame.draw.line(surface, SKIN_TONE, (x - 3, dress_top + 5), (x - 10, dress_top - 5), 2)
        pygame.draw.line(surface, SKIN_TONE, (x + 3, dress_top + 5), (x + 10, dress_top - 2), 2)
    else:
        pygame.draw.line(surface, SKIN_TONE, (x - 3, dress_top + 5), (x - 10, dress_top + 5), 2)
        pygame.draw.line(surface, SKIN_TONE, (x + 3, dress_top + 5), (x + 10, dress_top + 5), 2)
    if jumping:
        pygame.draw.line(surface, SKIN_TONE, (x - 3, bottom), (x - 6, bottom + 10), 2)
        pygame.draw.line(surface, SKIN_TONE, (x + 3, bottom), (x + 6, bottom + 10), 2)
    else:
        pygame.draw.line(surface, SKIN_TONE, (x - 3, bottom), (x - 3, bottom + 10), 2)
        pygame.draw.line(surface, SKIN_TONE, (x + 3, bottom), (x + 3, bottom + 10), 2)
    shoe_width, shoe_height = 4, 2
    left_shoe = pygame.Rect(x - 7, bottom + 10 - shoe_height, shoe_width, shoe_height)
    right_shoe = pygame.Rect(x + 3, bottom + 10 - shoe_height, shoe_width, shoe_height)
    pygame.draw.rect(surface, BLACK, left_shoe)
    pygame.draw.rect(surface, BLACK, right_shoe)

# ----------------------- CLASSE DA GAROTINHA ----------------------- #
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.speed = 5
        self.pong_timer = 0
        self.jumped = False

    def move(self, keys, platforms):
        global game_started, start_time
        if not game_started:
            if keys[pygame.K_UP] and self.on_ground:
                self.jumped = True
                self.vel_y = self.jump_power
        else:
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
                self.vel_x = -self.speed
            elif keys[pygame.K_RIGHT]:
                self.x += self.speed
                self.vel_x = self.speed
            else:
                self.vel_x = 0
            if keys[pygame.K_UP] and self.on_ground:
                self.vel_y = self.jump_power

        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0

        prev_on_ground = self.on_ground
        self.on_ground = False
        for platform in platforms:
            if (self.vel_y > 0 and
                    self.y >= platform.y and
                    self.y - self.vel_y <= platform.y + 2 and
                    platform.x <= self.x <= platform.x + platform.width):
                self.y = platform.y
                self.vel_y = 0
                self.on_ground = True
                if not prev_on_ground:
                    self.pong_timer = 10
                    if self.jumped and not game_started:
                        game_started = True
                        start_time = pygame.time.get_ticks() // 1000

    def draw(self):
        jumping = not self.on_ground
        draw_girl(screen, int(self.x), int(self.y), jumping, self.vel_y, self.vel_x)
        if self.pong_timer > 0:
            pong_text = font.render("pong", True, WHITE)
            text_rect = pong_text.get_rect(center=(self.x, int(self.y) - 30))
            screen.blit(pong_text, text_rect)
            self.pong_timer -= 1

# ----------------------- CLASSE DAS PLATAFORMAS ----------------------- #
class Platform:
    def __init__(self, x, y, width=INITIAL_PLATFORM_WIDTH, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flowers = self._generate_flowers()

    def _generate_flowers(self):
        flowers = []
        num_flowers = random.randint(1, 3)
        for _ in range(num_flowers):
            if self.width > 8:
                offset_x = random.randint(2, self.width - 2)
            else:
                offset_x = self.width // 2
            offset_y = -random.randint(2, 5)
            flowers.append((offset_x, offset_y))
        return flowers

    def update(self, dy):
        self.y += dy

    def draw(self):
        platform_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, GREEN, platform_rect)
        for offset in self.flowers:
            fx = self.x + offset[0]
            fy = self.y + offset[1]
            pygame.draw.circle(screen, YELLOW, (fx, fy), 2)
            pygame.draw.circle(screen, PETAL_RED, (fx - 2, fy), 1)
            pygame.draw.circle(screen, PETAL_RED, (fx + 2, fy), 1)
            pygame.draw.circle(screen, PETAL_RED, (fx, fy - 2), 1)
            pygame.draw.circle(screen, PETAL_RED, (fx, fy + 2), 1)

# ----------------------- FUNÇÕES AUXILIARES ----------------------- #
def generate_platforms():
    platforms = []
    number_of_platforms = NUM_PLATFORMS
    base_x = random.randint(50, WIDTH - INITIAL_PLATFORM_WIDTH - 50)
    base_y = HEIGHT - 50
    platforms.append(Platform(base_x, base_y, INITIAL_PLATFORM_WIDTH))
    prev_x = base_x
    prev_y = base_y

    for i in range(1, number_of_platforms):
        # Gera a nova posição da plataforma dentro do alcance do pulo
        new_x = random.randint(max(50, prev_x - JUMP_HEIGHT), min(WIDTH - INITIAL_PLATFORM_WIDTH - 50, prev_x + JUMP_HEIGHT))
        new_y = prev_y - random.randint(50, JUMP_HEIGHT)  # Garante que a plataforma esteja ao alcance vertical

        # Adiciona a nova plataforma
        platforms.append(Platform(new_x, new_y, INITIAL_PLATFORM_WIDTH))
        prev_x = new_x
        prev_y = new_y

    return platforms

def position_ball_on_platform(ball, platforms):
    bottom_platform = max(platforms, key=lambda p: p.y)
    ball.x = bottom_platform.x + bottom_platform.width // 2
    ball.y = bottom_platform.y
    ball.on_ground = True

def game_over_screen():
    screen.fill(BLACK)
    message = font.render("GAME OVER!", True, RED)
    retry_text = font.render("Retry", True, WHITE)
    retry_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 40)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 40))
    pygame.draw.rect(screen, GRAY, retry_rect)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_rect.collidepoint(mouse_pos):
                    return True # Sinaliza para reiniciar o jogo
            if event.type == pygame.KEYDOWN:
                return True # Sinaliza para reiniciar o jogo ao pressionar qualquer tecla
    return False

# ----------------------- INICIALIZAÇÃO ----------------------- #
def reset_game():
    global game_started, start_time, elapsed_time, score, clouds, ball, platforms, last_elapsed_time, dynamic_fall_speed, dynamic_platform_width
    game_started = False
    start_time = None
    elapsed_time = 0
    score = 0
    clouds = init_clouds()
    ball = Ball()
    platforms = generate_platforms()
    position_ball_on_platform(ball, platforms)
    last_elapsed_time = -1
    dynamic_fall_speed = BASE_FALL_SPEED
    dynamic_platform_width = INITIAL_PLATFORM_WIDTH

reset_game()

# ----------------------- LOOP PRINCIPAL DO JOGO ----------------------- #
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza o relógio
    clock.tick(60)

    if not game_over:
        # Atualiza e desenha o fundo
        update_clouds(clouds)
        draw_background(screen, clouds)

        # Movimenta e desenha a bola
        keys = pygame.key.get_pressed()
        ball.move(keys, platforms)
        ball.draw()

        # Atualiza o estado do jogo
        if game_started:
            current_elapsed_time = (pygame.time.get_ticks() // 1000) - start_time
            if current_elapsed_time > last_elapsed_time:
                elapsed_time = current_elapsed_time
                score += 1  # Incrementa o score a cada segundo
                dynamic_fall_speed = BASE_FALL_SPEED + (elapsed_time // 10)
                dynamic_platform_width = max(INITIAL_PLATFORM_WIDTH - 2 * (elapsed_time // 10), MIN_PLATFORM_WIDTH)
                last_elapsed_time = current_elapsed_time

            # Finaliza o jogo ao atingir 999 segundos
            if elapsed_time >= 999:
                game_over = True

            ball.y += dynamic_fall_speed

            # Atualiza a posição das plataformas
            for p in platforms:
                p.update(dynamic_fall_speed)

        # Desenha as plataformas
        for p in platforms:
            p.draw()

        # Remove plataformas fora da tela e adiciona novas
        platforms = [p for p in platforms if p.y < HEIGHT]
        while len(platforms) < NUM_PLATFORMS:
            new_width = dynamic_platform_width if game_started else INITIAL_PLATFORM_WIDTH
            new_x = random.randint(50, WIDTH - new_width - 50)
            new_y = platforms[-1].y - PLATFORM_GAP
            platforms.append(Platform(new_x, new_y, new_width))

        # Verifica se a bola caiu abaixo da tela
        if ball.y >= HEIGHT:
            game_over = True

        # Exibe o relógio e a pontuação
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 40))

        # Atualiza a tela
        pygame.display.flip()
    else:
        # Exibe a tela de "Game Over"
        if game_over_screen():
            reset_game()
            game_over = False
        else:
            running = False

pygame.quit()
