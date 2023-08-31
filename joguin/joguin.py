import pygame
import random
import sys

# Inicialização do pygame
pygame.init()

# Configurações gerais
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Corrida")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Tela de início
def show_start_screen():
    font = pygame.font.Font(None, 64)
    title_text = font.render("Jogo de Corrida", True, BLACK)
    start_text = font.render("Pressione ESPAÇO para iniciar", True, BLACK)
    screen.fill(WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Tela de game over
def show_game_over_screen(score):
    font = pygame.font.Font(None, 64)
    game_over_text = font.render("Fim de jogo", True, BLACK)
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    restart_text = font.render("Clique R para reiniciar", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 150))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Configurações do jogador
player_width = 50
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Configurações dos obstáculos, moedas, relógio e velocidade
obstacle_radius = 25
obstacles = []
coin_radius = 15
coins = []
clock = pygame.time.Clock()
initial_speed = 2
speed_increment = 0.05
max_speed = 10
current_speed = initial_speed

# Estado do jogo
game_state = "start"  # Pode ser "start", "playing", ou "game over"

# Carregar imagem do balde (opcional, você pode removê-lo)
poop_image = pygame.image.load("bucket.png")

image_coin = pygame.image.load("coin.png")
coin_rect = image_coin.get_rect()

imagem_bosta = pygame.image.load("poop.png")
bosta_rect = imagem_bosta.get_rect()

# Loop do jogo
running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "start":
        show_start_screen()
        game_state = "playing"

    elif game_state == "playing":
        # Lógica do jogo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Atualização das moedas
        for coin in coins:
            coin[1] += current_speed
            if coin[1] > HEIGHT:
                coins.remove(coin)
                score += 1

        # Atualização dos obstáculos
        for obstacle in obstacles:
            obstacle[1] += current_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)

        # Geração aleatória de moedas
        if random.randint(0, 100) < 5:
            coins.append([random.randint(coin_radius, WIDTH - coin_radius), 0])

        # Geração aleatória de obstáculos
        if random.randint(0, 100) < 3:
            obstacles.append([random.randint(obstacle_radius, WIDTH - obstacle_radius), 0])

        # Colisões com moedas
        for coin in coins:
            if (
                player_x < coin[0] < player_x + player_width
                and player_y < coin[1] < player_y + player_height
            ):
                coins.remove(coin)
                score += 1

        # Colisões com obstáculos
        for obstacle in obstacles:
            if (
                player_x < obstacle[0] + obstacle_radius
                and player_x + player_width > obstacle[0]
                and player_y < obstacle[1] + obstacle_radius
                and player_y + player_height > obstacle[1]
            ):
                game_state = "game over"

        # Mudança de cor da tela de fundo
        screen.fill(BLACK)

        # Desenho das moedas
        for coin in coins:
            screen.blit(image_coin, (coin[0], coin[1]))

        # Desenho dos obstáculos como imagens de cocô
        for obstacle in obstacles:
            screen.blit(imagem_bosta, (obstacle[0], obstacle[1]))

        # Desenho do jogador (balde)
        screen.blit(poop_image, (player_x, player_y))

        # Mostrar pontuação
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        # Aumento gradual da velocidade até a velocidade máxima
        if current_speed < max_speed:
            current_speed += speed_increment

    elif game_state == "game over":
        show_game_over_screen(score)
        game_state = "start"  # Reiniciar o jogo

        # Aguardar clique do mouse para reiniciar
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    score = 0
                    obstacles.clear()
                    coins.clear()
                    current_speed = initial_speed

pygame.quit
