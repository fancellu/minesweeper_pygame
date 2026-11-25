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


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE


class MinesweeperGame:
    mines: set[tuple[int, int]]
    flags: list[list[bool]]
    grid: list[list[int]]
    revealed: list[list[bool]]
    game_over: bool
    won: bool
    mouse_down_pos: tuple[int, int] | None
    mouse_down_time: float | None
    long_press_triggered: bool

    def __init__(self, is_wasm: bool):
        pygame.init()
        self.is_wasm = is_wasm
        self.running = True

        # One-time setup: window, drawing surface, font and assets
        flags = 0 if is_wasm else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), flags)
        # display is scaled up and blitted to screen at the end
        self.display = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        self.font = pygame.font.SysFont(None, 32)
        self.flag = pygame.image.load('flag.png')
        pygame.display.set_caption("Minesweeper")

        self.new_game()

    def new_game(self):
        """Reset the game state only."""
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.mines = set()
        self.game_over = False
        self.won = False
        self._reset_press()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def _reset_press(self):
        self.mouse_down_pos = None
        self.mouse_down_time = None
        self.long_press_triggered = False

    def _end_game(self, won: bool):
        self.game_over = True
        self.won = won
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # We don't want to put a mine under first click
    def place_mines(self, avoid_col: int, avoid_row: int) -> None:

        # Place mines
        self.mines = set()
        while len(self.mines) < MINE_COUNT:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if (x, y) in self.mines or (x == avoid_col and y == avoid_row):
                continue
            self.mines.add((x, y))

        # calculate grid[] numbers
        for x, y in self.mines:  # Here (x,y) represents (column, row)
            self.grid[y][x] = -1  # Mine at grid[row][column]
            # Increment adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if in_bounds(ny, nx) and self.grid[ny][nx] != -1:
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
                            self.display.blit(text, text.get_rect(center=rect.center))
                elif self.flags[row][col]:
                    self.display.blit(self.flag, self.flag.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(self.display, WHITE, rect)
                pygame.draw.rect(self.display, BLACK, rect, 1)

        if self.game_over:
            text = self.font.render("You Won!" if self.won else "Game Over!", True, WHITE)
            box = pygame.Rect(0, 0, 200, 200)
            box.center = (WINDOW_SIZE // 2, WINDOW_SIZE // 2)
            pygame.draw.rect(self.display, BLUE, box)
            self.display.blit(text, text.get_rect(center=box.center))

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def reveal_cell(self, row: int, col: int) -> None:
        if not in_bounds(row, col) or self.revealed[row][col] or self.flags[row][col]:
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
        # Win when all non-mine cells are revealed and all mines are flagged
        uncovered_safe = sum(row.count(True) for row in self.revealed)
        total_safe = GRID_SIZE * GRID_SIZE - MINE_COUNT
        if uncovered_safe == total_safe and all(self.flags[y][x] for x, y in self.mines):
            self._end_game(won=True)
            return True
        return False

    def toggle_flag(self, row: int, col: int) -> None:
        if in_bounds(row, col) and not self.revealed[row][col]:
            self.flags[row][col] = not self.flags[row][col]
            self.check_win()

    def _get_cell(self, event_pos: tuple[int, int]) -> tuple[int, int]:
        """Map a screen position to (col, row), accounting for window scaling."""
        screen_w, screen_h = self.screen.get_size()
        if screen_w == 0 or screen_h == 0:  # e.g. minimised window
            return -1, -1
        x = int(event_pos[0] * WINDOW_SIZE / screen_w)
        y = int(event_pos[1] * WINDOW_SIZE / screen_h)
        return x // CELL_PIXELS, y // CELL_PIXELS

    async def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.new_game()
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                col, row = self._get_cell(event.pos)
                if not in_bounds(row, col):
                    continue
                if event.button == 1:  # Left click down
                    if not self.mines:
                        self.place_mines(col, row)
                    self.mouse_down_time = time.monotonic()
                    self.mouse_down_pos = (col, row)
                    self.long_press_triggered = False
                elif event.button == 3:  # Right click (for desktop)
                    self.toggle_flag(row, col)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.mouse_down_pos is not None and not self.long_press_triggered:
                    col, row = self._get_cell(event.pos)
                    # Short press on the same cell: reveal it
                    if (col, row) == self.mouse_down_pos and not self.flags[row][col]:
                        if self.grid[row][col] == -1:
                            for mx, my in self.mines:
                                self.revealed[my][mx] = True
                            self._end_game(won=False)
                        else:
                            self.reveal_cell(row, col)
                            self.check_win()
                self._reset_press()

        # Check for long press while LMB is held
        if self.mouse_down_pos is not None and not self.long_press_triggered:
            if pygame.mouse.get_pressed()[0]:  # LMB still held
                if time.monotonic() - self.mouse_down_time >= LONG_PRESS_THRESHOLD:
                    col, row = self.mouse_down_pos
                    self.long_press_triggered = True
                    self.toggle_flag(row, col)

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
