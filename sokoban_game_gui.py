import pygame
import sys
import os
from sources.solver import Solver
import threading
import queue
from collections import deque
import time
from copy import deepcopy

time_out = 0.1
solver_result = queue.Queue()
move_history = deque()  # Lưu lịch sử các bước di chuyển
state_history = deque()  # Lưu trạng thái của game sau mỗi bước
current_move = None
is_running = True  # Biến kiểm soát thread
# Thêm biến global để lưu thông tin solution
current_solution = None
current_algorithm = None


def save_game_state():
    # Lưu trạng thái hiện tại của game
    return {
        "ares": deepcopy(ares),
        "stones": deepcopy(stones),
        "step_count": step_count[0],
        "weight_pushed": weght_pushed[0],
    }


def restore_game_state(state):
    # Khôi phục trạng thái game từ state đã lưu
    global ares, stones, step_count, weght_pushed
    ares = state["ares"]
    stones = state["stones"]
    step_count[0] = state["step_count"]
    weght_pushed[0] = state["weight_pushed"]


def solve_level(text):
    global is_running, current_solution, current_algorithm
    current_algorithm = text
    level_str = ""
    if level < 10:
        level_str = "0" + level.__str__()
    else:
        level_str = level.__str__()
    solver = Solver(
        text, f"inputs/input-{level_str}.txt", f"outputs/output-{level_str}.txt"
    )
    solution = solver.run()  # Nhận đối tượng Solution
    current_solution = solution  # Lưu solution để hiển thị
    if not is_running:
        return
    for move in solution.path:
        if not is_running:
            break
        solver_result.put(move.lower())


def start_solver(text):
    global is_running
    is_running = True
    solver_thread = threading.Thread(target=solve_level, args=(text,))
    solver_thread.daemon = True
    solver_thread.start()


def illustrate_solution():
    global state, current_move, is_running
    state = "pausing"
    while is_running and (state == "illustrating" or state == "pausing"):
        if not solver_result.empty() and state == "illustrating":
            move = solver_result.get()
            current_move = move
            state_history.append(
                save_game_state()
            )  # Lưu trạng thái trước khi di chuyển
            move_history.append(move)
            handle_move(move)
        time.sleep(time_out)
    print("Done illustrating")
    solver_result.queue.clear()


def start_ilustrating():
    global is_running
    is_running = True
    illustrate_thread = threading.Thread(target=illustrate_solution)
    illustrate_thread.daemon = True
    illustrate_thread.start()


# Initialize pygame
pygame.init()

# Get display resolution for fullscreen
# SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 100
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
UI_WIDTH = SCREEN_WIDTH // 4  # Tăng UI_WIDTH từ 1/4 lên 1/3 màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban Game with Textures")
# Constants
BG_COLOR = (230, 230, 230)
BUTTON_COLOR = (100, 100, 250)
TEXT_COLOR = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 190, 60  # Giảm kích thước button
BUTTON_SPACING = 20  # Khoảng cách giữa các button
# Cập nhật button_texts để thêm các nút mới
button_texts = {
    "playing": ["Levels", "Solution", "Restart"],
    "selecting": [f"Level {i+1}" for i in range(10)],
    "solution": ["DFS", "BFS", "UCS", "A*", "Restart"],
    "solving": ["Stop"],
    "illustrating": ["Pause", "Next", "Restart"],
    "pausing": ["Start", "Next", "Restart"],
    "won": ["Levels", "Restart"],
}


# Paths to texture images
GUI_RESOURCES_PATH = "resources/gui"
TEXTURE_PATHS = {
    "button": f"{GUI_RESOURCES_PATH}/grid/button.png",
    "floor": f"{GUI_RESOURCES_PATH}/grid/floor.png",
    "wall": f"{GUI_RESOURCES_PATH}/grid/wall_side.png",
    "ares": f"{GUI_RESOURCES_PATH}/grid/ares1.png",
    "stone": f"{GUI_RESOURCES_PATH}/grid/dark_crate.png",
    "switch": f"{GUI_RESOURCES_PATH}/grid/orb.png",
    "ares_on_switch": f"{GUI_RESOURCES_PATH}/grid/ares2.png",
    "stone_on_switch": f"{GUI_RESOURCES_PATH}/grid/light_crate.png",
    "background": f"{GUI_RESOURCES_PATH}/grid/back_ground.jpg",
    "board": f"{GUI_RESOURCES_PATH}/grid/toasts.png",
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

# Fonts
font = pygame.font.Font(f"{GUI_RESOURCES_PATH}/fonts/MinecraftBold-nMK1.otf", 36)
big_font = pygame.font.Font(f"{GUI_RESOURCES_PATH}/fonts/MinecraftBold-nMK1.otf", 120)


class Button:
    def __init__(
        self,
        text,
        pos,
        size,
        texture,
        hover_tint=(30, 30, 30),
        click_tint=(-50, -50, -50),
        font=None,
    ):
        self.text = text
        self.pos = pos
        self.size = size
        self.texture = pygame.transform.scale(
            texture["button"], size
        )  # Scale texture to button size
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
    else:
        level_str = level.__str__()
    with open(f"inputs/input-{level_str}.txt", "r") as file:
        line = file.readline().split(" ")
        line[-1] = line[-1].split("\n")[0]
        stone_weight = line
        grid_width = 0
        grid_height = 0

        for y, line in enumerate(file):
            grid_height += 1
            grid_width = max(grid_width, len(line) - 1)
            for x, char in enumerate(line):
                if char == "#":
                    walls.append((x, y))
                if char == "$" or char == "*":
                    stones.append((x, y, stone_weight[len(stones)]))
                if char == "." or char == "*" or char == "+":
                    switches.append((x, y))
                if char == "@" or char == "+":
                    ares.append((x, y))
    cell_size = min(
        (SCREEN_WIDTH - UI_WIDTH) // (grid_width), SCREEN_HEIGHT // (grid_height)
    )


def load_textures():
    for texture_name, texture_path in TEXTURE_PATHS.items():
        if os.path.exists(texture_path):
            texture = pygame.image.load(texture_path)
            textures[texture_name] = pygame.transform.scale(
                texture, (cell_size, cell_size)
            )
        else:
            print(f"Warning: {texture_path} does not exist.")

    if textures["switch"]:
        textures["switch"] = pygame.transform.scale(
            textures["switch"], (cell_size // 2, cell_size // 2)
        )

    # Scale background separately
    if textures["background"]:
        backgroud = pygame.image.load(TEXTURE_PATHS["background"])
        textures["background"] = pygame.transform.scale(
            backgroud, (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
        )

    if textures["board"]:
        board = pygame.image.load(TEXTURE_PATHS["board"])
        board_height = (
            300 if not current_solution else 400
        )  # Điều chỉnh chiều cao board dựa vào có solution hay không
        textures["board"] = pygame.transform.scale(board, (UI_WIDTH, board_height))


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
        screen.blit(
            textures["switch"],
            (
                switch[0] * cell_size + cell_size // 4,
                switch[1] * cell_size + cell_size // 4,
            ),
        )
    screen.blit(textures["ares"], (ares[0][0] * cell_size, ares[0][1] * cell_size))
    for x, y, _ in stones:
        if (x, y) in switches:
            screen.blit(textures["stone_on_switch"], (x * cell_size, y * cell_size))

    for x, y, w in stones:
        text = font.render(w.__str__(), True, (0, 0, 0))
        screen.blit(
            text,
            (
                x * cell_size + cell_size // 2 - text.get_width() // 2,
                y * cell_size + cell_size // 2 - text.get_height() // 2,
            ),
        )

    for x, y in ares:
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


def draw_solving():
    text = big_font.render("SOLVING...", True, TEXT_COLOR)
    screen.blit(
        text,
        (
            SCREEN_WIDTH // 2 - text.get_width() // 2,
            SCREEN_HEIGHT // 2 - text.get_height() // 2,
        ),
    )


def draw_won():
    text = big_font.render("YOU WIN!", True, TEXT_COLOR)
    screen.blit(
        text,
        (
            SCREEN_WIDTH // 2 - text.get_width() // 2,
            SCREEN_HEIGHT // 2 - text.get_height() // 2,
        ),
    )


def draw_board():
    board = textures["board"]
    y_offset = 20
    line_spacing = 40

    # Vẽ board background ở vị trí cao hơn
    screen.blit(board, (SCREEN_WIDTH - UI_WIDTH, 0))

    # Các thông tin cơ bản
    texts = [
        f"Level {level} - {current_algorithm}",
        state.upper(),
        f"Steps: {step_count[0]}",
        f"Weight: {weght_pushed[0]}",
    ]

    # Thêm thông tin về thuật toán và solution nếu có
    # if current_algorithm:
    # texts.append(f"Algorithm: {current_algorithm}")

    if current_solution:
        texts.extend(
            [
                f"Nodes: {current_solution.node_count}",
                f"Memory: {current_solution.memory:.2f} MB",
                f"Time: {current_solution.time:.0f} ms",
            ]
        )

    # Vẽ tất cả các dòng text
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(
            text_surface, (SCREEN_WIDTH - UI_WIDTH + 30, y_offset + i * line_spacing)
        )


def create_buttons():
    global buttons
    buttons.clear()

    vertical_offset = 100

    if state == "selecting":
        # Tính toán vị trí bắt đầu để căn giữa các button theo chiều dọc
        total_rows = (len(button_texts[state]) + 1) // 2
        total_height = total_rows * (BUTTON_HEIGHT + BUTTON_SPACING)
        y_start = (SCREEN_HEIGHT - total_height) // 2 + vertical_offset

        for i, text in enumerate(button_texts[state]):
            row = i // 2
            col = i % 2

            x_pos = (
                (SCREEN_WIDTH - UI_WIDTH + 10)
                if col == 0
                else (SCREEN_WIDTH - BUTTON_WIDTH - 10)
            )
            y_pos = y_start + row * (BUTTON_HEIGHT + BUTTON_SPACING)

            button = Button(
                text,
                (x_pos, y_pos),
                (BUTTON_WIDTH, BUTTON_HEIGHT),
                textures,
                font=font,
            )
            buttons.append(button)
        return

    # Các trạng thái khác
    total_height = len(button_texts[state]) * (BUTTON_HEIGHT + BUTTON_SPACING)
    y_start = (SCREEN_HEIGHT - total_height) // 2 + vertical_offset

    for i, text in enumerate(button_texts[state]):
        button = Button(
            text,
            (
                SCREEN_WIDTH - UI_WIDTH // 2 - BUTTON_WIDTH // 2,
                y_start + i * (BUTTON_HEIGHT + BUTTON_SPACING),
            ),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
            textures,
            font=font,
        )
        buttons.append(button)


def draw_buttons():
    for button in buttons:
        button.draw(screen)


def handle_button_click(text):
    global state, level, is_running
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
        if text == "Restart":
            state = "playing"
        else:
            state = "solving"
            reset_level(False)
            # Lưu trạng thái ban đầu
            state_history.append(save_game_state())
            start_solver(text)
    elif state == "solving":
        if text == "Stop":
            is_running = False
            state = "playing"
            reset_level()
        elif text == "Restart":
            is_running = False
            reset_level()
    elif state == "illustrating" or state == "pausing":
        if text == "Pause":
            state = "pausing"
        elif text == "Start":
            state = "illustrating"
        elif text == "Back":
            if state_history and move_history:
                move_history.pop()  # Xóa bước di chuyển cuối
                state_history.pop()  # Xóa trạng thái hiện tại
                if state_history:  # Nếu còn trạng thái trước đó
                    restore_game_state(
                        state_history[-1]
                    )  # Khôi phục trạng thái trước đó
                else:
                    reset_level(False)  # Nếu không còn trạng thái nào, reset về ban đầu
        elif text == "Next":
            if not solver_result.empty():
                state_history.append(save_game_state())
                move = solver_result.get()
                move_history.append(move)
                handle_move(move)
        elif text == "Stop":
            is_running = False
            state = "playing"
            reset_level()
        elif text == "Restart":
            is_running = False
            reset_level()
    elif state == "won":
        if text == "Levels":
            reset_level()
            state = "selecting"
        elif text == "Restart":
            reset_level()


# Game state handling
def handle_move(direction):
    global ares, stones
    direction = direction.lower()
    dx, dy = 0, 0
    if direction == "u":
        dy = -1
    elif direction == "d":
        dy = 1
    elif direction == "l":
        dx = -1
    elif direction == "r":
        dx = 1

    # move
    obj_x, obj_y = ares[0][0] + dx, ares[0][1] + dy

    if (obj_x, obj_y) in walls:
        return False

    for i in range(len(stones)):
        if stones[i][0] == obj_x and stones[i][1] == obj_y:
            if (obj_x + dx, obj_y + dy) in walls:
                return False
            for j in range(len(stones)):
                if stones[j][0] == obj_x + dx and stones[j][1] == obj_y + dy:
                    return False
            stones[i] = (obj_x + dx, obj_y + dy, stones[i][2])
            weght_pushed[0] += int(stones[i][2])
            break

    step_count[0] += 1
    ares = [(obj_x, obj_y)]
    return True


def check_won():
    for x, y in switches:
        flag = False
        for sx, sy, _ in stones:
            if x == sx and y == sy:
                flag = True
                continue
        if not flag:
            return False
    return True


def reset_level(p=True):
    global state, move_history, state_history, current_solution, current_algorithm
    if p:
        state = "playing"
    move_history.clear()
    state_history.clear()
    current_solution = None  # Reset solution info
    current_algorithm = None  # Reset algorithm info
    read_grid(level)
    load_textures()


def game_loop():
    global running, state, is_running
    running = True

    while running:
        if check_won():
            state = "won"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False  # Dừng các thread
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key(event.key)

            for button in buttons:
                button.handle_event(event)

        if state == "solving":
            draw_solving()
            if not solver_result.empty():
                state = "illustrating"
                start_ilustrating()

        create_buttons()
        draw_background()
        draw_board()
        draw_buttons()
        draw_grid()
        if state == "solving":
            draw_solving()
            if not solver_result.empty():
                state = "illustrating"
                start_ilustrating()
        if state == "won":
            draw_won()
        pygame.time.Clock().tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


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

# pygame.quit()
# sys.exit()
