# Pygame Minesweeper (Desktop & Web)

A classic Minesweeper game implemented in Python using Pygame-CE. This version is designed to run both as a standard desktop application and in a web browser using Pyodide (WebAssembly).

## Features

* **Classic Minesweeper Gameplay:** Uncover cells, avoid mines, and use flags to mark suspected mine locations.
* **Cross-Platform:**
    * Runs as a standalone desktop application.
    * Runs in modern web browsers via Pyodide and WebAssembly.
* **Safe First Click:** The first cell you click will never be a mine.
* **Responsive Display:** The game window can be resized on the desktop, and the game scales to the canvas size in the browser.
* **Adaptive Input:**
    * **Desktop:** Left-click to reveal, Right-click to flag.
    * **Browser/Touch:** Click/Tap to reveal, Long-press to flag.
* **New Game Button:** Easily start a new game at any time.

## How to Run

### 1. Desktop Version

**Prerequisites:**
* Python 3.x
* Pygame-CE (Community Edition)

**Installation & Setup:**
1. Clone or download this repository
```bash
git clone https://github.com/fancellu/minesweeper-pygame.git
cd minesweeper-pygame
```
2. Install the required Python package:
```bash
pip install -r requirements.txt
```
3. Run the game on the desktop:
```bash
python mineseeper.py
```

**Web Version**

1. Run build-code.zip-py to bundle the source and any assets into code.zip
2. Host the code.zip and index.html on a web server or use a local development server
3. Open index.html in a modern web browser

## To run on web via wasm

[Click here to Preview](https://acid.seedhost.eu/seedbod/minesweeperpygame/)

The game will automatically load and initialize using Pyodide

## How to Play Minesweeper (For Beginners)

Minesweeper is a single-player puzzle game. The goal is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field.

**Objective:**

*   Uncover all the cells on the board that **do not** contain mines.
*   If you uncover a cell with a mine, you lose the game.
*   Mark all the cells that **do** contain mines with flags.

**Gameplay:**

1.  **Starting the Game:**
  *   The game board is a grid of covered cells.
  *   Your first click on any cell is always safe; it will never be a mine.

2.  **Uncovering Cells:**
  *   **Desktop:** Left-click on a cell to reveal it.
  *   **Browser/Touch:** Click or tap on a cell to reveal it.
  *   **What happens when you uncover a cell?**
    *   **If it's a Mine:** Boom! The game is over, and all mine locations are revealed.
    *   **If it's a Number (1-8):** This number tells you exactly how many mines are hidden in the 8 cells immediately surrounding that numbered cell (horizontally, vertically, and diagonally). Use these numbers as clues to deduce where mines are.
    *   **If it's Blank (Empty):** This means there are no mines in any of the 8 surrounding cells. The game will automatically reveal all adjacent blank cells and any cells with numbers next to those blanks. This can clear large areas of the board quickly!

3.  **Flagging Mines:**
  *   If you suspect a cell contains a mine, you should mark it with a flag. This helps you keep track of potential mine locations and prevents you from accidentally clicking on them.
  *   **Desktop:** Right-click on a cell to place or remove a flag.
  *   **Browser/Touch:** Long-press (hold click/tap for about 0.5 seconds) on a cell to place or remove a flag.
  *   You cannot reveal a cell that has a flag on it. You must remove the flag first if you change your mind.

**Winning the Game:**

You win the game when:

*   All cells that **do not** contain mines have been revealed.
*   AND (in this version of the game) all cells that **do** contain mines have been correctly flagged.

**Losing the Game:**

You lose the game if you click on a cell that contains a mine.

**Basic Strategy Tips:**

*   **Start with the Corners/Edges:** Often, numbers near the edges or corners give you more definitive clues.
*   **Look for Obvious Mines:** If a cell shows the number '1', and there's only one unrevealed cell next to it, that unrevealed cell *must* be a mine. Flag it!
*   **Use Revealed Numbers Together:** If two numbered cells are adjacent, their clues can help you figure out shared or distinct mine locations. For example, if a '1' is next to a '2', and you've identified the mine for the '1', you can use that information to help locate the second mine for the '2'.
*   **When in Doubt, Be Cautious:** If you're unsure, it's better to leave a cell unclicked and look for more clues elsewhere than to make a risky guess.

Good luck, and have fun sweeping those mines!