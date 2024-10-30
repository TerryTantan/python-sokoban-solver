import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Get display resolution for fullscreen
# SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 100
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
UI_WIDTH = SCREEN_WIDTH // 4
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban Game with Textures")
# Constants
BG_COLOR = (230, 230, 230)
BUTTON_COLOR = (100, 100, 250)
TEXT_COLOR = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 140
BUTTON_SPACING = 100

# Define button labels for each game state
button_texts = {
    "playing": ["Menu", "Pause", "Restart"],
    "menu": ["Play", "Levels", "Restart", "Solutions"],
    "level_select": [f"Level {i+1}" for i in range(10)],
    "solutions": ["DFS", "BFS", "UCS", "A*", "Restart"],
    "solving": ["Menu", "Pause", "Restart"]
}


# Paths to texture images
TEXTURE_PATHS = {
    "button": "textures/UI/button.png",
    "floor": "textures/grid/floor.png",
    "wall": "textures/grid/wall_side.png",
    "ares": "textures/grid/ares1.png",
    "stone": "textures/grid/dark_crate.png",
    "switch": "textures/grid/orb.png",
    "ares_on_switch": "textures/grid/ares2.png",
    "stone_on_switch": "textures/grid/light_crate.png",
    "background": "textures/UI/back_ground.jpg"
}

# Loaded textures
textures = {key: None for key in TEXTURE_PATHS.keys()}

# Game logic variables
level = 1
state = "playing"  # Can be 'playing', 'menu', 'level_select', 'solutions', 'solving'
grid_width, grid_height = 10, 8  # Example grid size
cell_size = 0  # Size of each cell in the grid
stones = []
ares = []
switches = []
walls = []
#
font = pygame.font.Font("textures/MinecraftBold-nMK1.otf", 36)

def read_grid(level):
    global grid_width, grid_height, cell_size
    level_str = ""
    stones.clear()
    switches.clear()
    walls.clear()
    ares.clear()
    if level < 10:
        level_str = "0" + level.__str__()
    with open(f"inputs/input-{level_str}.txt", "r") as file:
        line = file.readline().split(' ')
        line[-1] = line[-1].split('\n')[0]
        stone_weight = line
        grid_width = 0
        grid_height = 0

        for y, line in enumerate(file):
            print(line)
            grid_height += 1
            grid_width = max(grid_width, len(line) - 1)
            for x, char in enumerate(line):
                if char == '#':
                    walls.append((x, y))
                if char == '$' or char == '*':
                    stones.append((x, y, stone_weight[len(stones)]))
                if char == '.' or char == '*' or char == '+':
                    switches.append((x, y))
                if char == '@' or char == '+':
                    ares.append((x, y))
    cell_size = min((SCREEN_WIDTH - UI_WIDTH) // (grid_width), SCREEN_HEIGHT // (grid_height))
    print(stones)

class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action  # Function or method to call when clicked

    def draw(self, screen):
        # Draw button texture if available, otherwise draw a colored rectangle
        if textures["button"]:
            screen.blit(textures["button"], self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw button text
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def load_textures():
    for texture_name, texture_path in TEXTURE_PATHS.items():
        if os.path.exists(texture_path):
            texture = pygame.image.load(texture_path)
            textures[texture_name] = pygame.transform.scale(texture, (cell_size, cell_size))
        else:
            print(f"Warning: {texture_path} does not exist.")
    
    if textures["switch"]:
        textures["switch"] = pygame.transform.scale(textures["switch"], (cell_size//2, cell_size//2))

    # Scale background separately
    if textures["background"]:
        backgroud = pygame.image.load(TEXTURE_PATHS["background"])
        textures["background"] = pygame.transform.scale(backgroud, (SCREEN_WIDTH*2, SCREEN_HEIGHT*2))

    if textures["button"]:
        button = pygame.image.load(TEXTURE_PATHS["button"])
        textures["button"] = pygame.transform.scale(button, (BUTTON_WIDTH, BUTTON_HEIGHT))

    print("Textures loaded successfully.")
    

buttons = []

def create_buttons():
    buttons.clear()
    button_set = button_texts[state]
    ui_x = SCREEN_WIDTH - UI_WIDTH
    button_x = ui_x + (UI_WIDTH - BUTTON_WIDTH)//2
    button_y = 20

    for text in button_set:
        action = lambda txt=text: handle_button_click(txt)
        button = Button(text, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, action)
        buttons.append(button)
        button_y += BUTTON_SPACING

def draw_buttons():
    for button in buttons:
        button.draw(screen)

# Draw game grid on the left side of the screen
def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            screen.blit(textures["floor"], (x * cell_size, y * cell_size))
    for wall in walls:
        screen.blit(textures["wall"], (wall[0] * cell_size, wall[1] * cell_size))
    for stone in stones:
        screen.blit(textures["stone"], (stone[0] * cell_size, stone[1] * cell_size))
    for switch in switches:
        screen.blit(textures["switch"], (switch[0] * cell_size + cell_size//4, switch[1] * cell_size + cell_size//4))
    screen.blit(textures["ares"], (ares[0][0] * cell_size, ares[0][1] * cell_size))
    for (x, y, _) in stones:
        if (x, y) in switches:
            screen.blit(textures["stone_on_switch"], (x * cell_size, y * cell_size))
    
    for (x, y, w) in stones:
        text = font.render(w.__str__(), True, (0, 0, 0))
        screen.blit(text, (x * cell_size + cell_size//2 - text.get_width()//2, y * cell_size + cell_size//2 - text.get_height()//2))

    for (x, y) in ares:
        if (x, y) in switches:
            screen.blit(textures["floor"], (x * cell_size, y * cell_size))
            screen.blit(textures["ares_on_switch"], (x * cell_size, y * cell_size))


# Draw the background image or fallback color
# Variables to control background movement
bg_x, bg_y = 0, 0
bg_dx, bg_dy = -1, -1

def draw_background():
    global bg_x, bg_y, bg_dx, bg_dy, screen

    if textures["background"]:
        # Move background position
        bg_x += bg_dx
        bg_y += bg_dy

        # Get background and screen dimensions
        bg_width = textures["background"].get_width()
        bg_height = textures["background"].get_height()

        # Check for boundaries, adjusting to reverse before the background fully leaves the screen
        if bg_x <= -(bg_width - SCREEN_WIDTH) or bg_x >= 0:
            bg_dx *= -1
        if bg_y <= -(bg_height - SCREEN_HEIGHT) or bg_y >= 0:
            bg_dy *= -1

        # Draw the background texture at the updated position
        screen.blit(textures["background"], (bg_x, bg_y))
    else:
        # Fallback to a solid color if no background image is loaded
        screen.fill(BG_COLOR)



# Game state handling
def handle_button_click(button_text):
    global state, level
    if state == "playing":
        if button_text == "Menu":
            state = "menu"
        elif button_text == "Pause":
            state = "paused"
        elif button_text == "Restart":
            reset_level()
    elif state == "menu":
        if button_text == "Play":
            state = "playing"
        elif button_text == "Levels":
            state = "level_select"
        elif button_text == "Restart":
            reset_level()
        elif button_text == "Solutions":
            state = "solutions"
    elif state == "level_select":
        if button_text.startswith("Level"):
            level = int(button_text.split()[1])
            reset_level()
            state = "playing"
    elif state == "solutions":
        if button_text in ["DFS", "BFS", "UCS", "A*"]:
            state = "solving"
        elif button_text == "Restart":
            reset_level()
    elif state == "solving":
        if button_text == "Menu":
            state = "menu"
        elif button_text == "Pause":
            state = "paused"
        elif button_text == "Restart":
            reset_level()
    create_buttons()  # Update buttons whenever state changes

def handle_move(direction):
    global ares, stones
    direction.lower()
    dx, dy = 0, 0
    if direction == "u":
        dy = -1
    elif direction == "d":
        dy = 1
    elif direction == "l":
        dx = -1
    elif direction == "r":
        dx = 1

    #move
    obj_x, obj_y = ares[0][0] + dx, ares[0][1] + dy

    if (obj_x, obj_y) in walls:
        return
    for i in range(len(stones)):
        if stones[i][0] == obj_x and stones[i][1] == obj_y:
            if (obj_x + dx, obj_y + dy) in walls:
                return
            for j in range(len(stones)):
                if stones[j][0] == obj_x + dx and stones[j][1] == obj_y + dy:
                    return
            stones[i] = (obj_x + dx, obj_y + dy, stones[i][2])
            break
    ares = [(obj_x, obj_y)]

def reset_level():
    global state
    state = "playing"
    read_grid(level)
    load_textures()

def game_loop():
    global running
    create_buttons()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        button.action()
                        break
            elif event.type == pygame.KEYDOWN:
                handle_key(event.key)
        draw_background()
        draw_grid()
        draw_buttons()
        pygame.time.Clock().tick(60)
        pygame.display.flip()
        

# Handle arrow key movements (placeholder)
def handle_key(key):
    if state == "playing":
        if key == pygame.K_UP:
            handle_move("u")
        elif key == pygame.K_DOWN:
            handle_move("d")
        elif key == pygame.K_LEFT:
            handle_move("l")
        elif key == pygame.K_RIGHT:
            handle_move("r")

# Start the game
read_grid(level)
load_textures()
game_loop()

pygame.quit()
sys.exit()
