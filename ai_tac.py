import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 3
CELL_SIZE = 150  # Set this to a smaller value to reduce board size
LINE_WIDTH = 10
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 20  # Updated for a more prominent look
CROSS_WIDTH = 30  # Updated for a more prominent look
SPACE = CELL_SIZE // 4
FPS = 60
NEON_COLORS = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 102, 102)]
RAIN_SPEED = 1

# Colors
BG_COLOR = (10, 10, 30)  # Dark, futuristic background color
LINE_COLOR = (0, 255, 255)  # Neon cyan for grid lines
CIRCLE_COLOR = (255, 20, 147)  # Neon pink/magenta for 'O'
CROSS_COLOR = (0, 255, 127)  # Neon green for 'X'

# Fonts
menu_font = pygame.font.Font('path_to_pixel_font.ttf', 40)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe Cyberpunk Edition")

# Load the pixelated background image
background = pygame.image.load('path_to_pixelated_background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Board positioning
board_x = (WIDTH - CELL_SIZE * GRID_SIZE) // 2
board_y = (HEIGHT - CELL_SIZE * GRID_SIZE) // 2

# Raindrop settings
raindrops = []
for _ in range(100):
    raindrops.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice(NEON_COLORS), random.randint(1, 3)])

# Board
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player = 'X'  # X starts first

#Firework particle settings
class FireworkParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.life = random.randint(20, 40)  # How long the particle lives
        self.speed_x = random.uniform(-4, 4)  # Horizontal speed
        self.speed_y = random.uniform(-4, 4)  # Vertical speed
        self.gravity = 0.1  # Gravity effect
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity  # Apply gravity
        self.life -= 1
    
    def draw(self):
        if self.life > 0:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Function to spawn fireworks
def spawn_fireworks(x, y, color):
    particles = []
    for _ in range(100):  # Number of particles per firework
        particles.append(FireworkParticle(x, y, color))
    return particles

# Update and draw the fireworks
def update_and_draw_fireworks(fireworks):
    for particle in fireworks:
        particle.update()
        particle.draw()

# Function to draw the neon rain
def draw_neon_rain():
    for drop in raindrops:
        pygame.draw.line(screen, drop[2], (drop[0], drop[1]), (drop[0], drop[1] + 10), 2)
        drop[1] += drop[3] * RAIN_SPEED
        if drop[1] > HEIGHT:
            drop[1] = random.randint(-20, -5)
            drop[0] = random.randint(0, WIDTH)

# Function to darken the background
def draw_background():
    screen.blit(background, (0, 0))
    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    dark_overlay.set_alpha(100)  # Change transparency as needed
    dark_overlay.fill((0, 0, 0))
    screen.blit(dark_overlay, (0, 0))

# Function to render text with a black box behind it and change appearance on hover
def draw_menu_text(text, pos, font, color=(255, 255, 255), hover=False):
    text_color = (200, 200, 200) if hover else color  # Darken the text color when hovered
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)
    
    # Darken the box color when hovered
    box_color = (20, 20, 20) if hover else (0, 0, 0)
    box_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(screen, box_color, box_rect)
    screen.blit(text_surface, text_rect)
    
    return text_rect

# Draw Tic-Tac-Toe Grid
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, 
                         (board_x, board_y + row * CELL_SIZE), 
                         (board_x + GRID_SIZE * CELL_SIZE, board_y + row * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, 
                         (board_x + row * CELL_SIZE, board_y), 
                         (board_x + row * CELL_SIZE, board_y + GRID_SIZE * CELL_SIZE), LINE_WIDTH)

# Draw Symbols (X or O)
def draw_figures():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (board_x + col * CELL_SIZE + CELL_SIZE // 2, board_y + row * CELL_SIZE + CELL_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (board_x + col * CELL_SIZE + SPACE, board_y + row * CELL_SIZE + CELL_SIZE - SPACE), 
                                 (board_x + col * CELL_SIZE + CELL_SIZE - SPACE, board_y + row * CELL_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (board_x + col * CELL_SIZE + SPACE, board_y + row * CELL_SIZE + SPACE), 
                                 (board_x + col * CELL_SIZE + CELL_SIZE - SPACE, board_y + row * CELL_SIZE + CELL_SIZE - SPACE), CROSS_WIDTH)

# Check for a Win
def check_win(player):
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check for a Draw
def check_draw():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True

# Handle AI Move (Random for now)
def ai_move():
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] is None]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'

# Game Over Screen
def game_over_screen(result):
    fireworks = []  # List to store all the fireworks particles
    firework_colors = [CIRCLE_COLOR, CROSS_COLOR, (255, 255, 0), (0, 255, 255)]  # Neon color scheme

    # Spawn initial fireworks (can be more than one)
    fireworks.extend(spawn_fireworks(WIDTH // 2, HEIGHT // 2, random.choice(firework_colors)))
    fireworks.extend(spawn_fireworks(WIDTH // 4, HEIGHT // 3, random.choice(firework_colors)))
    fireworks.extend(spawn_fireworks(3 * WIDTH // 4, 2 * HEIGHT // 3, random.choice(firework_colors)))

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_neon_rain()

        # Draw fireworks
        update_and_draw_fireworks(fireworks)

        # Show the winning text or draw message
        draw_menu_text(result, (WIDTH // 2, HEIGHT // 2 - 50), menu_font)
        draw_menu_text("Click to Restart", (WIDTH // 2, HEIGHT // 2 + 60), menu_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# Main Tic-Tac-Toe Game Loop (Human vs Human or AI)
def tic_tac_toe_game(vs_ai=False):
    global board, player
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player = 'X'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not vs_ai:
                mouse_x, mouse_y = event.pos
                clicked_row = (mouse_y - board_y) // CELL_SIZE
                clicked_col = (mouse_x - board_x) // CELL_SIZE

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player

                    if check_win(player):
                        game_over_screen(f"{player} Wins!")
                        return
                    elif check_draw():
                        game_over_screen("It's a Draw!")
                        return

                    player = 'O' if player == 'X' else 'X'

            if event.type == pygame.MOUSEBUTTONDOWN and vs_ai and player == 'X':
                mouse_x, mouse_y = event.pos
                clicked_row = (mouse_y - board_y) // CELL_SIZE
                clicked_col = (mouse_x - board_x) // CELL_SIZE

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player

                    if check_win(player):
                        game_over_screen(f"{player} Wins!")
                        return
                    elif check_draw():
                        game_over_screen("It's a Draw!")
                        return

                    player = 'O'
                    ai_move()

                    if check_win('O'):
                        game_over_screen("AI Wins!")
                        return
                    elif check_draw():
                        game_over_screen("It's a Draw!")
                        return

                    player = 'X'

        screen.fill(BG_COLOR)
        draw_neon_rain()
        draw_grid()
        draw_figures()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# Initialize dummy Rect objects before use
human_vs_human_rect = pygame.Rect(0, 0, 0, 0)
play_against_ai_rect = pygame.Rect(0, 0, 0, 0)
exit_rect = pygame.Rect(0, 0, 0, 0)

# Main Menu
def main_menu():
    global human_vs_human_rect, play_against_ai_rect, exit_rect  # Use global so we can modify them
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_vs_human_rect.collidepoint(mouse_pos):
                    tic_tac_toe_game(vs_ai=False)
                elif play_against_ai_rect.collidepoint(mouse_pos):
                    tic_tac_toe_game(vs_ai=True)
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
        
        draw_background()
        draw_neon_rain()

        # Detect if the mouse is hovering over any menu item
        hover_human_vs_human = human_vs_human_rect.collidepoint(mouse_pos)
        hover_play_against_ai = play_against_ai_rect.collidepoint(mouse_pos)
        hover_exit = exit_rect.collidepoint(mouse_pos)

        # Draw menu items with hover effect
        human_vs_human_rect = draw_menu_text("1. Play Against Human", (WIDTH // 2, HEIGHT // 2 - 50), menu_font, hover=hover_human_vs_human)
        play_against_ai_rect = draw_menu_text("2. Play Against AI", (WIDTH // 2, HEIGHT // 2), menu_font, hover=hover_play_against_ai)
        exit_rect = draw_menu_text("3. Exit", (WIDTH // 2, HEIGHT // 2 + 50), menu_font, hover=hover_exit)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# Start the game at the main menu
main_menu()

