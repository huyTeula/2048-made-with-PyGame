import pygame
import sys
import math
from logic import add_new_tile, is_game_over, has_won
from movement import handle_move

# Cấu hình giao diện
GRID_SIZE = 7  # Kích thước lưới 7x7
TILE_SIZE = 80  # Kích thước mỗi ô
TILE_MARGIN = 10  # Khoảng cách giữa các ô
SCREEN_SIZE = GRID_SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
BACKGROUND_COLOR = "#555555"
TILE_COLORS = {
    0: "#CCD5B4",
    2: "#EEE4DA",
    4: "#CCFF66",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
    4096: "#1E90FF",
    8192: "#1C86EE",
    16384: "#1874CD",
    32768: "#4682B4",
    65536: "#63B8FF",
    131072: "#DAA520",
    262144: "#C6E2FF",
    524288: "#FFD700",
    1048576: "#00F5FF",
}
FONT_COLOR = "#111111"

# Khởi tạo pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048 - Challenge Mode")
font = pygame.font.Font(None, 40)

def draw_menu(screen, title, buttons, background_image_path=None):
    """Vẽ menu với các nút."""
    screen.fill(BACKGROUND_COLOR)
    if background_image_path:
        try:
            background_image = pygame.image.load(background_image_path).convert()
            background_image = pygame.transform.scale(background_image, screen.get_size())
            screen.blit(background_image, (0,0))
        except pygame.error as e:
            print(f"Error loading background image: {e}")

    font_title = pygame.font.Font(None, 70)
    title_surface = font_title.render(title, True, FONT_COLOR)
    title_rect = title_surface.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 4))
    screen.blit(title_surface, title_rect)


    button_height = 60
    button_width = 200
    button_y_start = SCREEN_SIZE // 2
    button_y_spacing = 80
    for i, (text, action) in enumerate(buttons):
        button_rect = pygame.Rect(
            (SCREEN_SIZE - button_width) // 2,
            button_y_start + i * button_y_spacing,
            button_width, button_height
        )
        pygame.draw.rect(screen, "#FFFFCC", button_rect, border_radius=8)
        font_button = pygame.font.Font(None, 40)
        button_surface = font_button.render(text, True, FONT_COLOR)
        button_rect = button_surface.get_rect(center=button_rect.center)
        screen.blit(button_surface, button_rect)

        if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            action()
            break  # Ngăn chặn xử lý sự kiện khác trong cùng một khung hình

    pygame.display.flip() # Di chuyển hàm này xuống đây
class Game:
    def __init__(self):
        self.game_running = False
        self.reset_game() # Thêm hàm này
        self.menu_event = False # Biến cờ kiểm tra sự kiện menu
        

    def reset_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        add_new_tile(self.grid)
        add_new_tile(self.grid)

    def restart_game(self):
        self.reset_game()
        self.game_running = True

    def main_loop(self):
        while self.game_running:  # game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_grid = handle_move(self.grid, "left")
                    elif event.key == pygame.K_RIGHT:
                        new_grid = handle_move(self.grid, "right")
                    elif event.key == pygame.K_UP:
                        new_grid = handle_move(self.grid, "up")
                    elif event.key == pygame.K_DOWN:
                        new_grid = handle_move(self.grid, "down")
                    else:
                        new_grid = self.grid
                    if new_grid != self.grid:
                        self.grid = animate_move(self.grid, new_grid)
                        add_new_tile(self.grid)
                        if has_won(self.grid):
                            self.game_running = False
                            self.show_win_screen()
                            break
                    if is_game_over(self.grid):
                        self.game_running = False
                        self.show_gameover_screen()
                        break

            draw_grid(self.grid)
            pygame.display.flip()
            pygame.time.delay(30)

    def show_win_screen(self):
        while True:
            draw_menu(screen, "YOU WIN!", [
                ("Try Again", lambda: self.restart_game()),
                ("Exit", lambda: sys.exit())
            ], background_image_path="end_background.jpg")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


    def show_gameover_screen(self):
        while True:
            draw_menu(screen, "Game Over!", [
                ("Try Again", lambda: self.restart_game()),
                ("Exit", lambda: sys.exit())
            ], background_image_path="end_background.jpg")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


    def run(self):
        while True:
            self.handle_menu_events() # Xử lý sự kiện menu riêng
            if self.game_running:
                self.main_loop()
                break
    def handle_menu_events(self):
        if self.menu_event:
            return
        self.menu_event = True
        draw_menu(screen, "2048 - Challenge Mode", [
                ("Play", lambda: setattr(self, "game_running", True)),
                ("Exit", lambda: sys.exit())
            ], background_image_path="start_background.jpg")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.menu_event = False # Reset cờ



def animate_move(grid, target_grid, animation_speed=10): #Thêm animation_speed
    """Hoạt ảnh di chuyển ô."""
    diff = []
    for r in range(GRID_SIZE):
        row_diff = []
        for c in range(GRID_SIZE):
            if grid[r][c] != target_grid[r][c]:
                row_diff.append((c, target_grid[r][c]))
        diff.append(row_diff)

    clock = pygame.time.Clock()
    step = 0
    while step < animation_speed:
        screen.fill(BACKGROUND_COLOR)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = grid[r][c]
                color = TILE_COLORS.get(value, (60, 58, 50))
                rect = pygame.Rect(
                    c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                    r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                    TILE_SIZE, TILE_SIZE
                )

                # Hoạt ảnh di chuyển
                if len(diff[r]) > 0:
                  for target_c, target_val in diff[r]:
                    if c == target_c:
                       dx = (target_c - c) * (TILE_SIZE + TILE_MARGIN)
                       if step > 0: # Chỉ di chuyển khi step > 0
                           rect.x += dx * (step / animation_speed)
                           value = target_val
                       
                pygame.draw.rect(screen, color, rect, border_radius=8)
                if value > 0:
                    text_surface = font.render(str(value), True, FONT_COLOR)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        step += 1
    # Cập nhật grid sau khi hoạt ảnh kết thúc.
    grid = target_grid
    return grid

def draw_shiny_tile(surface, rect, color, intensity=0.5):
    """Vẽ ô với hiệu ứng chói sáng."""
    # Tạo gradient
    gradient_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    for x in range(rect.width):
        for y in range(rect.height):
            # Tính độ sáng dựa trên khoảng cách đến tâm
            distance_to_center = math.sqrt((x - rect.width // 2) ** 2 + (y - rect.height // 2) ** 2)
            brightness = int(255 * (1 - distance_to_center / (max(rect.width, rect.height) / 2)) * intensity)
            # Áp dụng độ sáng cho màu
            brightened_color = (min(color[0] + brightness, 255),
                                 min(color[1] + brightness, 255),
                                 min(color[2] + brightness, 255),
                                 255)
            gradient_surface.set_at((x, y), brightened_color)
    # Vẽ gradient lên ô
    surface.blit(gradient_surface, rect)

def draw_grid(grid):
    """Vẽ lưới trò chơi."""
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = TILE_COLORS.get(value, (60, 58, 50))
            rect = pygame.Rect(
                col * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                row * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                TILE_SIZE, TILE_SIZE
            )
            if value == 1048576:
                draw_shiny_tile(screen, rect, pygame.Color("#00F5FF")) #Áp dụng hiệu ứng
            else:
                pygame.draw.rect(screen, color, rect, border_radius=8)
            if value > 0:
                text_surface = font.render(str(value), True, FONT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("2048 - Challenge Mode")
    font = pygame.font.Font(None, 40)
    game = Game()
    game.run()