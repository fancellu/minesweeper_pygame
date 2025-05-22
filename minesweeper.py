import pygame
import random
import platform
import asyncio
import time

# Constants
GRID_SIZE = 10
CELL_PIXELS = 40
MINE_COUNT = 10
WINDOW_SIZE = GRID_SIZE * CELL_PIXELS
FPS = 60
LONG_PRESS_THRESHOLD = 0.5  # 500ms for long press

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class MinesweeperGame:
    mines: set[tuple[int, int]] | None
    flags: list[list[bool]] | None
    grid: list[list[int]]
    revealed: list[list[bool]] | None
    game_over: bool
    won: bool
    mouse_down_pos: tuple[int, int] | None
    mouse_down_time: float | None
    long_press_triggered: bool

    def new_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.won = False

        if self.is_wasm:
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        else:
            if self.screen is None:
                self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
        self.display = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        # display is scaled up and blitted to screen at the end
        self.font = pygame.font.SysFont(None, 32)
        pygame.display.set_caption("Minesweeper")
        self.flag = pygame.image.load('flag.png')
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.mines = set()

    def __init__(self, is_wasm: bool):
        pygame.init()
        self.is_wasm = is_wasm
        self.mouse_down_pos = None
        self.long_press_triggered = False
        self.mouse_down_time = None
        self.running = True
        self.screen = None
        self.mines = None
        self.flag = None
        self.font = None
        self.display = None

        self.won = False
        self.game_over = False
        self.flags = None
        self.revealed = None
        self.grid = None

        self.new_game()

    # We don't want to put a mine under first click
    def place_mines(self, avoid_col: int, avoid_row: int) -> None:

        # Place mines
        self.mines = set()
        while len(self.mines) < MINE_COUNT:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if (x, y) in self.mines or (x == avoid_col and y == avoid_row):
                continue
            self.mines.add((x, y))
            # print(f"[DEBUG] Mine placed at (col, row) = ({x}, {y})")

        # calculate grid[] numbers
        for x, y in self.mines: # Here (x,y) represents (column, row)
            self.grid[y][x] = -1  # Mine at grid[row][column]
            # Increment adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] != -1:
                        self.grid[ny][nx] += 1

    def draw(self):
        self.display.fill(WHITE)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * CELL_PIXELS, row * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS)
                if self.revealed[row][col]:
                    if self.grid[row][col] == -1:
                        pygame.draw.rect(self.display, RED, rect)
                    else:
                        pygame.draw.rect(self.display, GRAY, rect)
                        if self.grid[row][col] > 0:
                            text = self.font.render(str(self.grid[row][col]), True, BLACK)

                            text_rect = text.get_rect(center=(
                                col * CELL_PIXELS + CELL_PIXELS // 2,
                                row * CELL_PIXELS + CELL_PIXELS // 2
                            ))
                            self.display.blit(text, text_rect)
                            # self.display.blit(text, (col * CELL_PIXELS + 15, row * CELL_PIXELS + 10))
                elif self.flags[row][col]:
                    flag_rect = self.flag.get_rect(center=(
                        col * CELL_PIXELS + CELL_PIXELS // 2,
                        row * CELL_PIXELS + CELL_PIXELS // 2
                    ))
                    self.display.blit(self.flag, flag_rect)
                else:
                    pygame.draw.rect(self.display, WHITE, rect)
                pygame.draw.rect(self.display, BLACK, rect, 1)

        if self.game_over:
            text = self.font.render("Game Over!" if not self.won else "You Won!", True, BLACK)

            pygame.draw.rect(self.display, BLUE, (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 - 100, 200, 200))
            w, _ = text.get_size()
            self.display.blit(text, (WINDOW_SIZE // 2 - w // 2, WINDOW_SIZE // 2))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def reveal_cell(self, row: int, col: int) -> None:
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE or self.revealed[row][col] or self.flags[row][
            col]:
            return
        self.revealed[row][col] = True
        if self.grid[row][col] == -1:
            return
        if self.grid[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal_cell(row + dr, col + dc)

    def check_win(self) -> bool:
        # Check if all non-mine cells are revealed
        def is_win():
            uncovered_safe = sum(row.count(True) for row in self.revealed)
            total_safe = GRID_SIZE * GRID_SIZE - MINE_COUNT
            if uncovered_safe != total_safe:
                # print(f"[DEBUG] check_win: Not all non-mine cells revealed ({uncovered_safe}/{total_safe})")
                return False

            # Check if all mines are flagged
            for x, y in self.mines:
                if not self.flags[y][x]:
                    # print(f"[DEBUG] check_win: Mine at (col, row) = ({x}, {y}) not flagged")
                    return False

            # print("[DEBUG] check_win: All conditions met, win!")
            return True

        if is_win():
            self.game_over = True
            self.won = True
            return True
        return False

    def _get_scaled_mouse_pos(self, event_pos: tuple[int, int]) -> tuple[int, int]:
        screen_w, screen_h = self.screen.get_size()
        # Prevent division by zero if window size is 0, though unlikely
        scale_x = screen_w / WINDOW_SIZE if WINDOW_SIZE > 0 else 1
        scale_y = screen_h / WINDOW_SIZE if WINDOW_SIZE > 0 else 1

        # Ensure scales are not zero to prevent division by zero if screen size is smaller
        # than WINDOW_SIZE and then scaled down to 0 by int conversion.
        # This scenario is less likely with how scaling is usually done.
        # The primary concern is screen_w/h being 0.

        mouse_x = int(event_pos[0] / scale_x) if scale_x != 0 else event_pos[0]
        mouse_y = int(event_pos[1] / scale_y) if scale_y != 0 else event_pos[1]
        return mouse_x, mouse_y

    async def update_loop(self):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.new_game()
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                scaled_x, scaled_y = self._get_scaled_mouse_pos(event.pos)
                col, row = scaled_x // CELL_PIXELS, scaled_y // CELL_PIXELS
                if event.button == 1:  # Left click down
                    if len(self.mines) == 0:
                        self.place_mines(col, row)
                    self.mouse_down_time = time.time()
                    self.mouse_down_pos = (col, row)
                    self.long_press_triggered = False
                elif event.button == 3:  # Right click (for desktop)
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and not self.revealed[row][col]:
                        self.flags[row][col] = not self.flags[row][col]
                        # print(f"[DEBUG] Flagged (col, row) = ({col}, {row})")
                        self.check_win()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.mouse_down_time is not None and self.mouse_down_pos is not None and not self.long_press_triggered:
                    scaled_x, scaled_y = self._get_scaled_mouse_pos(event.pos)
                    col, row = scaled_x // CELL_PIXELS, scaled_y // CELL_PIXELS
                    if (col, row) == self.mouse_down_pos and not self.flags[row][col]:  # Short press: reveal cell
                        if self.grid[row][col] == -1:
                            self.game_over = True
                            for mx, my in self.mines:
                                self.revealed[my][mx] = True
                        else:
                            self.reveal_cell(row, col)
                            self.check_win()
                    self.mouse_down_time = None
                    self.mouse_down_pos = None
                    self.long_press_triggered = False

        # Check for long press while LMB is held
        if self.mouse_down_time is not None and self.mouse_down_pos is not None and not self.long_press_triggered:
            if pygame.mouse.get_pressed()[0]:  # LMB still held
                col, row = self.mouse_down_pos
                if time.time() - self.mouse_down_time >= LONG_PRESS_THRESHOLD and not self.revealed[row][col]:
                    self.flags[row][col] = not self.flags[row][col]
                    # print(f"[DEBUG] Long press flagged (col, row) = ({col}, {row})")
                    self.long_press_triggered = True
                    self.check_win()

        self.draw()
        pygame.display.flip()


game: MinesweeperGame | None = None


def new_game():
    """Reset the current game state. Safe to call from JavaScript."""
    if game is not None:
        game.new_game()


async def main(is_wasm: bool = False):
    global game
    game = MinesweeperGame(is_wasm)

    while game.running:
        await game.update_loop()
        # Limit the frame rate this way, better for wasm, no need for pygame.clock
        await asyncio.sleep(1.0 / FPS)


# if wasm
if platform.system() == "Emscripten":
    asyncio.ensure_future(main(is_wasm=True))
else:
    # desktop
    if __name__ == "__main__":
        asyncio.run(main())
