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
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 100
BUTTON_SPACING = 100

# Define button labels for each game state
button_texts = {
    "playing": ["Levels", "Solution", "Restart"],
    "selecting": [f"Level {i+1}" for i in range(10)],
    "solution": ["DFS", "BFS", "UCS", "A*", "Restart"],
    "solving": ["Restart"],
    "illustrating": ["Pause", "Restart"],
    "pausing": ["Resume", "Restart"],
    "won": ["Levels", "Restart"]
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
    "background": "textures/UI/back_ground.jpg",
    "board": "textures/UI/toasts.png"
}

# Loaded textures
textures = {key: None for key in TEXTURE_PATHS.keys()}

# Game logic variables
level = 1
state = "playing"
grid_width, grid_height = 10, 8  # Example grid size
cell_size = 0  # Size of each cell in the grid
stones = []
ares = []
switches = []
walls = []
step_count = [0]
weght_pushed = [0]
#
font = pygame.font.Font("textures/MinecraftBold-nMK1.otf", 36)


class Button:
    def __init__(self, text, pos, size, texture, hover_tint=(30, 30, 30), click_tint=(-50, -50, -50), font=None):
        self.text = text
        self.pos = pos
        self.size = size
        self.texture = pygame.transform.scale(texture["button"], size)  # Scale texture to button size
        self.hover_tint = hover_tint
        self.click_tint = click_tint
        self.font = font or pygame.font.Font(None, 30)
        self.rect = pygame.Rect(pos, size)
        self.clicked = False

    def apply_tint(self, tint):
        """Apply tint to texture."""
        tinted_surface = self.texture.copy()
        overlay = pygame.Surface(self.size, pygame.SRCALPHA)
        overlay.fill((*tint, 100))  # 100 is the alpha for transparency
        tinted_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted_surface

    def draw(self, screen):
        # Determine which tint to apply
        if self.clicked:
            button_image = self.apply_tint(self.click_tint)
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            button_image = self.apply_tint(self.hover_tint)
        else:
            button_image = self.texture

        # Draw the button texture (with tint if applied)
        screen.blit(button_image, self.pos)

        # Render and draw text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True  # Button is being clicked
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                handle_button_click(self.text)
            self.clicked = False  # Reset click state

def read_grid(level):
    global grid_width, grid_height, cell_size
    level_str = ""
    stones.clear()
    switches.clear()
    walls.clear()
    ares.clear()
    step_count[0] = 0
    weght_pushed[0] = 0
    if level < 10:
        level_str = "0" + level.__str__()
    with open(f"inputs/input-{level_str}.txt", "r") as file:
        line = file.readline().split(' ')
        line[-1] = line[-1].split('\n')[0]
        stone_weight = line
        grid_width = 0
        grid_height = 0

        for y, line in enumerate(file):
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


    if textures["board"]:
        board = pygame.image.load(TEXTURE_PATHS["board"])
        textures["board"] = pygame.transform.scale(board, (UI_WIDTH, UI_WIDTH))
    

buttons = []


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

def draw_board():
    board = textures["board"]
    text1 = font.render(f"Level {level}", True, TEXT_COLOR)
    text2 = font.render(state.upper(), True, TEXT_COLOR)
    text3 = font.render(f"Steps: {step_count[0]}", True, TEXT_COLOR)
    text4 = font.render(f"Weight: {weght_pushed[0]}", True, TEXT_COLOR)
    screen.blit(board, (SCREEN_WIDTH - UI_WIDTH, 0))
    screen.blit(text1, (SCREEN_WIDTH - UI_WIDTH + 30, 10 + text1.get_height()//2))
    screen.blit(text2, (SCREEN_WIDTH - UI_WIDTH + 30, 50 + text2.get_height()//2))
    screen.blit(text3, (SCREEN_WIDTH - UI_WIDTH + 30, 100 + text3.get_height()//2))
    screen.blit(text4, (SCREEN_WIDTH - UI_WIDTH + 30, 150 + text4.get_height()//2))

def create_buttons():
    global buttons
    buttons.clear()
    if state == "selecting":
        for i, text in enumerate(button_texts[state]):
            if i % 2 == 0:
                button = Button(
                    text,
                    (SCREEN_WIDTH - UI_WIDTH//2 - BUTTON_WIDTH//2 - BUTTON_SPACING, UI_WIDTH + i//2 * (BUTTON_SPACING)),
                    (BUTTON_WIDTH, BUTTON_HEIGHT),
                    textures,
                    font=font
                )
            else:
                button = Button(
                    text,
                    (SCREEN_WIDTH - UI_WIDTH//2 - BUTTON_WIDTH//2 + BUTTON_SPACING, UI_WIDTH + i//2 * (BUTTON_SPACING)),
                    (BUTTON_WIDTH, BUTTON_HEIGHT),
                    textures,
                    font=font
                )
            buttons.append(button)
        return
    for i, text in enumerate(button_texts[state]):
        button = Button(
            text,
            (SCREEN_WIDTH - UI_WIDTH// 2 - BUTTON_WIDTH//2, UI_WIDTH + i * (BUTTON_SPACING)),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
            textures,
            font=font
        )
        buttons.append(button)


def draw_buttons():
    for button in buttons:
        button.draw(screen)

def handle_button_click(text):
    global state, level
    print(f"Button clicked: {text}")
    if state == "playing":
        if text == "Levels":
            state = "selecting"
        elif text == "Solution":
            state = "solution"
        elif text == "Restart":
            reset_level()
    elif state == "selecting":
        if text.startswith("Level"):
            level = int(text.split(" ")[1])
            reset_level()
            state = "playing"
    elif state == "solution":
        if text == "DFS":
            pass
        elif text == "BFS":
            pass
        elif text == "UCS":
            pass
        elif text == "A*":
            pass
        elif text == "Restart":
            state = "playing"
    elif state == "won":
        if text == "Levels":
            reset_level()
            state = "selecting"
        elif text == "Restart":
            reset_level()

# Game state handling
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
            weght_pushed[0] += int(stones[i][2])
            break
    step_count[0] += 1
    ares = [(obj_x, obj_y)]

def check_won():
    for (x, y) in switches:
        flag = False
        for (sx, sy, _) in stones:
            if x == sx and y == sy:
                flag = True
                continue
        if not flag:
            return False
    return True

def reset_level():
    global state
    state = "playing"
    read_grid(level)
    load_textures()

def game_loop():
    global running, state
    running = True

    while running:
        if(check_won()):
            state = "won"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key(event.key)

            for button in buttons:
                button.handle_event(event)

        create_buttons()
        draw_background()
        draw_board()
        draw_buttons()
        draw_grid()
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
