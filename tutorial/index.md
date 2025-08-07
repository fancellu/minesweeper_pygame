# Tutorial: minesweeper_pygame

This project is a classic implementation of the **Minesweeper** game using the *Pygame* library. Its special design allows it to run not only as a standard desktop application but also directly in a *web browser*. The game features an adaptive control scheme, recognizing left/right clicks on desktop and distinguishing between *short taps* and *long presses* for touch devices to reveal or flag cells.


**Source Repository:** [https://github.com/fancellu/minesweeper_pygame](https://github.com/fancellu/minesweeper_pygame)

```mermaid
flowchart TD
    A0["MinesweeperGame class
"]
    A1["Game State Grids
"]
    A2["The Main Game Loop (`update_loop`)
"]
    A3["Adaptive User Input Handling
"]
    A4["Rendering (`draw` method)
"]
    A5["Cell Revealing Logic (`reveal_cell`)
"]
    A6["Desktop vs. Web (WASM) Adaptation
"]
    A7["Web Asset Bundler (`build-code-zip.py`)
"]
    A0 -- "Manages" --> A1
    A2 -- "Calls" --> A4
    A2 -- "Executes" --> A3
    A3 -- "Triggers" --> A5
    A4 -- "Visualizes" --> A1
    A5 -- "Modifies" --> A1
    A6 -- "Instantiates" --> A0
    A7 -- "Bundles assets for" --> A6
```

## Chapters

1. [Desktop vs. Web (WASM) Adaptation
](01_desktop_vs__web__wasm__adaptation_.md)
2. [The Main Game Loop (`update_loop`)
](02_the_main_game_loop___update_loop___.md)
3. [`MinesweeperGame` Class
](03__minesweepergame__class_.md)
4. [Game State Grids
](04_game_state_grids_.md)
5. [Rendering (`draw` method)
](05_rendering___draw__method__.md)
6. [Adaptive User Input Handling
](06_adaptive_user_input_handling_.md)
7. [Cell Revealing Logic (`reveal_cell`)
](07_cell_revealing_logic___reveal_cell___.md)
8. [Web Asset Bundler (`build-code-zip.py`)
](08_web_asset_bundler___build_code_zip_py___.md)


---

